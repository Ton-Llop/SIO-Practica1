import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# ======================================================================
# CONFIGURACIÓN
# ======================================================================
DATA_FILE = "DATA/cadena_subministrament_2015_2018.csv"
COLUMN = "order_item_profit_ratio"

# --- Ejecución ---
try:
    # Cargar datos. Asegúrate de que esta ruta sea correcta para tu entorno.
    # Asumimos que el CSV está en la misma carpeta que el script.
    df = pd.read_csv(DATA_FILE, sep=",")
    
    # Verificar que la columna exista
    if COLUMN not in df.columns:
        raise KeyError(f"La columna '{COLUMN}' no se encontró en el archivo.")

    # ======================================================================
    # 1. ANÁLISIS ESTADÍSTICO DESCRIPTIVO (Salida en Terminal)
    # ======================================================================
    
    print("=========================================================")
    print(f"ANÁLISIS ESTADÍSTICO para '{COLUMN}'")
    print("=========================================================")
    
    # Calcular Estadísticas Descriptivas (Tendencia Central, Posición, Variabilidad)
    stats_df = df[COLUMN].describe().to_frame().T
    
    # Añadir medidas de Forma (Asimetría y Curtosis)
    stats_df['Skewness'] = df[COLUMN].skew()
    stats_df['Kurtosis'] = df[COLUMN].kurt()
    
    print("\nEstadísticas Descriptivas Completas:")
    # Usamos Markdown para formatear la salida en la terminal
    print(stats_df.to_markdown(numalign="left", stralign="left"))
    
    # ======================================================================
    # 2. ANÁLISIS CONDICIONAL Y REGLAS DE NEGOCIO (Salida en Terminal)
    # ======================================================================
    
    threshold = 0.0  # El umbral para la rentabilidad es 0
    
    count_profitable = df[df[COLUMN] > threshold].shape[0]
    count_non_profitable = df[df[COLUMN] <= threshold].shape[0]
    total_count = df.shape[0]
    
    percent_profitable = (count_profitable / total_count) * 100
    
    print("\n=========================================================")
    print(f"ANÁLISIS CONDICIONAL: Ratio de Beneficio vs Umbral de {threshold}")
    print("=========================================================")
    
    print(f"Total de Órdenes Analizadas: {total_count}")
    print(f"Porcentaje de Órdenes Rentables (> 0): {percent_profitable:.2f}%")
    print(f"Porcentaje de Órdenes No Rentables (<= 0): {100 - percent_profitable:.2f}%")
    
    # Regla de Negocio (Ejemplos):
    if percent_profitable >= 90:
        print("\n🟢 Más del 90% de los artículos son rentables.")
    elif percent_profitable >= 75:
        print("\n🟡 Tres cuartas partes de los artículos son rentables. Revisar las categorías o artículos en el 25% inferior.")
    elif percent_profitable < 50:
        print("\n🔴 Menos del 50% de los artículos son rentables. ¡Una parte mayoritaria del inventario genera pérdidas! Es necesaria una revisión de costes o precios.")
    else:
        print("\n🟡 RENDIMIENTO ACEPTABLE: La mayoría de los artículos son rentables, pero se debe monitorizar el margen.")

except FileNotFoundError:
    print(f"Error: El archivo '{DATA_FILE}' no se encontró. Por favor, asegúrate de que el archivo CSV está en la ubicación correcta.")
except KeyError as e:
    print(f"Error: La columna {e} no se encuentra. Revisa que el nombre de la columna sea exactamente '{COLUMN}'.")
except Exception as e:
    print(f"Ocurrió un error inesperado durante la ejecución: {e}")