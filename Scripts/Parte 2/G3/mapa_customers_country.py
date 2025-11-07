import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import sys
import warnings # Para ocultar advertencias de matplotlib

# --- Configuración de Rutas ---
CSV_FILE_PATH = "DATA/cadena_subministrament_2015_2018.csv"
GEOJSON_FILE_PATH = "DATA/countries.geojson"
OUTPUT_IMAGE_PATH = "PART2/G3/mapa_ventas_y_pedidos_top10.png" 

# --- PARÁMETRO DE ESCALA DE BURBUJAS ---
BUBBLE_SCALE_DIVISOR = 5

print("Iniciando la generación del mapa combinado (Color Ventas + Burbujas Pedidos)...")

try:
    # --- 1. Cargar el CSV (Pandas) ---
    try:
        df = pd.read_csv(CSV_FILE_PATH, encoding='latin1')
        print("CSV cargado correctamente.")
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo CSV en: {CSV_FILE_PATH}")
        sys.exit()

    # --- 2. Cargar el GeoJSON (Fondo del Mapa) ---
    try:
        world_gdf = gpd.read_file(GEOJSON_FILE_PATH)
        world_gdf = world_gdf[world_gdf.geometry.is_valid]
        print("GeoJSON cargado y validado.")
    except Exception as e:
        print(f"Error: No se pudo cargar el archivo GeoJSON desde: {GEOJSON_FILE_PATH}")
        sys.exit()

    # --- 3. Preparar los Datos ---
    
    # 3a. VOLUMEN TOTAL DE VENTAS (para el color)
    df_sales = df.groupby('order_country_en')['sales'].sum().reset_index()
    df_sales.columns = ['pais', 'total_sales']
    print(f"Agregado: Ventas totales ($) por país.")

    # 3b. NÚMERO DE PEDIDOS (para las burbujas)
    df_orders = df.groupby('order_country_en')['order_id'].count().reset_index()
    df_orders.columns = ['pais', 'num_ventas']
    print(f"Agregado: Número de pedidos por país.")

    # 3c. Unir ambas estadísticas
    df_stats = pd.merge(df_sales, df_orders, on='pais', how='outer')

    # --- 4. Unir Datos Estadísticos con GeoDataFrame ---
    merged_gdf = world_gdf.merge(df_stats, left_on='ADMIN', right_on='pais', how='left')
    
    merged_gdf['total_sales'] = merged_gdf['total_sales'].fillna(0)
    merged_gdf['num_ventas'] = merged_gdf['num_ventas'].fillna(0)
    print("Datos estadísticos unidos al GeoDataFrame.")

    # --- 5. Identificar el Top 10 y sus Coordenadas ---
    # Este GDF ('top10_gdf') tiene los POLÍGONOS como geometría activa
    top10_gdf = merged_gdf.nlargest(10, 'num_ventas').copy()
    
    # Calculamos los puntos y los guardamos en una nueva columna
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        top10_gdf['point_to_plot'] = top10_gdf.geometry.representative_point()
    
    print(f"Top 10 países por NÚMERO de pedidos: {top10_gdf['pais'].tolist()}")

    # --- 6. Generar el Mapa (Matplotlib) ---
    fig, ax = plt.subplots(figsize=(20, 12)) 
    ax.set_aspect('equal')

    # 6a. Dibujar el mapa de fondo
    world_gdf.plot(ax=ax, color='#E0E0E0', edgecolor='white', linewidth=0.5)

    # 6b. Dibujar el MAPA DE COLOR (Coropletas)
    merged_gdf[merged_gdf['total_sales'] > 0].plot(
        column='total_sales',
        cmap='Greens',
        ax=ax,
        legend=True,
        legend_kwds={'label': "Volumen Total de Ventas ($)", 'orientation': "horizontal", 'shrink': 0.5, 'pad': 0.01},
        missing_kwds={'color': '#E0E0E0'}
    )

    # 6c. Crear GDF de Burbujas
    # Este GDF ('gdf_burbujas_top10') tiene los PUNTOS como geometría activa
    gdf_burbujas_top10 = top10_gdf.set_geometry('point_to_plot')

    # 6d. Dibujar las BURBUJAS (Top 10)
    # Usamos el GDF que tiene los puntos como geometría
    gdf_burbujas_top10.plot(
        ax=ax,
        markersize=gdf_burbujas_top10['num_ventas'] / BUBBLE_SCALE_DIVISOR,
        color='red',
        alpha=0.6,
        edgecolor='black',
        linewidth=1
    )

    # 6e. --- ¡FIX DEFINITIVO! AÑADIR ETIQUETAS ---
    print("Añadiendo etiquetas al Top 10...")
    
    # Iteramos sobre 'top10_gdf' (el que tiene polígonos Y la columna 'point_to_plot')
    for idx, row in top10_gdf.iterrows(): 
        label = f"{row['pais']}\n{int(row['num_ventas'])}"
        
        # Guardamos el objeto 'Point' de la columna 'point_to_plot'
        point = row['point_to_plot'] 
        
        # Ajustes para que las etiquetas de Europa no se solapen
        x_offset = -5 if row['pais'] == 'France' else (5 if row['pais'] == 'Germany' else 0)
        y_offset = 5 if row['pais'] == 'France' else (5 if row['pais'] == 'United Kingdom' else 0)
        
        # Usamos las coordenadas .x e .y del 'Point' guardado
        ax.text(
            point.x + x_offset,
            point.y + y_offset,
            label, 
            fontsize=9, 
            fontweight='bold', 
            ha='center',
            bbox=dict(facecolor='white', alpha=0.5, pad=0.1, edgecolor='none')
        )

    # 6f. Título y Limpieza
    ax.set_title(
        'Ventas Totales (Color) y Top 10 Países por Nº de Pedidos (Burbujas)', 
        fontdict={'fontsize': '20', 'fontweight': '3'}
    )
    ax.set_axis_off()

    # --- 7. Guardar la Imagen ---
    plt.savefig(OUTPUT_IMAGE_PATH, dpi=300, bbox_inches='tight') 
    
    print(f"\n¡Éxito!")
    print(f"Mapa combinado guardado como imagen en: '{OUTPUT_IMAGE_PATH}'")

except Exception as e:
    print(f"Ha ocurrido un error inesperado: {e}")