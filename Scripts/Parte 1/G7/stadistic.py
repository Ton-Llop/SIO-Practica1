import pandas as pd
import numpy as np

# CONFIGURACIÓN: REEMPLAZA EL NOMBRE DE TU ARCHIVO
DATA_FILE = "DATA/cadena_subministrament_2015_2018.csv"
QUANTITATIVE_VAR = "sales"
CATEGORICAL_VAR = "category_name"

try:
    df = pd.read_csv(DATA_FILE)

    # ======================================================================
    # 1. ANÁLISIS UNIVARIADO: ESTADÍSTICAS GENERALES DE VENTAS
    # ======================================================================
    
    print("=========================================================")
    print(f"ESTADÍSTICAS DESCRIPTIVAS UNIVARIADAS para '{QUANTITATIVE_VAR}'")
    print("=========================================================")

    # Calcula las estadísticas de tendencia central, variabilidad y forma
    sales_stats = df[QUANTITATIVE_VAR].describe().to_frame()
    sales_stats.loc['skewness'] = df[QUANTITATIVE_VAR].skew()
    sales_stats.loc['kurtosis'] = df[QUANTITATIVE_VAR].kurt()
    sales_stats.loc['IQR'] = sales_stats.loc['75%'] - sales_stats.loc['25%']

    print(sales_stats)
    print("\n")

    # ======================================================================
    # 2. ANÁLISIS BIVARIADO: ESTADÍSTICAS CONDICIONALES (VENTAS POR CATEGORÍA)
    # ======================================================================
    
    print("=========================================================")
    print(f"ESTADÍSTICAS DESCRIPTIVAS CONDICIONALES: '{QUANTITATIVE_VAR}' por '{CATEGORICAL_VAR}'")
    print("=========================================================")

    # Agrupa los datos por categoría y calcula las estadísticas clave
    # La mediana es crucial por su robustez ante outliers.
    stats_por_categoria = df.groupby(CATEGORICAL_VAR)[QUANTITATIVE_VAR].agg(
        Total_Ventas='sum',
        Conteo_Ordenes='count',
        Media='mean',
        Mediana='median',
        Desviacion_Estandar='std',
        Min='min',
        Max='max'
    ).sort_values(by='Media', ascending=False)
    
    print(stats_por_categoria)

except FileNotFoundError:
    print(f"Error: El archivo '{DATA_FILE}' no se encontró. Por favor, asegúrate de subir el archivo CSV para ejecutar este análisis.")
except KeyError as e:
    print(f"Error: La columna {e} no se encuentra en el archivo. Revisa que las variables '{QUANTITATIVE_VAR}' y '{CATEGORICAL_VAR}' sean correctas y en minúsculas.")