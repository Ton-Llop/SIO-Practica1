import pandas as pd
import matplotlib.pyplot as plt
import os

# Obtener carpeta del script y no donde la ejecutamos
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Cargar datos
data = pd.read_csv(script_dir + "/../DATA/cadena_subministrament_2015_2018.csv", sep=",")

# Sales vs Category Name horizontal bars ordered big to small by sales
sales_by_category = data.groupby("category_name")["sales"].sum().sort_values(ascending=False)
plt.figure(figsize=(15, 10))
sales_by_category.plot(kind="barh", color="skyblue")
plt.title("Total Sales by Category Name")
plt.xlabel("Total Sales")
plt.ylabel("Category Name")
plt.gca().invert_yaxis()  # Invertir el eje Y para que la categoría con más ventas esté arriba
plt.grid(axis="x", linestyle="--", alpha=0.7)
# Dejar mas espacio entre cada categoría
plt.savefig("barrasH_sales_vs_category_name.png")
plt.show()