import pandas as pd
import matplotlib.pyplot as plt
import os

# Obtener carpeta del script y no donde la ejecutamos
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Cargar datos
data = pd.read_csv(script_dir + "/../DATA/cadena_subministrament_2015_2018.csv", sep=",")

# Benefit per Order vs Customer Segment agrupated bars or boxplot 
benefit_per_order = data.groupby("customer_segment")["benefit_per_order"].sum().sort_values(ascending=False)
plt.figure(figsize=(10, 6))
benefit_per_order.plot(kind="bar", color="lightgreen")
plt.title("Total Benefit per Order by Customer Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Total Benefit per Order")
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Guardar y mostrar
plt.tight_layout()
plt.savefig("barras_benefit_per_order_vs_customer_segment.png")
plt.show()