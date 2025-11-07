import pandas as pd, numpy as np, matplotlib.pyplot as plt, os
from scipy import stats

# --- Setup y carga ---
script_dir = os.path.dirname(os.path.abspath(__file__)); os.chdir(script_dir)
df = pd.read_csv(script_dir + "/../../DATA/cadena_subministrament_2015_2018.csv")

# --- Columnas (según tu diccionario) ---
col_cat, col_mode, col_ratio = "category_name", "shipping_mode", "order_item_profit_ratio"

# --- Datos y limpieza ---
d = df[[col_cat, col_mode, col_ratio]].dropna()
d = d[(d[col_ratio] > -10) & (d[col_ratio] < 10)]

# --- (Opcional) limitar a Top N categorías por nº de filas para que sea legible ---
TOP_N = 12
top_cats = d[col_cat].value_counts().nlargest(TOP_N).index
d = d[d[col_cat].isin(top_cats)]

# --- Agregado y barras agrupadas ---
agg = d.groupby([col_cat, col_mode])[col_ratio].mean().unstack(col_mode).fillna(0)
x = np.arange(len(agg.index)); modes = agg.columns; width = 0.8/len(modes)

plt.figure(figsize=(13,5))
for i, m in enumerate(modes):
    plt.bar(x + i*width, agg[m].values, width=width, label=str(m))
plt.xticks(x + width*(len(modes)-1)/2, agg.index, rotation=45, ha="right")
plt.ylabel("Beneficio medio (ratio)")
plt.title("Beneficio medio por categoría (Top 12) y modo de envío")
plt.legend(title="Modo")
plt.tight_layout(); plt.savefig("g1_beneficio_cat_modo.png"); plt.show()

# --- Estadística breve (ANOVA 1-factor) ---
F_cat, p_cat = stats.f_oneway(*[g[col_ratio].values for _, g in d.groupby(col_cat)])
F_mod, p_mod = stats.f_oneway(*[g[col_ratio].values for _, g in d.groupby(col_mode)])
print(f"ANOVA categoría: F={F_cat:.3f}, p={p_cat:.3e}")
print(f"ANOVA modo:      F={F_mod:.3f}, p={p_mod:.3e}")
print("Interpretación rápida: p<0.05 => diferencias significativas en el beneficio medio.")
