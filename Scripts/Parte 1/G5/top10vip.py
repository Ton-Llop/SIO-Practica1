import pandas as pd
import matplotlib.pyplot as plt
import os


script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)


data = pd.read_csv(script_dir + "/../../DATA/cadena_subministrament_2015_2018.csv", sep=",")


data = data.dropna(subset=["customer_id", "order_item_total"])

# Calculo de ventas totales por cliente
ventas_cliente = (
    data.groupby("customer_id")["order_item_total"]
        .sum()
        .reset_index(name="ventas_totales")
)

# Top 10
top_clientes = ventas_cliente.sort_values("ventas_totales", ascending=False).head(10)

# Grafica de barras
plt.figure(figsize=(12, 6))
plt.bar(top_clientes["customer_id"].astype(str), top_clientes["ventas_totales"], color="skyblue")

plt.title("Top 10 Clientes con Más Compras Realizadas")
plt.xlabel("Cliente (customer_id)")
plt.ylabel("Ventas Totales")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("top10_clientes.png")
plt.show()
