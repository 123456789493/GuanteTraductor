import pandas as pd
import numpy as np

def generar_datos(num_filas=5000):
    """
    Genera un dataset de prueba con datos de 5 sensores y una clase de salida.

    Args:
        num_filas (int): El número de filas (muestras) a generar.

    Returns:
        pd.DataFrame: Un DataFrame de pandas con los datos generados.
    """
    # 1. Definir Sensores y generar datos aleatorios
    datos = {
        'sensor_1': np.random.rand(num_filas),
        'sensor_2': np.random.rand(num_filas),
        'sensor_3': np.random.rand(num_filas),
        'sensor_4': np.random.rand(num_filas),
        'sensor_5': np.random.rand(num_filas),
    }
    df = pd.DataFrame(datos)

    # 2. Generar Etiqueta (Target) basada en una lógica
    condicion_A = ((df['sensor_1'] > 0.6) & (df['sensor_3'] > 0.6)) | \
                  ((df['sensor_4'] < 0.4) & (df['sensor_5'] < 0.4))

    df['clase'] = np.where(condicion_A, 'A', 'B')

    return df

if __name__ == "__main__":
    # 3. Guardar el DataFrame en un archivo CSV
    dataset = generar_datos(num_filas=5000)
    dataset.to_csv('dataset_prueba.csv', index=False)
    print("Dataset de prueba 'dataset_prueba.csv' generado con éxito con 5000 filas.")