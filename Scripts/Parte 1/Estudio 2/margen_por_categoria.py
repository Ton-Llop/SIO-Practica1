import pandas as pd, numpy as np, matplotlib.pyplot as plt, os
from scipy import stats

script_dir = os.path.dirname(os.path.abspath(__file__)); os.chdir(script_dir)
df = pd.read_csv(script_dir + "/../../DATA/cadena_subministrament_2015_2018.csv")

# Detección simple de columnas
col_cat = [c for c in df.columns if "category" in c.lower()][0]
col_sales = [c for c in df.columns if ("sales" in c.lower() or "total" in c.lower())][0]
col_profit = [c for c in df.columns if any(k in c.lower() for k in ["profit","benefit","margin"])][0]

df["margin_pct"] = 100 * df[col_profit] / df[col_sales].replace(0, np.nan)
df = df.dropna(subset=["margin_pct", col_cat])

# Limita a top 10 categorías (legible)
top = df[col_cat].value_counts().index[:10]
d = df[df[col_cat].isin(top)]

# Boxplot
plt.figure(figsize=(12,6))
d.boxplot(column="margin_pct", by=col_cat, showfliers=False)
plt.title("Margen (%) por Categoría (Top 10)"); plt.suptitle("")
plt.xlabel("Categoría"); plt.ylabel("Margen (%)")
plt.xticks(rotation=35, ha="right"); plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.tight_layout(); plt.savefig("g2_boxplot_margen_categoria_simple.png"); plt.show()

# ANOVA simple
groups = [g["margin_pct"].values for _, g in d.groupby(col_cat)]
F, p = stats.f_oneway(*groups)
print(f"ANOVA: F={F:.2f}, p={p:.4e}")
print("Diferencias significativas entre categorías." if p<0.05 else "No hay diferencias significativas.")
