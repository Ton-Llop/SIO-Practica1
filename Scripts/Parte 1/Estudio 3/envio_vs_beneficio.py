import pandas as pd, numpy as np, matplotlib.pyplot as plt, os
from scipy import stats

script_dir = os.path.dirname(os.path.abspath(__file__)); os.chdir(script_dir)
df = pd.read_csv(script_dir + "/../../DATA/cadena_subministrament_2015_2018.csv")

col_days, col_ratio, col_mode = "days_for_shipping_real","order_item_profit_ratio","shipping_mode"

d = df[[col_days,col_ratio,col_mode]].dropna()
d = d[(d[col_days] >= 0) & (d[col_days] < 60) & (d[col_ratio] > -10) & (d[col_ratio] < 10)]

plt.figure(figsize=(10,6))
for m, g in d.groupby(col_mode):
    plt.scatter(g[col_days], g[col_ratio], s=14, alpha=0.6, label=str(m))
plt.xlabel("Días reales de envío"); plt.ylabel("Ratio de beneficio")
plt.title("Días de envío vs Ratio de beneficio (color: modo)")
plt.legend(title="Modo", fontsize=8); plt.grid(True, linestyle="--", alpha=0.4)
plt.tight_layout(); plt.savefig("g3_scatter_dias_vs_ratio.png"); plt.show()

r, p = stats.pearsonr(d[col_days], d[col_ratio])
print(f"Correlación Pearson (global): R={r:.3f}, p={p:.3e}")
