import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy import stats

# Obtener carpeta del script y no donde la ejecutamos 
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Cargar datos
data = pd.read_csv(script_dir + "/../../DATA/cadena_subministrament_2015_2018.csv", sep=",")

# Eliminar valores nulos
data = data.dropna(subset=["days_for_shipping_real", "delivery_status"])

# Crear boxplot
plt.figure(figsize=(12, 6))
data.boxplot(column="days_for_shipping_real", by="delivery_status", grid=False, patch_artist=True)

plt.title("Días Reales de Envío según Estado de Entrega")
plt.suptitle("")  # Quitar título automático
plt.xlabel("Estado de Entrega (delivery_status)")
plt.ylabel("Días Reales de Envío")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Guardar y mostrar
plt.tight_layout()
plt.savefig("boxplot_envio_vs_estado.png")
plt.show()

#ANOVA
# Agrupar por estado
groups = [group["days_for_shipping_real"] for _, group in data.groupby("delivery_status")]

F, p = stats.f_oneway(*groups)
print("Resultados del ANOVA:")
print("La F es el valor estadístico de la prueba y la p es el valor")
print("Si la F es alta y la p es menor que 0,05, significa que hay diferencias significativas entre los grupos.")
print(f"F = {F:.3f}, p = {p:.4f}")

if p < 0.05:
    print("Hay diferencias significativas entre al menos dos estados.")
else:
    print("No se encontraron diferencias significativas entre estados.")
