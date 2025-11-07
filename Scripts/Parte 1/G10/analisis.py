import pandas as pd
import numpy as np
import os

# ======================================================================
# CONFIGURACIÓN
# ======================================================================
DATA_FILE = "DATA/cadena_subministrament_2015_2018.csv"
MIN_ORDERS_THRESHOLD = 20  # Mínimo de pedidos para que el producto sea representativo

# --- Ejecución ---
try:
    # 1. Cargar datos (ajusta la ruta si es necesario)
    # Asumimos que el CSV está en la misma carpeta que el script para este entorno.
    df = pd.read_csv(DATA_FILE, sep=",")
    
    # 2. Ingeniería de Características: Calcular días de diferencia y crear columna de retraso
    df["days_shipping_diff"] = df["days_for_shipping_real"] - df["days_for_shipment_scheduled"]
    # Variable categórica binaria: True si hay retraso
    df["late"] = df["days_shipping_diff"] > 0

    # 3. Análisis Descriptivo Univariado de la Diferencia de Días de Envío
    print("=====================================================================")
    print("ANÁLISIS ESTADÍSTICO DE LA SEVERIDAD DEL RETRASO ('days_shipping_diff')")
    print("=====================================================================")
    
    # Filtrar solo órdenes retrasadas (días_diff > 0) para analizar la SEVERIDAD
    late_orders = df[df["late"] == True]
    
    if not late_orders.empty:
        # Calcular estadísticas solo para los pedidos efectivamente retrasados
        diff_stats = late_orders["days_shipping_diff"].describe().to_frame().T
        diff_stats['Skewness'] = late_orders["days_shipping_diff"].skew()
        diff_stats['Kurtosis'] = late_orders["days_shipping_diff"].kurt()
        
        print("\nEstadísticas (solo para pedidos RETRASADOS - días > 0):")
        print(diff_stats.to_markdown(numalign="left", stralign="left"))

        print("\nInterpretación Clave:")
        print(f"-> Media del Retraso: {diff_stats['mean'].iloc[0]:.2f} días.")
        print(f"-> Desv. Estándar: {diff_stats['std'].iloc[0]:.2f}. Indica la consistencia del retraso.")
        print(f"-> Máximo Retraso: {diff_stats['max'].iloc[0]:.0f} días (Outlier de servicio).")
    else:
        print("No se encontraron órdenes retrasadas para realizar el análisis de severidad.")


    # 4. ANÁLISIS BIVARIADO: Rendimiento de Retraso por Producto
    print("\n=====================================================================")
    print("ANÁLISIS DE RENDIMIENTO: Porcentaje de Retrasos por Producto")
    print("=====================================================================")

    # a) Agrupar por producto y calcular el % de retraso
    product_stats = (
        df.groupby("product_name")
        .agg(total_pedidos=("order_id", "count"),
             retrasados=("late", "sum"))
        .reset_index()
    )
    product_stats["pct_retraso"] = (product_stats["retrasados"] / product_stats["total_pedidos"]) * 100

    # b) Filtrar por representatividad
    product_stats_filtered = product_stats[product_stats["total_pedidos"] >= MIN_ORDERS_THRESHOLD]

    # c) Seleccionar Top 10 por % retraso
    top10_retraso = product_stats_filtered.sort_values("pct_retraso", ascending=False).head(10)
    
    print(f"Mostrando Top 10 Productos (mínimo {MIN_ORDERS_THRESHOLD} pedidos):")
    print(top10_retraso.to_markdown(index=False, numalign="left", stralign="left"))


    # 5. Conclusión de Negocio
    print("\n=====================================================================")
    print("CONCLUSIÓN DE NEGOCIO")
    print("=====================================================================")
    if not top10_retraso.empty:
        peor_producto = top10_retraso.iloc[0]
        print(f"🔴 Producto con peor rendimiento de entrega: {peor_producto['product_name']}.")
        print(f"   -> Tiene un {peor_producto['pct_retraso']:.2f}% de retrasos sobre {peor_producto['total_pedidos']} pedidos.")
        print("   -> Se debe investigar si el problema es logístico (almacén, transportista) o de inventario.")
    else:
        print("No hay productos con suficientes pedidos (> 20) para analizar el rendimiento de entrega.")

except FileNotFoundError:
    print(f"Error: El archivo '{DATA_FILE}' no se encontró. Asegura que el archivo CSV está en la ubicación correcta.")
except KeyError as e:
    print(f"Error: Una columna necesaria no se encontró. Revisa los nombres de: 'days_for_shipping_real', 'days_for_shipment_scheduled', 'product_name', 'order_id'. Error: {e}")
except Exception as e:
    print(f"Ocurrió un error inesperado durante la ejecución: {e}")