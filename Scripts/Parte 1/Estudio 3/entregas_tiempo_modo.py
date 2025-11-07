import pandas as pd, numpy as np, matplotlib.pyplot as plt, os
from scipy.stats import chi2_contingency

script_dir = os.path.dirname(os.path.abspath(__file__)); os.chdir(script_dir)
df = pd.read_csv(script_dir + "/../../DATA/cadena_subministrament_2015_2018.csv")

col_status, col_mode, col_cat = "delivery_status","shipping_mode","category_name"

d = df[[col_status,col_mode,col_cat]].dropna()
d["on_time"] = d[col_status].str.lower().isin({"shipping on time","on time","delivered on time","entregado a tiempo"}).astype(int)

pct = d.groupby([col_mode,col_cat])["on_time"].mean().unstack(col_cat)*100
pct = pct.fillna(0)

plt.figure(figsize=(13,5))
im = plt.imshow(pct.values, aspect="auto", vmin=0, vmax=100)
plt.xticks(np.arange(pct.shape[1]), pct.columns, rotation=45, ha="right")
plt.yticks(np.arange(pct.shape[0]), pct.index)
plt.title("% Entregas a tiempo por modo y categoría")
cb = plt.colorbar(im); cb.set_label("% on-time")
plt.tight_layout(); plt.savefig("g2_on_time_heatmap.png"); plt.show()

# Estadística breve (Chi²: puntualidad ~ modo / categoría)
chi_m, p_m, _, _ = chi2_contingency(pd.crosstab(d[col_mode], d["on_time"]))
chi_c, p_c, _, _ = chi2_contingency(pd.crosstab(d[col_cat],  d["on_time"]))
print(f"Chi² on_time ~ modo:     p={p_m:.3e}")
print(f"Chi² on_time ~ categoría: p={p_c:.3e}")
