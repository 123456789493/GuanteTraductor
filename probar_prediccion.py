import joblib
import numpy as np
import pandas as pd

# 1. Cargar el modelo y el codificador de etiquetas
try:
    model = joblib.load('modelo_predictivo.pkl')
    le = joblib.load('label_encoder.pkl')
except FileNotFoundError:
    print("Error: 'modelo_predictivo.pkl' o 'label_encoder.pkl' no encontrados.")
    print("Por favor, ejecuta primero 'entrenar_modelo.py' para crear estos archivos.")
    exit()

# 2. Simular una nueva entrada de datos de sensor
# Este dato debería predecir la clase 'A' porque sensor_1 > 0.6 y sensor_3 > 0.6
datos_simulados_A = np.array([[0.7, 0.2, 0.8, 0.5, 0.5]])
# Este dato debería predecir la clase 'B'
datos_simulados_B = np.array([[0.1, 0.2, 0.3, 0.5, 0.6]])

# Convertir a DataFrame para tener los nombres de las columnas, igual que en el entrenamiento
columnas_sensores = ['sensor_1', 'sensor_2', 'sensor_3', 'sensor_4', 'sensor_5']
datos_df_A = pd.DataFrame(datos_simulados_A, columns=columnas_sensores)
datos_df_B = pd.DataFrame(datos_simulados_B, columns=columnas_sensores)

# 3. Predecir la clase para los datos simulados
prediccion_codificada_A = model.predict(datos_df_A)
prediccion_codificada_B = model.predict(datos_df_B)

# 4. Decodificar la predicción para obtener la etiqueta original ('A' o 'B')
prediccion_original_A = le.inverse_transform(prediccion_codificada_A)
prediccion_original_B = le.inverse_transform(prediccion_codificada_B)

# 5. Verificar y mostrar el resultado
print("--- Prueba de Predicción ---")
print(f"Datos de entrada para el caso A: {datos_simulados_A[0]}")
print(f"Predicción del modelo (clase): '{prediccion_original_A[0]}'")
print("-" * 20)
print(f"Datos de entrada para el caso B: {datos_simulados_B[0]}")
print(f"Predicción del modelo (clase): '{prediccion_original_B[0]}'")

# Verificación final
if prediccion_original_A[0] == 'A' and prediccion_original_B[0] == 'B':
    print("\n¡Éxito! El flujo de predicción funciona como se esperaba.")
else:
    print("\nAlerta: La predicción no coincide con el resultado esperado.")