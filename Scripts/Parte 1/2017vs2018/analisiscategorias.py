import pandas as pd
import matplotlib.pyplot as plt
import os

# === Cargar datos ===
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
data = pd.read_csv(script_dir + "/../../DATA/cadena_subministrament_2015_2018.csv", sep=",")

# === Preparar datos ===
data['order_date_dateorders'] = pd.to_datetime(data['order_date_dateorders'], errors='coerce')
data = data.dropna(subset=['order_date_dateorders'])

# Dividir datos antes y después de septiembre 2017
antes_sep = data[data['order_date_dateorders'] < '2017-09-01']
despues_sep = data[data['order_date_dateorders'] >= '2017-09-01']

# --- Top 10 categorías antes ---
ventas_antes = (
    antes_sep.groupby('category_name')['sales']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

# --- Top 10 categorías después ---
ventas_despues = (
    despues_sep.groupby('category_name')['sales']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

# === Gráfico antes de septiembre 2017 ===
plt.figure(figsize=(12,6))
ventas_antes.sort_values().plot(kind='barh', color='steelblue', alpha=0.8)
plt.title('Top 10 categorías por ventas ANTES de septiembre 2017', fontsize=14, fontweight='bold')
plt.xlabel('Ventas totales')
plt.ylabel('Categoría')
plt.tight_layout()
plt.savefig('top10_categorias_antes_sep2017.png', dpi=300)
plt.show()

# === Gráfico desde septiembre 2017 ===
plt.figure(figsize=(12,6))
ventas_despues.sort_values().plot(kind='barh', color='orange', alpha=0.8)
plt.title('Top 10 categorías por ventas DESDE septiembre 2017', fontsize=14, fontweight='bold')
plt.xlabel('Ventas totales')
plt.ylabel('Categoría')
plt.tight_layout()
plt.savefig('top10_categorias_despues_sep2017.png', dpi=300)
plt.show()

# --- Agrupar ventas totales por categoría ---
ventas_antes = antes_sep.groupby('category_name')['sales'].sum()
ventas_despues = despues_sep.groupby('category_name')['sales'].sum()

# Seleccionamos top 8 categorías por ventas totales globales
top_categorias = (ventas_antes + ventas_despues).sort_values(ascending=False).head(8).index

# Filtramos y calculamos porcentajes
pct_antes = (ventas_antes[top_categorias] / ventas_antes.sum()) * 100
pct_despues = (ventas_despues[top_categorias] / ventas_despues.sum()) * 100

# --- Crear gráfico ---
x = range(len(top_categorias))
width = 0.35

plt.figure(figsize=(12,6))
plt.bar(x, pct_antes, width, label='Antes Sep 2017', color='steelblue', alpha=0.7)
plt.bar([i + width for i in x], pct_despues, width, label='Desde Sep 2017', color='orange', alpha=0.7)

plt.xticks([i + width/2 for i in x], top_categorias, rotation=45, ha='right')
plt.ylabel('% sobre ventas totales')
plt.title('Cambio en la distribución de ventas por categoría (Antes vs Después Sep 2017)', fontsize=14, fontweight='bold')
plt.legend()
plt.tight_layout()
plt.savefig('comparacion_porcentual_categorias_antes_despues_sep2017.png', dpi=300)
plt.show()