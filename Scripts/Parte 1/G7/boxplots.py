import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# CONFIGURACIÓN: REEMPLAZA EL NOMBRE DE TU ARCHIVO
DATA_FILE = "DATA/cadena_subministrament_2015_2018.csv"
QUANTITATIVE_VAR = "sales"
CATEGORICAL_VAR = "category_name"

try:
    df = pd.read_csv(DATA_FILE)

    print("=========================================================")
    print(f"GENERANDO BOXPLOTS: '{QUANTITATIVE_VAR}' por '{CATEGORICAL_VAR}'")
    print("=========================================================")

    # 1. Calcular el orden de las categorías (por Mediana, más robusta que la media)
    # Esto asegura que el gráfico esté ordenado, facilitando la interpretación.
    category_order = df.groupby(CATEGORICAL_VAR)[QUANTITATIVE_VAR].median().sort_values(ascending=False).index

    # 2. Generar el Boxplot
    plt.figure(figsize=(14, 10)) # Tamaño grande para asegurar que las etiquetas no se superpongan
    
    # Usamos seaborn para el boxplot, y lo ordenamos por la mediana calculada
    sns.boxplot(x=QUANTITATIVE_VAR, y=CATEGORICAL_VAR, data=df, 
                order=category_order, palette="Spectral")
    
    plt.title(f'Distribución de {QUANTITATIVE_VAR.upper()} por {CATEGORICAL_VAR.upper()}', fontsize=16)
    plt.xlabel(f'{QUANTITATIVE_VAR.capitalize()} (Valor)', fontsize=12)
    plt.ylabel(f'{CATEGORICAL_VAR.capitalize()}', fontsize=12)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    
    # Guardar el gráfico
    output_filename = "bivariado_boxplot_ventas_por_categoria.png"
    plt.tight_layout()
    plt.savefig(output_filename)
    plt.close()
    
    print(f"Gráfico guardado exitosamente: {output_filename}")

except FileNotFoundError:
    print(f"Error: El archivo '{DATA_FILE}' no se encontró. Por favor, sube el archivo CSV para ejecutar el análisis y generar el gráfico.")
except KeyError as e:
    print(f"Error: La columna {e} no se encuentra en el archivo. Revisa que las variables '{QUANTITATIVE_VAR}' y '{CATEGORICAL_VAR}' sean los nombres exactos y en minúsculas.")