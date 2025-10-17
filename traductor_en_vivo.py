import joblib
import numpy as np
import pandas as pd
import time
# import serial  # Descomentar para usar el modo Serial

# --- Configuración ---
MODO_SERIAL = False  # Cambiar a True para leer desde el puerto serie
PUERTO_SERIE = 'COM3'  # Reemplazar con tu puerto (ej: '/dev/ttyUSB0' en Linux)
BAUD_RATE = 9600
# ---------------------

def preprocesar_datos(datos_array):
    """Convierte un array de numpy al formato DataFrame esperado por el modelo."""
    columnas_sensores = ['sensor_1', 'sensor_2', 'sensor_3', 'sensor_4', 'sensor_5']
    return pd.DataFrame(datos_array, columns=columnas_sensores)

def main():
    """
    Función principal que carga el modelo y ejecuta el bucle de traducción en vivo.
    """
    # 1. Cargar el modelo y el codificador de etiquetas
    try:
        modelo = joblib.load('modelo_predictivo.pkl')
        le = joblib.load('label_encoder.pkl')
        print("Modelo y codificador cargados correctamente.")
    except FileNotFoundError:
        print("Error: No se encontraron los archivos 'modelo_predictivo.pkl' o 'label_encoder.pkl'.")
        print("Asegúrate de ejecutar 'entrenar_modelo.py' primero.")
        return

    # Inicializar la conexión serial si está en modo serial
    puerto = None
    if MODO_SERIAL:
        # --- Código para la comunicación Serial (Persona 2) ---
        # try:
        #     puerto = serial.Serial(PUERTO_SERIE, BAUD_RATE, timeout=1)
        #     print(f"Escuchando en el puerto serie {PUERTO_SERIE} a {BAUD_RATE} baudios.")
        # except serial.SerialException as e:
        #     print(f"Error al abrir el puerto serie: {e}")
        #     return
        pass # Placeholder

    print("\n--- Iniciando traductor en vivo ---")
    print("Presiona Ctrl+C para detener.")

    # 2. Bucle principal para simulación o lectura en tiempo real
    while True:
        try:
            datos_para_predecir = None

            if MODO_SERIAL:
                # --- Lectura desde Puerto Serie (a implementar por Persona 2) ---
                # if puerto and puerto.in_waiting > 0:
                #     linea = puerto.readline().decode('utf-8').strip()
                #     if linea:
                #         print(f"Dato recibido: {linea}")
                #         try:
                #             valores = [float(v) for v in linea.split(',')]
                #             if len(valores) == 5:
                #                 datos_para_predecir = np.array([valores])
                #             else:
                #                 print("Advertencia: Se recibieron datos con formato incorrecto.")
                #         except ValueError:
                #             print("Advertencia: No se pudo convertir los datos a números.")
                pass # Placeholder
            else:
                # --- Simulación de datos (Modo por defecto) ---
                # 3. Simular la recepción de datos de 5 sensores
                datos_simulados = np.random.rand(1, 5)
                print(f"Datos simulados: {[f'{v:.2f}' for v in datos_simulados[0]]}")
                datos_para_predecir = datos_simulados

            # 4. Preprocesar y predecir si hay datos válidos
            if datos_para_predecir is not None:
                # Darle la forma correcta a los datos para la predicción
                df_datos = preprocesar_datos(datos_para_predecir)

                # 5. Predecir y decodificar
                prediccion_codificada = modelo.predict(df_datos)
                prediccion_final = le.inverse_transform(prediccion_codificada)

                print(f"** Predicción: {prediccion_final[0]} **\n")

                # Opcional: Enviar la predicción de vuelta por el puerto serie
                # if puerto:
                #     puerto.write(f"{prediccion_final[0]}\n".encode('utf-8'))

            # 6. Pausa para simular tasa de muestreo
            time.sleep(0.5)

        except KeyboardInterrupt:
            print("\n--- Deteniendo el traductor ---")
            break
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
            break

    # if puerto and puerto.is_open:
    #     puerto.close()
    #     print("Puerto serie cerrado.")

if __name__ == "__main__":
    main()