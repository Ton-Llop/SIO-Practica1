import pandas as pd
import matplotlib.pyplot as plt
import os

#  Cargar datos 
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
data = pd.read_csv(script_dir + "/../DATA/cadena_subministrament_2015_2018.csv", sep=",")

# Calcular días de diferencia y crear columna de retraso
data["days_shipping_diff"] = data["days_for_shipping_real"] - data["days_for_shipment_scheduled"]
data["late"] = data["days_shipping_diff"] > 0

# Agrupar por producto
product_stats = (
    data.groupby("product_name")
    .agg(total_pedidos=("order_id", "count"),
         retrasados=("late", "sum"))
    .reset_index()
)
product_stats["pct_retraso"] = (product_stats["retrasados"] / product_stats["total_pedidos"]) * 100

# Filtrar productos con un mínimo de pedidos (ej. > 20 para que sea representativo)
product_stats = product_stats[product_stats["total_pedidos"] >= 20]

# Seleccionar top 10 por % retraso
top10 = product_stats.sort_values("pct_retraso", ascending=False).head(10)

# Gráfico
plt.figure(figsize=(12, 6))
bars = plt.barh(top10["product_name"], top10["pct_retraso"], color="red", alpha=0.7)
plt.xlabel("Porcentaje de pedidos retrasados (%)", fontsize=12)
plt.title("Top 10 productos con mayor porcentaje de retrasos", fontsize=14, fontweight='bold')

# Etiquetas de porcentaje a la derecha de cada barra
for bar, pct in zip(bars, top10["pct_retraso"]):
    plt.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
             f"{pct:.1f}%", va='center', fontsize=9)

plt.gca().invert_yaxis()  # para que el más alto quede arriba
plt.grid(axis='x', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("top10_productos_mayor_retraso.png", dpi=300)
plt.show()
