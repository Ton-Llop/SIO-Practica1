import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import os

# Obtener carpeta del script y no donde la ejecutamos
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Cargar datos
data = pd.read_csv(script_dir + "/../../DATA/cadena_subministrament_2015_2018.csv", sep=",")

# Detectar columnas equivalentes
# (ajusta si en tu dataset los nombres son diferentes)
col_discount = [c for c in data.columns if "discount" in c.lower()][0]
col_sales = [c for c in data.columns if "sales" in c.lower() or "total" in c.lower()][0]
col_profit = [c for c in data.columns if "profit" in c.lower() or "benefit" in c.lower() or "margin" in c.lower()][0]



# Calcular margen porcentual
data["margin_pct"] = 100 * data[col_profit] / data[col_sales].replace(0, np.nan)

# Eliminar valores nulos o erróneos
data = data.dropna(subset=[col_discount, "margin_pct"])

# Crear gráfica de dispersión
plt.figure(figsize=(10, 6))
plt.scatter(data[col_discount], data["margin_pct"], alpha=0.4, c="blue")
plt.title("Relación entre Descuento y Margen (%)")
plt.xlabel(f"Descuento ({col_discount})")
plt.ylabel("Margen (%)")
plt.grid(True, linestyle="--", alpha=0.7)

# Línea de tendencia
z = np.polyfit(data[col_discount], data["margin_pct"], 1)
xline = np.linspace(data[col_discount].min(), data[col_discount].max(), 100)
plt.plot(xline, z[0]*xline + z[1], color="red", linewidth=2, label="Tendencia lineal")
plt.legend()

# Guardar y mostrar
plt.tight_layout()
plt.savefig("scatter_descuento_margen_simple.png")
plt.show()

# Análisis estadístico simple: correlación Pearson
r, p = stats.pearsonr(data[col_discount], data["margin_pct"])
print(f"Correlación de Pearson: R = {r:.3f}, p = {p:.4f}")
if p < 0.05 and r < 0:
    print("Existe una correlación negativa significativa: a mayor descuento, menor margen.")
elif p < 0.05 and r > 0:
    print("Existe una correlación positiva significativa: los descuentos se asocian a mayores márgenes.")
else:
    print("No se observa una relación lineal significativa entre descuento y margen.")
