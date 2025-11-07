import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import sys

# --- Configuración de Rutas ---
CSV_FILE_PATH = "DATA/cadena_subministrament_2015_2018.csv"
GEOJSON_FILE_PATH = "DATA/countries.geojson"
OUTPUT_IMAGE_PATH = "PART2/G3/mapa_burbujas_ventas.png" 

# --- PARÁMETRO DE FILTRADO ---
# Umbral de ventas (ajústalo si es necesario)
SALES_THRESHOLD = 2000

print(f"Iniciando la generación del mapa de burbujas enfocado (Threshold > {SALES_THRESHOLD})...")

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
        print("GeoJSON cargado correctamente.")
    except Exception as e:
        print(f"Error: No se pudo cargar el archivo GeoJSON desde: {GEOJSON_FILE_PATH}")
        sys.exit()

    # --- 3. Preparar los datos (Agrupar por ciudad) ---
    required_cols = ['customer_city', 'sales', 'latitude_src', 'longitude_src']
    if not all(col in df.columns for col in required_cols):
        print(f"Error: Faltan una o más columnas requeridas: {required_cols}")
        sys.exit()

    df_limpio = df.dropna(subset=required_cols)
    df_agrupado = df_limpio.groupby('customer_city').agg(
        total_sales=('sales', 'sum'),
        latitude=('latitude_src', 'mean'),
        longitude=('longitude_src', 'mean')
    ).reset_index()

    # --- 4. APLICAR EL FILTRO (THRESHOLD) ---
    df_filtrado = df_agrupado[df_agrupado['total_sales'] > SALES_THRESHOLD].copy()
    print(f"Datos agrupados por {len(df_agrupado)} ciudades.")
    print(f"Aplicando filtro: Se mostrarán {len(df_filtrado)} ciudades (ventas > {SALES_THRESHOLD}).")
    
    # --- 5. Convertir datos de burbujas a GeoDataFrame ---
    gdf_burbujas = gpd.GeoDataFrame(
        df_filtrado, 
        geometry=gpd.points_from_xy(df_filtrado['longitude'], df_filtrado['latitude']),
        crs="EPSG:4326"
    )

    # --- 6. Generar el Mapa (Matplotlib) ---
    fig, ax = plt.subplots(figsize=(12, 10)) # Ajustado el tamaño para la región
    ax.set_aspect('equal')

    # 6a. Dibujar el mapa de fondo
    world_gdf.plot(ax=ax, color='#E0E0E0', edgecolor='white', linewidth=0.5)

    # 6b. Dibujar las burbujas (ya filtradas)
    if not gdf_burbujas.empty:
        divisor_escala = 5000 
        gdf_burbujas.plot(
            ax=ax, 
            markersize=gdf_burbujas['total_sales'] / divisor_escala, 
            color='dodgerblue', 
            alpha=0.6, 
            edgecolor='black',
            linewidth=0.5
        )
    
        # 6c. Añadir etiquetas para el Top 10 (del grupo filtrado)
        gdf_top10 = gdf_burbujas.nlargest(10, 'total_sales')
        for idx, row in gdf_top10.iterrows():
            ax.text(row.geometry.x + 0.5, row.geometry.y, row['customer_city'], 
                    fontsize=9, fontweight='bold', ha='left')

    # 6d. --- ¡NUEVO! APLICAR EL ENFOQUE/ZOOM ---
    # Fija los límites a EE.UU., México y el Caribe.
    # Puedes ajustar estos valores si quieres más o menos zoom.
    ax.set_xlim(-128, -60) # Longitud (Oeste de EE.UU. a Este del Caribe)
    ax.set_ylim(15, 50)   # Latitud (Sur del Caribe a Norte de EE.UU.)
    
    # 6e. Título y ejes
    ax.set_title(f'Ciudades Vendedoras (EE.UU.) con Ventas > {SALES_THRESHOLD:,.0f}', 
                 fontdict={'fontsize': '16', 'fontweight': '3'})
    ax.set_axis_off()

    # --- 7. Guardar la Imagen ---
    plt.savefig(OUTPUT_IMAGE_PATH, dpi=300, bbox_inches='tight') 
    
    print(f"\n¡Éxito!")
    print(f"Mapa enfocado guardado como imagen en: '{OUTPUT_IMAGE_PATH}'")

except Exception as e:
    print(f"Ha ocurrido un error inesperado: {e}")