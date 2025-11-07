import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns  # Necesario para el mapa de densidad (KDE)
import sys

# --- Configuración de Rutas ---
# Basado en tu script anterior
CSV_FILE_PATH = "DATA/cadena_subministrament_2015_2018.csv"
GEOJSON_FILE_PATH = "DATA/countries.geojson"
OUTPUT_IMAGE_PATH = "PART2/G2/mapa_calor_retrasos.png" 

print("Iniciando la generación del mapa de calor (PNG)...")

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

    # --- 3. Preparar los datos de puntos ---
    
    # 3a. Filtrar solo pedidos con retraso
    df_retrasos = df[df['late_delivery_risk'] == 1].copy()
    print(f"Se encontraron {len(df_retrasos)} pedidos con retraso.")

    # 3b. Asegurarse de que las columnas existen
    required_cols = ['latitude_dest', 'longitude_dest']
    if not all(col in df.columns for col in required_cols):
        print("Error: Las columnas 'latitude_dest' o 'longitude_dest' no se encuentran en el CSV.")
        sys.exit()

    # 3c. Limpiar NaNs (KDE no los soporta)
    df_retrasos = df_retrasos.dropna(subset=required_cols)
    print(f"Se usarán {len(df_retrasos)} puntos con coordenadas válidas.")
    
    if df_retrasos.empty:
        print("No hay datos de retraso para mostrar en el mapa.")
        sys.exit()

    # --- 4. Generar el Mapa (Matplotlib + Seaborn) ---
    
    # 4a. Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(15, 10))
    ax.set_aspect('equal') # Importante para que el mapa no se deforme

    # 4b. Dibujar el mapa de fondo (GeoJSON)
    world_gdf.plot(ax=ax, color='#E0E0E0', edgecolor='white', linewidth=0.5)

    # 4c. Dibujar la capa de calor (KDE) encima
    # Esto calcula la densidad de los puntos y la dibuja
    sns.kdeplot(
        x=df_retrasos['longitude_dest'],
        y=df_retrasos['latitude_dest'],
        ax=ax,
        fill=True,          # Rellenar las zonas
        cmap="Reds",        # Mapa de color "caliente"
        alpha=0.6,          # Transparencia
        thresh=0.05,        # Nivel mínimo de densidad para dibujar
        warn_singular=False # Evitar avisos si hay pocos datos
    )

    # 4d. Añadir título y limpiar ejes
    ax.set_title('Mapa de Calor: Concentración de Pedidos con Retraso', 
                 fontdict={'fontsize': '16', 'fontweight': '3'})
    ax.set_axis_off() # Ocultar ejes (latitud/longitud)

    # --- 5. Guardar la Imagen ---
    # bbox_inches='tight' recorta el espacio en blanco de los bordes
    plt.savefig(OUTPUT_IMAGE_PATH, dpi=300, bbox_inches='tight') 
    
    print(f"\n¡Éxito!")
    print(f"Mapa de calor guardado como imagen en: '{OUTPUT_IMAGE_PATH}'")

except Exception as e:
    print(f"Ha ocurrido un error inesperado: {e}")
