import pandas as pd, numpy as np, matplotlib.pyplot as plt, os
from scipy import stats

script_dir = os.path.dirname(os.path.abspath(__file__)); os.chdir(script_dir)
df = pd.read_csv(script_dir + "/../../DATA/cadena_subministrament_2015_2018.csv")

col_days, col_mode, col_cat = "days_for_shipping_real","shipping_mode","category_name"

d = df[[col_days,col_mode,col_cat]].dropna()
d = d[(d[col_days] >= 0) & (d[col_days] < 60)]

pvt = d.groupby([col_mode,col_cat])[col_days].mean().unstack(col_cat).fillna(0)

plt.figure(figsize=(13,5))
im = plt.imshow(pvt.values, aspect="auto")
plt.xticks(np.arange(pvt.shape[1]), pvt.columns, rotation=45, ha="right")
plt.yticks(np.arange(pvt.shape[0]), pvt.index)
plt.title("Tiempo medio de envío por modo y categoría")
cb = plt.colorbar(im); cb.set_label("Días (media)")
plt.tight_layout(); plt.savefig("g4_heatmap_dias.png"); plt.show()

F_mod, p_mod = stats.f_oneway(*[g[col_days].values for _, g in d.groupby(col_mode)])
F_cat, p_cat = stats.f_oneway(*[g[col_days].values for _, g in d.groupby(col_cat)])
print(f"ANOVA días ~ modo:      F={F_mod:.3f}, p={p_mod:.3e}")
print(f"ANOVA días ~ categoría: F={F_cat:.3f}, p={p_cat:.3e}")
