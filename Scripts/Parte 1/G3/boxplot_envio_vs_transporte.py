import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy import stats
import itertools


script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)


data = pd.read_csv(script_dir + "/../../DATA/cadena_subministrament_2015_2018.csv", sep=",")
data = data.dropna(subset=["days_for_shipping_real", "shipping_mode"])


#boxplot
plt.figure(figsize=(12, 6))
data.boxplot(column="days_for_shipping_real", by="shipping_mode", grid=False, patch_artist=True)
plt.title("Tiempo de Envío por Modo de Transporte")
plt.suptitle("")
plt.xlabel("Modo de Transporte (shipping_mode)")
plt.ylabel("Días Reales de Envío")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.savefig("boxplot_envio_vs_transporte.png")
plt.show()



# T-TEST 
print("\n Comparaciones t-Student  por múltiples comparaciones")
modos = data["shipping_mode"].unique()
print("Modos detectados:", list(modos))

resultados = []
for a, b in itertools.combinations(modos, 2):
    ga = data.loc[data["shipping_mode"] == a, "days_for_shipping_real"]
    gb = data.loc[data["shipping_mode"] == b, "days_for_shipping_real"]
    t_stat, p_val = stats.ttest_ind(ga, gb, equal_var=False)  # Welch
    resultados.append((a, b, len(ga), len(gb), t_stat, p_val))

res_df = pd.DataFrame(resultados, columns=["Grupo A","Grupo B","n_A","n_B","t","p_valor"])
res_df = res_df.sort_values("p_valor").reset_index(drop=True)
res_df["significativo_0.05"] = res_df["p_valor"] < 0.05

print("\nResultados:")
print(res_df)
res_df.to_csv("t_test_shipping_mode.csv", index=False)


#interpretación rápida
sig = res_df[res_df["significativo_0.05"]]
print("\nInterpretación rápida")
if len(sig) > 0:
    print(f"Hay {len(sig)} pares con p < 0.05. Ejemplos:")
    print(sig[["Grupo A","Grupo B"]].head())
else:
    print("No hay pares con p < 0.05.")

