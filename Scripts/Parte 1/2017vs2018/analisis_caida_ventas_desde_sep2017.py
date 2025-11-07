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

# Filtrar desde septiembre 2017
data = data[data['order_date_dateorders'] >= '2017-09-01']

# Crear columna mensual
data['mes'] = data['order_date_dateorders'].dt.to_period('M').dt.to_timestamp()

# ==========================
# 1. Ventas mensuales por mercado
# ==========================
ventas_mercado = data.groupby(['mes', 'market'])['sales'].sum().reset_index()

plt.figure(figsize=(12,6))
for mkt in ventas_mercado['market'].unique():
    sub = ventas_mercado[ventas_mercado['market'] == mkt]
    plt.plot(sub['mes'], sub['sales'], marker='o', label=mkt)

plt.title('Ventas mensuales por mercado (desde Sep 2017)', fontsize=14, fontweight='bold')
plt.xlabel('Fecha')
plt.ylabel('Ventas totales')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("ventas_mensuales_por_mercado_desde_sep2017.png", dpi=300)
plt.show()

# ==========================
# 2. Número de pedidos por mes
# ==========================
pedidos_mes = data.groupby('mes')['order_id'].nunique()

plt.figure(figsize=(12,5))
plt.plot(pedidos_mes.index, pedidos_mes.values, marker='o', color='blue')
plt.title('Número de pedidos por mes (desde Sep 2017)', fontsize=14, fontweight='bold')
plt.ylabel('Pedidos únicos')
plt.xlabel('Fecha')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("pedidos_por_mes_desde_sep2017.png", dpi=300)
plt.show()

# ==========================
# 3. Ticket medio por pedido
# ==========================
ventas_mes = data.groupby('mes')['sales'].sum()
ticket_medio = ventas_mes / pedidos_mes

plt.figure(figsize=(12,5))
plt.plot(ticket_medio.index, ticket_medio.values, marker='o', color='green')
plt.title('Ticket medio por pedido (desde Sep 2017)', fontsize=14, fontweight='bold')
plt.ylabel('Ticket medio (€)')
plt.xlabel('Fecha')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("ticket_medio_por_pedido_desde_sep2017.png", dpi=300)
plt.show()

# ==========================
# 4. Distribución de estados de pedidos
# ==========================
estado_mes = data.groupby(['mes','order_status']).size().unstack(fill_value=0)
estado_mes_prop = estado_mes.div(estado_mes.sum(axis=1), axis=0) * 100

plt.figure(figsize=(12,6))
estado_mes_prop.plot(kind='area', stacked=True, figsize=(12,6), colormap='tab20', ax=plt.gca())
plt.title('Distribución porcentual de estados de pedidos (desde Sep 2017)', fontsize=14, fontweight='bold')
plt.ylabel('% de pedidos')
plt.xlabel('Fecha')
plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
plt.tight_layout()
plt.savefig("distribucion_estados_pedidos_desde_sep2017.png", dpi=300)
plt.show()
