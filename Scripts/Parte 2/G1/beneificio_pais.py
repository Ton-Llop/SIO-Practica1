import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# --- Configuración de Rutas ---
# Asegúrate de que estas rutas sean correctas en tu entorno local.
CSV_FILE_PATH = "DATA/cadena_subministrament_2015_2018.csv"
GEOJSON_FILE_PATH = "DATA/countries.geojson"
OUTPUT_IMAGE_PATH = "PART2/G1/mapa_beneficio_pais.png" # Salida como imagen PNG

print("Iniciando la generación del mapa...")

try:
    # --- 1. Cargar y procesar los datos (Pandas) ---
    try:
        df = pd.read_csv(CSV_FILE_PATH, encoding='latin1')
        print("CSV cargado correctamente.")
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo CSV en: {CSV_FILE_PATH}")
        print("Asegúrate de que la ruta es correcta.")
        exit()

    # Agrupar por país y calcular el beneficio medio
    df_agrupado = df.groupby('order_country_en')['benefit_per_order'].mean().reset_index()
    df_agrupado.columns = ['pais', 'beneficio_medio']
    print("Datos agrupados por país.")

    # --- 2. Cargar el GeoJSON (Geopandas) ---
    try:
        gdf = gpd.read_file(GEOJSON_FILE_PATH)
        print("GeoJSON cargado correctamente.")
    except Exception as e:
        print(f"Error: No se pudo cargar el archivo GeoJSON desde: {GEOJSON_FILE_PATH}")
        print(f"Detalle: {e}")
        exit()

    # --- 3. Unir los datos geográficos con los datos de beneficio ---
    # Usamos 'ADMIN' (del GeoJSON) y 'pais' (de nuestro df_agrupado)
    merged_gdf = gdf.merge(df_agrupado, left_on='ADMIN', right_on='pais', how='left')
    
    # Rellenar países sin datos (NaN) con 0 para que no salgan en blanco
    merged_gdf['beneficio_medio'] = merged_gdf['beneficio_medio'].fillna(0)
    print("Datos unidos (merge) correctamente.")

    # --- 4. Generar el Mapa (Matplotlib) ---
    
    # Crear la figura y los ejes para el gráfico
    # Ajusta figsize para cambiar el tamaño (ancho, alto) en pulgadas
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))

    # Dibujar el mapa
    # 'column' es la columna de datos que define el color
    # 'cmap' es el mapa de color (YlOrRd = Amarillo-Naranja-Rojo)
    # 'legend=True' añade la barra de leyenda
    # 'ax=ax' le dice dónde dibujarse
    # 'edgecolor' dibuja los bordes
    merged_gdf.plot(column='beneficio_medio', 
                    cmap='RdYlBu', 
                    linewidth=0.8, 
                    ax=ax, 
                    edgecolor='0.8', 
                    legend=True,
                    legend_kwds={'label': "Beneficio Medio por Pedido"})

    # Añadir título
    ax.set_title('Beneficio Medio por País de Destino (Order Country)', 
                 fontdict={'fontsize': '16', 'fontweight': '3'})

    # Opcional: Ocultar los ejes de latitud/longitud
    ax.set_axis_off()

    # --- 5. Guardar la Imagen ---
    plt.savefig(OUTPUT_IMAGE_PATH, dpi=300) # dpi=300 para alta resolución
    
    print(f"\n¡Éxito!")
    print(f"Mapa guardado como imagen en: '{OUTPUT_IMAGE_PATH}'")

except Exception as e:
    print(f"Ha ocurrido un error inesperado: {e}")