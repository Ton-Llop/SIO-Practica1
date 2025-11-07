import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- CONFIGURACIÓN DE ARCHIVO Y COLUMNAS ---
# Nota: La ruta relativa puede fallar. Se recomienda asegurar que el archivo esté en la raíz de trabajo.
DATA_FILE = "DATA/cadena_subministrament_2015_2018.csv"
QUANTITATIVE_VAR = "benefit_per_order"
CATEGORICAL_VAR = "customer_segment"

try:
    df = pd.read_csv(DATA_FILE) 

    # ======================================================================
    # A. ESTADÍSTICAS DESCRIPTIVAS CONDICIONALES
    # ======================================================================
    
    print("=================================================================")
    print(f"ESTADÍSTICAS CONDICIONALES: '{QUANTITATIVE_VAR}' por '{CATEGORICAL_VAR}'")
    print("=================================================================")

    # Agrupa por segmento y calcula Media, Mediana y Desviación Estándar
    stats_por_segmento = df.groupby(CATEGORICAL_VAR)[QUANTITATIVE_VAR].agg(
        Total_Beneficio='sum',
        Ordenes_Contadas='count',
        Media_Beneficio='mean',
        Mediana_Beneficio='median',
        Desviacion_Estandar='std',
        IQR=lambda x: x.quantile(0.75) - x.quantile(0.25)
    ).sort_values(by='Media_Beneficio', ascending=False)
    
    print(stats_por_segmento)
    print("\n")


    # ======================================================================
    # B. VISUALIZACIÓN: BOXPLOT
    # ======================================================================
    
    print("GENERANDO BOXPLOT para la Distribución de Beneficios por Segmento")
    
    # Usamos el orden basado en la Media (o Mediana) del beneficio
    segment_order = stats_por_segmento.index
    
    plt.figure(figsize=(12, 6)) 
    
    # Generar el Boxplot (análisis bivariado Cuantitativa/Categórica)
    sns.boxplot(x=QUANTITATIVE_VAR, y=CATEGORICAL_VAR, data=df, 
                order=segment_order, palette="viridis")
    
    plt.title('Distribución de Beneficio por Orden por Segmento de Cliente', fontsize=14)
    plt.xlabel('Beneficio por Orden', fontsize=12)
    plt.ylabel('Segmento de Cliente', fontsize=12)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    
    # Guardar y mostrar
    output_filename = "boxplot_benefit_per_order_vs_customer_segment.png"
    plt.tight_layout()
    plt.savefig(output_filename)
    plt.show()
    
    print(f"Gráfico de Boxplot guardado exitosamente: {output_filename}")

except FileNotFoundError:
    print(f"Error: El archivo '{DATA_FILE}' no se encontró. Asegura que el archivo CSV está subido.")
except KeyError as e:
    print(f"Error: La columna {e} no se encuentra. Revisa que las variables '{QUANTITATIVE_VAR}' y '{CATEGORICAL_VAR}' sean correctas.")