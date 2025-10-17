# Documentación para Persona 2: Traductor en Vivo

Este documento describe el funcionamiento y la configuración del script `traductor_en_vivo.py`, diseñado para actuar como el "pegamento" entre el modelo de Machine Learning y la entrada de datos en tiempo real.

## Propósito del Script

El script `traductor_en_vivo.py` tiene dos objetivos principales:

1.  **Simular un flujo de datos en tiempo real:** Por defecto, el script genera datos de sensores aleatorios, los procesa con el modelo de ML (`modelo_predictivo.pkl`) y muestra la predicción en la consola.
2.  **Proporcionar una base para la comunicación real:** Incluye todo el código necesario, aunque comentado, para leer datos desde un puerto serie (simulando una conexión Bluetooth desde un microcontrolador).

## 1. Instalación de Dependencias

Antes de ejecutar el script, asegúrate de tener todas las librerías necesarias. Si ya ejecutaste los scripts de la Persona 1, solo necesitarás `pyserial`. Si no, instala todo con el siguiente comando:

```bash
pip install pandas numpy scikit-learn joblib pyserial
```

## 2. Ejecutar en Modo Simulación (Por defecto)

Este modo te permite probar el flujo completo sin necesidad de hardware externo. El script generará datos falsos y mostrará las predicciones.

**Para ejecutar:**

```bash
python traductor_en_vivo.py
```

Verás una salida similar a esta, actualizándose cada medio segundo:

```
Modelo y codificador cargados correctamente.

--- Iniciando traductor en vivo ---
Presiona Ctrl+C para detener.
Datos simulados: ['0.81', '0.23', '0.95', '0.02', '0.67']
** Predicción: A **

Datos simulados: ['0.45', '0.11', '0.33', '0.88', '0.19']
** Predicción: B **
```

Para detener el script, presiona `Ctrl+C`.

## 3. Habilitar y Configurar el Modo Serial

Este modo está diseñado para recibir datos de un dispositivo externo, como un Arduino o un módulo Bluetooth conectado a un puerto serie.

### Pasos para habilitar:

1.  **Abre el archivo `traductor_en_vivo.py`** en un editor de texto.

2.  **Modifica las variables de configuración** al principio del archivo:
    *   Cambia `MODO_SERIAL = False` a `MODO_SERIAL = True`.
    *   Actualiza `PUERTO_SERIE = 'COM3'` con el nombre correcto de tu puerto.
        *   En **Windows**, será algo como `COM3`, `COM4`, etc.
        *   En **Linux** o **macOS**, será algo como `/dev/ttyUSB0` o `/dev/tty.usbmodem14201`.
    *   Asegúrate de que `BAUD_RATE` coincida con la configuración de tu dispositivo (normalmente 9600).

3.  **Descomenta el código de `pyserial`:** Busca y descomenta todas las líneas que empiezan con `#` y contienen `serial` o `puerto`. Son aproximadamente 10-12 líneas en total, distribuidas en la inicialización, el bucle principal y la sección de limpieza.

### Formato de Datos Esperado

El script espera recibir una cadena de texto a través del puerto serie con el siguiente formato:
*   5 números de punto flotante.
*   Separados por comas.
*   Terminados con un carácter de nueva línea (`\n`).

**Ejemplo de cadena válida:** `0.78,0.21,0.95,0.44,0.12\n`

Una vez configurado, ejecuta el script de la misma manera (`python traductor_en_vivo.py`). Ahora leerá los datos del puerto serie en lugar de simularlos. El manejo de errores básicos está implementado para advertir sobre datos mal formados.