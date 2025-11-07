import pandas as pd, numpy as np, matplotlib.pyplot as plt, os
from scipy import stats

script_dir = os.path.dirname(os.path.abspath(__file__)); os.chdir(script_dir)
df = pd.read_csv(script_dir + "/../../DATA/cadena_subministrament_2015_2018.csv")

col_date = next((c for c in df.columns if "date" in c.lower()), "order_date")
df[col_date] = pd.to_datetime(df[col_date], errors="coerce")
col_profit = [c for c in df.columns if any(k in c.lower() for k in ["profit","benefit","margin"])][0]

d = df.dropna(subset=[col_date, col_profit])
m = d.groupby(pd.Grouper(key=col_date, freq="ME"))[col_profit].sum().reset_index(name="profit_sum")

plt.figure(figsize=(13,5))
plt.plot(m[col_date], m["profit_sum"], marker="o")
plt.title("Beneficio mensual"); plt.xlabel("Mes"); plt.ylabel("Beneficio (€)")
plt.grid(True, linestyle="--", alpha=0.6); plt.tight_layout()
plt.savefig("g4_beneficio_mensual_simple.png"); plt.show()

m["t"] = np.arange(len(m))
r, p = stats.pearsonr(m["t"], m["profit_sum"])
print(f"Correlación tiempo–beneficio: R={r:.3f}, p={p:.4e}")
print("Tendencia creciente significativa." if (p<0.05 and r>0)
      else "Tendencia decreciente significativa." if (p<0.05 and r<0)
      else "Sin tendencia lineal significativa.")
