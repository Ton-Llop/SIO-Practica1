import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.stats import chi2_contingency

# Obtener carpeta del script y no donde la ejecutamos
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Cargar datos
data = pd.read_csv(script_dir + "/../../DATA/cadena_subministrament_2015_2018.csv", sep=",")

# Agrupar clientes por país y segmento
clientes_segmento = data.groupby(["customer_country", "customer_segment"])["customer_id"].nunique().unstack(fill_value=0)

# Crear gráfico de barras apiladas
clientes_segmento.plot(kind="bar", stacked=True, figsize=(14, 7))

plt.title("Número de Clientes por Segmento y País")
plt.xlabel("País (customer_country)")
plt.ylabel("Número de Clientes Únicos")
plt.xticks(rotation=90)
plt.legend(title="Segmento de Cliente")
plt.tight_layout()

# Guardar y mostrar
plt.savefig("barras_apiladas_clientes.png")
plt.show()


# CHI-CUADRADO DE INDEPENDENCIA
chi2, p, dof, expected = chi2_contingency(clientes_segmento)
print("\nChi-square test")
print(f"Chi² = {chi2:.3f}")
print(f"Grados de libertad = {dof}")
print(f"p-valor = {p:.4}")

if p < 0.05:
    print("La distribución de segmentos depende significativamente del país.")
else:
    print("No hay evidencia suficiente para afirmar que la distribución de segmentos dependa del país.")
