import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy import stats
import numpy as np


script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

data = pd.read_csv(script_dir + "/../../DATA/cadena_subministrament_2015_2018.csv", sep=",")
# Convertir fechas y limpiar nulos
data["order_date_dateorders"] = pd.to_datetime(data["order_date_dateorders"], errors="coerce")
data = data.dropna(subset=["order_date_dateorders", "order_item_total"])


# Agrupar ventas por mes
ventas_tiempo = (
    data.groupby(pd.Grouper(key="order_date_dateorders", freq="ME"))["order_item_total"]
    .sum()
    .reset_index()
)
# Gráfico de línea
plt.figure(figsize=(14, 6))
plt.plot(
    ventas_tiempo["order_date_dateorders"],
    ventas_tiempo["order_item_total"],
    marker="o",
    linestyle="-",
    color="blue",
    alpha=0.8
)
plt.title("Evolución de Ventas a lo Largo del Tiempo")
plt.xlabel("Fecha (mensual)")
plt.ylabel("Ventas Totales")
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig("ventas_tiempo.png")
plt.show()


#análisis estadístico
print("\nAnálisis estadístico de la variable 'Ventas Totales'")

# Estadísticos descriptivos
print("\nEstadísticos descriptivos:")
print(ventas_tiempo["order_item_total"].describe())

# Medidas de forma: asimetría y curtosis
skew = stats.skew(ventas_tiempo["order_item_total"])
kurt = stats.kurtosis(ventas_tiempo["order_item_total"])
print(f"\nAsimetría (skewness): {skew:.3f}")
print(f"Curtosis (kurtosis): {kurt:.3f}")

# Convertir tiempo en variable numérica para correlación
ventas_tiempo["mes_num"] = np.arange(len(ventas_tiempo))

# Correlación tiempo-ventas (Pearson)
r, p = stats.pearsonr(ventas_tiempo["mes_num"], ventas_tiempo["order_item_total"])
print(f"\nCorrelación de Pearson tiempo-ventas: R = {r:.3f}, p = {p:.4f}")

# Interpretación automática
print("\nInterpretación:")
if r > 0 and p < 0.05:
    print("Existe una tendencia creciente significativa en las ventas a lo largo del tiempo.")
elif r < 0 and p < 0.05:
    print("Existe una tendencia decreciente significativa en las ventas a lo largo del tiempo.")
else:
    print("No se observa una tendencia lineal significativa. Las ventas se mantienen relativamente estables.")

if skew > 0:
    print("La distribución presenta asimetría positiva: algunos meses con ventas muy altas.")
elif skew < 0:
    print("La distribución presenta asimetría negativa: algunos meses con ventas muy bajas.")
else:
    print("La distribución es aproximadamente simétrica.")
