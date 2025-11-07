import pandas as pd, matplotlib.pyplot as plt, os

script_dir = os.path.dirname(os.path.abspath(__file__)); os.chdir(script_dir)
df = pd.read_csv(script_dir + "/../../DATA/cadena_subministrament_2015_2018.csv")

col_cat = [c for c in df.columns if "category" in c.lower()][0]
col_disc = [c for c in df.columns if "discount" in c.lower()][0]
posibles = ["shipping_mode","ship_mode","shipment_mode","delivery_type"]
col_ship = next((c for c in df.columns if c.lower() in posibles), None)
if col_ship is None:
    raise ValueError("No se encontró ninguna columna de modo de envío.")


# Top 8 categorías (legible)
top = df[col_cat].value_counts().index[:8]
d = df[df[col_cat].isin(top)].dropna(subset=[col_disc])

pivot = d.pivot_table(index=col_cat, columns=col_ship, values=col_disc, aggfunc="mean").fillna(0)
pivot = pivot.loc[pivot.mean(axis=1).sort_values(ascending=False).index]

pivot.plot(kind="bar", stacked=True, figsize=(12,6))
plt.title("Descuento medio por Categoría y Modo de Envío")
plt.xlabel("Categoría"); plt.ylabel("Descuento medio (%)")
plt.legend(title="Modo de envío"); plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.tight_layout(); plt.savefig("g3_descuento_medio_cat_ship_simple.png"); plt.show()

print("\nTop categorías por descuento medio (promedio sobre modos):")
print(d.groupby(col_cat)[col_disc].mean().sort_values(ascending=False).head(5))
