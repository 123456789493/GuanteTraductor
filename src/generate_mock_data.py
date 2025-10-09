# Dentro de src/generate_mock_data.py

import pandas as pd
import numpy as np
import os

# --- Configuración ---
SAMPLES_PER_GESTURE = 100  # Número de muestras a generar por cada gesto
NOISE_LEVEL = 25           # Nivel de variación o "ruido" para que los datos parezcan reales
OUTPUT_PATH = 'data/raw/'  # Carpeta donde se guardará el archivo
FILE_NAME = 'mock_data.csv'

# --- Definición de los Perfiles de Gestos ---
# Cada lista representa los valores base de los 5 sensores para un gesto.
# Formato: [pulgar, indice, medio, anular, meñique]
gesture_profiles = {
    'fist': [800, 810, 820, 805, 790],
    'open_hand': [200, 190, 210, 205, 215],
    'pointing_index': [750, 220, 790, 780, 770]
}

# --- Generación de Datos ---
all_data = []

print("Generando datos de prueba...")

# Bucle a través de cada gesto definido
for label, base_values in gesture_profiles.items():
    print(f"  - Generando {SAMPLES_PER_GESTURE} muestras para el gesto: '{label}'")
    for _ in range(SAMPLES_PER_GESTURE):
        # Añade ruido aleatorio a los valores base
        noise = np.random.randint(-NOISE_LEVEL, NOISE_LEVEL, size=len(base_values))
        noisy_values = np.array(base_values) + noise
        
        # Añade el label (nombre del gesto) al final de la fila
        row = list(noisy_values)
        row.append(label)
        all_data.append(row)

# --- Creación del DataFrame y Guardado ---
# Define los nombres de las columnas
columns = ['sensor_1', 'sensor_2', 'sensor_3', 'sensor_4', 'sensor_5', 'label']

# Crea el DataFrame con pandas
df = pd.DataFrame(all_data, columns=columns)

# Mezcla los datos de forma aleatoria para que no estén ordenados por gesto
df = df.sample(frac=1).reset_index(drop=True)

# Asegúrate de que la carpeta de salida exista
os.makedirs(OUTPUT_PATH, exist_ok=True)
full_path = os.path.join(OUTPUT_PATH, FILE_NAME)

# Guarda el DataFrame en un archivo CSV
df.to_csv(full_path, index=False)

print(f"\n¡Éxito! Se generaron {len(df)} filas de datos.")
print(f"El archivo fue guardado en: {full_path}")