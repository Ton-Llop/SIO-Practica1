import pandas as pd
import matplotlib.pyplot as plt
import os

# Obtener carpeta del script y no donde la ejecutamos
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Cargar datos
data = pd.read_csv(script_dir + "/../DATA/cadena_subministrament_2015_2018.csv", sep=",")

# Histograma del ratio de beneficio por articulo 
plt.figure(figsize=(10, 6))
plt.hist(data["order_item_profit_ratio"], bins=30, color='skyblue', edgecolor='black')
plt.title("Histograma del Ratio de Beneficio por Artículo")
plt.xlabel("Ratio de Beneficio por Artículo")
plt.ylabel("Frecuencia")
plt.grid(axis='y', alpha=0.75)
plt.tight_layout()
# Guardar y mostrar
plt.savefig("histograma_order_item_profit_ratio.png")
plt.show()
