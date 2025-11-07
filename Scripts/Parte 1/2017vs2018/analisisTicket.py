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

# Dividir antes y después de septiembre 2017
antes_sep = data[data['order_date_dateorders'] < '2017-09-01']
despues_sep = data[data['order_date_dateorders'] >= '2017-09-01']

# =============================
# Ticket medio por categoría
# =============================
ticket_antes = antes_sep.groupby('category_name').apply(lambda g: g['sales'].sum() / g['order_id'].nunique())
ticket_despues = despues_sep.groupby('category_name').apply(lambda g: g['sales'].sum() / g['order_id'].nunique())

# Seleccionar top 10 categorías con mayor ticket antes o después
top_categorias = pd.concat([ticket_antes, ticket_despues]).sort_values(ascending=False).head(10).index

ticket_antes = ticket_antes[top_categorias].sort_values(ascending=True)
ticket_despues = ticket_despues[top_categorias].sort_values(ascending=True)

# --- Gráfico ticket medio antes ---
plt.figure(figsize=(12,6))
ticket_antes.plot(kind='barh', color='steelblue', alpha=0.8)
plt.title('Ticket medio por categoría ANTES de septiembre 2017', fontsize=14, fontweight='bold')
plt.xlabel('Ticket medio (€)')
plt.ylabel('Categoría')
plt.tight_layout()
plt.savefig('ticket_medio_por_categoria_antes_sep2017.png', dpi=300)
plt.show()

# --- Gráfico ticket medio después ---
plt.figure(figsize=(12,6))
ticket_despues.plot(kind='barh', color='orange', alpha=0.8)
plt.title('Ticket medio por categoría DESDE septiembre 2017', fontsize=14, fontweight='bold')
plt.xlabel('Ticket medio (€)')
plt.ylabel('Categoría')
plt.tight_layout()
plt.savefig('ticket_medio_por_categoria_despues_sep2017.png', dpi=300)
plt.show()
