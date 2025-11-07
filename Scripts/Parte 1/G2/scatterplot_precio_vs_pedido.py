import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# Obtener carpeta del script y no donde la ejecutamos 
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Cargar datos
data = pd.read_csv(script_dir + "/../../DATA/cadena_subministrament_2015_2018.csv", sep=",")

# Crear una gráfica de dispersión
plt.figure(figsize=(10, 6))
plt.scatter(data['order_item_product_price'], data['order_item_total'], alpha=0.5, c='blue')
plt.title('Relación entre Precio del Producto y Total del Pedido')
plt.xlabel('Precio del Producto (order_item_product_price)')
plt.ylabel('Total del Pedido (order_item_total)')
plt.grid(True)
plt.savefig('scatter_plot.png')
plt.show()


# Correlación de Pearson (solo R)
x = data['order_item_product_price'].values
y = data['order_item_total'].values

r = np.corrcoef(x, y)[0, 1]
print("Si la correlación es próxima a 1 o -1 indica una relación lineal fuerte entre las variables.")
print(f"Correlación de Pearson (R) = {r:.3f}")
if abs(r) > 0.7:
    print("Hay una relación lineal fuerte entre el precio del producto y el total del pedido.") 
else:
    print("No hay una relación lineal fuerte entre el precio del producto y el total del pedido.")