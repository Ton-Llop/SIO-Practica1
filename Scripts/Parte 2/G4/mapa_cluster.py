# -*- coding: utf-8 -*-
import pandas as pd
import folium
from folium.plugins import MarkerCluster
import sys
import os

# --- Configuración de rutas ---
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    # Por si se ejecuta en un entorno interactivo (p. ej. notebook)
    script_dir = os.path.abspath('.')

os.chdir(script_dir)

CSV_FILE_PATH = os.path.normpath(os.path.join(script_dir, '../../DATA/cadena_subministrament_2015_2018.csv'))
OUTPUT_HTML_PATH = "mapa_clusters_shipping_mode_leyenda.html"

print("Iniciando la generación del mapa de clústeres categórico con leyenda...\n")

try:
    # --- 1) Cargar CSV ---
    df = pd.read_csv(CSV_FILE_PATH, encoding='latin1')
    print("CSV cargado correctamente.")
except FileNotFoundError:
    print(f"❌ No se encontró el archivo CSV en: {CSV_FILE_PATH}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error al leer el CSV: {e}")
    sys.exit(1)

# --- 2) Validar columnas necesarias y limpiar ---
required_cols = ['latitude_dest', 'longitude_dest', 'shipping_mode']
missing = [c for c in required_cols if c not in df.columns]
if missing:
    print(f"❌ Faltan columnas requeridas: {missing}")
    sys.exit(1)

# Forzar a numérico lat/lon y a texto el modo
df['latitude_dest'] = pd.to_numeric(df['latitude_dest'], errors='coerce')
df['longitude_dest'] = pd.to_numeric(df['longitude_dest'], errors='coerce')
df['shipping_mode'] = df['shipping_mode'].astype(str).str.strip()

df_clean = df.dropna(subset=required_cols)
print(f"Datos limpios: {len(df_clean)} registros.")

if df_clean.empty:
    print("❌ No hay datos válidos tras la limpieza (NaN en coordenadas o shipping_mode).")
    sys.exit(1)

# --- 3) Agrupar por coordenadas y método ---
df_grouped = (
    df_clean
    .groupby(required_cols)
    .size()
    .reset_index(name='count')
)
print(f"Datos reducidos a {len(df_grouped)} puntos únicos.")

# --- 4) Colores por modo de envío ---
def get_color(mode: str) -> str:
    if mode == 'Same Day':
        return 'red'
    elif mode == 'First Class':
        return 'blue'
    elif mode == 'Second Class':
        return 'green'
    elif mode == 'Standard Class':
        return 'purple'
    return 'gray'

# --- 5) Crear mapa base (sin tiles por defecto) ---
ATTR_OSM = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
ATTR_CARTO = (ATTR_OSM + ' &copy; <a href="https://carto.com/attributions">CARTO</a>')
ATTR_STAMEN = ('Map tiles by <a href="http://stamen.com">Stamen Design</a>, '
               'under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. '
               'Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, '
               'under <a href="http://www.openstreetmap.org/copyright">ODbL</a>.')

map_center = [df_clean['latitude_dest'].mean(), df_clean['longitude_dest'].mean()]
m = folium.Map(location=map_center, zoom_start=2, tiles=None)  # sin tiles por defecto

# --- 6) Capas base con atribución ---
folium.TileLayer('openstreetmap', name='OpenStreetMap', attr=ATTR_OSM).add_to(m)
folium.TileLayer('cartodbdark_matter', name='CartoDB Dark', attr=ATTR_CARTO).add_to(m)
folium.TileLayer('cartodbpositron', name='CartoDB Positron', attr=ATTR_CARTO).add_to(m)
folium.TileLayer('Stamen Toner', name='Stamen Toner', attr=ATTR_STAMEN).add_to(m)

# --- 7) Marcadores + Clúster ---
cluster = MarkerCluster(name='Envíos (cluster)').add_to(m)

for _, row in df_grouped.iterrows():
    lat = float(row['latitude_dest'])
    lon = float(row['longitude_dest'])
    mode = row['shipping_mode']
    cnt = int(row['count'])
    color = get_color(mode)

    popup_html = folium.Popup(
        f"<b>Shipping mode:</b> {mode}<br><b>Pedidos en este punto:</b> {cnt}",
        max_width=300
    )

    # Puedes usar Marker con Icon o CircleMarker. Aquí uso Marker con Icon
    folium.Marker(
        location=[lat, lon],
        popup=popup_html,
        icon=folium.Icon(color=color, icon="circle")
    ).add_to(cluster)

# Control de capas
folium.LayerControl().add_to(m)

# --- 8) Leyenda ---
legend_html = """
<div style="
  position: fixed; bottom: 40px; left: 40px; width: 220px;
  background-color: rgba(0, 0, 0, 0.7); border: 1px solid rgba(255,255,255,0.2);
  border-radius: 8px; z-index: 9999; font-size: 14px; color: white;
  padding: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.5);
">
<b> Leyenda - Modo de Envío</b><br>
<i class="fa fa-map-marker fa-1x" style="color:red"></i> Same Day<br>
<i class="fa fa-map-marker fa-1x" style="color:blue"></i> First Class<br>
<i class="fa fa-map-marker fa-1x" style="color:green"></i> Second Class<br>
<i class="fa fa-map-marker fa-1x" style="color:purple"></i> Standard Class<br>
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

# --- 9) Guardar ---
m.save(OUTPUT_HTML_PATH)
print(f" Mapa guardado en: {os.path.abspath(OUTPUT_HTML_PATH)}")
