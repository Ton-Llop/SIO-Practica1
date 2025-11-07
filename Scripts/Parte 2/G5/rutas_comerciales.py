import os
import sys
import math
import pandas as pd
import folium
from folium import FeatureGroup
from folium.plugins import MarkerCluster

# --- Config rutas (igual estilo que antes) ---
try:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    SCRIPT_DIR = os.path.abspath('.')
os.chdir(SCRIPT_DIR)

CSV_FILE_PATH = os.path.normpath(os.path.join(SCRIPT_DIR, '../../DATA/cadena_subministrament_2015_2018.csv'))
OUTPUT_HTML_PATH = "mapa_flujo_rutas_principales.html"

print("\n🔄 Generando Mapa de Flujo (Tránsito)…")

# --- 1) Cargar datos ---
try:
    df = pd.read_csv(CSV_FILE_PATH, encoding='latin1')
except FileNotFoundError:
    print(f"❌ No se encontró el CSV: {CSV_FILE_PATH}")
    sys.exit(1)

# --- 2) Normalizar/validar columnas ---
# Intentamos usar coordenadas a nivel pedido
cols_coord = ['latitude_src', 'longitude_src', 'latitude_dest', 'longitude_dest']
fallback_cols = ['customer_country', 'order_country']  # para centroides por país
if not all(c in df.columns for c in cols_coord) and not all(c in df.columns for c in fallback_cols):
    print("❌ Faltan columnas. Necesitas:\n"
          f" - Coordenadas: {cols_coord}\n"
          f"   o bien\n"
          f" - Países: {fallback_cols} (para usar centroides)")
    sys.exit(1)

# Convertir a numérico si existen
for c in cols_coord:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors='coerce')

# --- 3) Construir origen/destino ---
def build_routes_from_coords(dd: pd.DataFrame) -> pd.DataFrame:
    base_cols = ['order_id'] if 'order_id' in dd.columns else None
    req = ['latitude_src', 'longitude_src', 'latitude_dest', 'longitude_dest']
    ddc = dd.dropna(subset=req).copy()
    if ddc.empty:
        return pd.DataFrame()
    if base_cols and base_cols[0] in ddc.columns:
        cols = base_cols + req
    else:
        # si no hay order_id, contaremos filas igualmente
        cols = req
    ddc = ddc[cols]
    g = (ddc
         .groupby(req)
         .size()
         .reset_index(name='count'))
    g['src'] = list(zip(g['latitude_src'], g['longitude_src']))
    g['dst'] = list(zip(g['latitude_dest'], g['longitude_dest']))
    return g[['src', 'dst', 'count']]

def build_routes_from_country_centroids(dd: pd.DataFrame) -> pd.DataFrame:
    # centroides: media de lat/lon por país (a partir de los destinos reales disponibles)
    # si no existen coordenadas, este fallback no se podrá calcular: en ese caso error.
    if not {'latitude_src','longitude_src','latitude_dest','longitude_dest'}.issubset(dd.columns):
        print("⚠️ Fallback por país requiere alguna columna de coordenadas para calcular centroides. "
              "Se intentará con las coordenadas existentes.")
    # Centroides de origen por país cliente
    df_src = dd.dropna(subset=['latitude_src','longitude_src'], how='any') \
               .groupby('customer_country', as_index=False)[['latitude_src','longitude_src']].mean() \
               .rename(columns={'latitude_src':'lat_src_c','longitude_src':'lon_src_c'})
    # Centroides de destino por país de pedido
    df_dst = dd.dropna(subset=['latitude_dest','longitude_dest'], how='any') \
               .groupby('order_country', as_index=False)[['latitude_dest','longitude_dest']].mean() \
               .rename(columns={'latitude_dest':'lat_dst_c','longitude_dest':'lon_dst_c'})

    tmp = dd.copy()
    tmp['customer_country'] = tmp['customer_country'].astype(str)
    tmp['order_country'] = tmp['order_country'].astype(str)
    tmp = tmp.merge(df_src, on='customer_country', how='left') \
             .merge(df_dst, on='order_country', how='left')

    tmp = tmp.dropna(subset=['lat_src_c','lon_src_c','lat_dst_c','lon_dst_c'])
    if tmp.empty:
        return pd.DataFrame()

    g = (tmp.groupby(['customer_country','order_country','lat_src_c','lon_src_c','lat_dst_c','lon_dst_c'])
             .size()
             .reset_index(name='count'))

    g['src'] = list(zip(g['lat_src_c'], g['lon_src_c']))
    g['dst'] = list(zip(g['lat_dst_c'], g['lon_dst_c']))
    return g[['src','dst','count','customer_country','order_country']]

# Intento 1: rutas por coordenadas reales
routes = build_routes_from_coords(df)

# Fallback: por país y centroides (si no había suficientes coordenadas a nivel pedido)
if routes.empty:
    if all(c in df.columns for c in fallback_cols):
        routes = build_routes_from_country_centroids(df)
        if routes.empty:
            print("❌ No fue posible calcular rutas por centroides de país.")
            sys.exit(1)
        else:
            print("ℹ️ Usando rutas por país (centroides).")
    else:
        print("❌ No hay datos suficientes para construir rutas.")
        sys.exit(1)
else:
    print("ℹ️ Usando rutas por coordenadas de cada pedido.")

# --- 4) Seleccionar Top-N rutas ---
TOP_N = 20
routes_top = routes.sort_values('count', ascending=False).head(TOP_N).reset_index(drop=True)
print(f"Top {TOP_N} rutas encontradas:")
print(routes_top[['src','dst','count']].head(10).to_string(index=False))

# --- 5) Preparar mapa base ---
# Centro aproximado: media de destinos si existen, si no, media de todas las coords
if {'dst'}.issubset(routes_top.columns) and not routes_top.empty:
    lat_center = sum(lat for (lat, _lon) in routes_top['dst'])/len(routes_top)
    lon_center = sum(lon for (_lat, lon) in routes_top['dst'])/len(routes_top)
else:
    lat_center, lon_center = 20.0, 0.0

ATTR_OSM = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
ATTR_CARTO = (ATTR_OSM + ' &copy; <a href="https://carto.com/attributions">CARTO</a>')
m = folium.Map(location=[lat_center, lon_center], zoom_start=2, tiles=None)
folium.TileLayer('cartodbdark_matter', name='CartoDB Dark', attr=ATTR_CARTO).add_to(m)
folium.TileLayer('openstreetmap', name='OpenStreetMap', attr=ATTR_OSM).add_to(m)

# --- 6) Escalado de grosor (weight) por nº de pedidos ---
cmin, cmax = routes_top['count'].min(), routes_top['count'].max()
def scale_weight(c, min_w=2, max_w=12):
    if cmax == cmin:
        return (min_w + max_w) / 2
    return min_w + (max_w - min_w) * ((c - cmin) / (cmax - cmin))

# Color neutro para rutas (puedes cambiar a un gradiente si quieres)
def route_color(c):
    # más oscuro para más tráfico
    # devuelve un color hex sencillo por tramos
    if c >= 0.9 * cmax:
        return "#ffa600"  # muy alto
    elif c >= 0.6 * cmax:
        return "#ff6e54"
    elif c >= 0.3 * cmax:
        return "#dd5182"
    else:
        return "#955196"

routes_fg = FeatureGroup(name=f"Top {TOP_N} rutas").add_to(m)

# --- 7) Dibujar rutas y nodos ---
# Nodos: grado de salida/entrada
deg = {}
for _, r in routes_top.iterrows():
    deg[r['src']] = deg.get(r['src'], 0) + r['count']
    deg[r['dst']] = deg.get(r['dst'], 0) + r['count']

# Líneas
for idx, row in routes_top.iterrows():
    (lat1, lon1) = row['src']
    (lat2, lon2) = row['dst']
    cnt = int(row['count'])
    weight = scale_weight(cnt)
    color = route_color(cnt)

    tooltip = f"#{idx+1} Ruta | Pedidos: {cnt}"
    folium.PolyLine(
        locations=[(lat1, lon1), (lat2, lon2)],
        color=color,
        weight=weight,
        opacity=0.8,
        tooltip=tooltip
    ).add_to(routes_fg)

# Marcadores (origen/destino) como círculos con tamaño por grado
nodes_fg = FeatureGroup(name="Nodos (origen/destino)").add_to(m)
for (lat, lon), val in deg.items():
    radius = 3 + 7 * (val - min(deg.values())) / (max(deg.values()) - min(deg.values()) if max(deg.values()) != min(deg.values()) else 1)
    folium.CircleMarker(
        location=(lat, lon),
        radius=radius,
        color="#2EC4B6",
        fill=True,
        fill_opacity=0.7,
        popup=folium.Popup(f"Conexiones (pedidos) en este nodo: {val}", max_width=260)
    ).add_to(nodes_fg)

# --- 8) Leyenda simple ---
legend = """
<div style="
 position: fixed; bottom: 40px; left: 40px; z-index: 9999;
 background: rgba(0,0,0,0.75); color: white; padding: 10px 12px;
 border-radius: 8px; font-size: 13px; border: 1px solid rgba(255,255,255,0.2);
">
<b>Mapa de Flujo – Rutas Principales</b><br>
Línea = Ruta Origen → Destino<br>
Grosor = Nº de pedidos (más grueso = más tráfico)<br>
Color ≈ Volumen relativo de la ruta
</div>
"""
m.get_root().html.add_child(folium.Element(legend))

folium.LayerControl(collapsed=False).add_to(m)

# --- 9) Guardar ---
m.save(OUTPUT_HTML_PATH)
print(f" Mapa guardado en: {os.path.abspath(OUTPUT_HTML_PATH)}")