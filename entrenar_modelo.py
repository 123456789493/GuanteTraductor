import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import joblib

# 1. Cargar el dataset
try:
    df = pd.read_csv('dataset_prueba.csv')
except FileNotFoundError:
    print("Error: 'dataset_prueba.csv' no encontrado.")
    print("Por favor, ejecuta primero 'generar_datos_falsos.py' para crear el dataset.")
    exit()

# 2. Preparar los datos
# Separar características (X) y etiqueta (y)
X = df.drop('clase', axis=1)
y = df['clase']

# Codificar la etiqueta categórica a numérica
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Dividir los datos en conjuntos de entrenamiento y prueba (80% / 20%)
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# 3. Entrenar y comparar modelos
# Modelo 1: Árbol de Decisión
dt_model = DecisionTreeClassifier(random_state=42)
dt_model.fit(X_train, y_train)
dt_preds = dt_model.predict(X_test)
dt_accuracy = accuracy_score(y_test, dt_preds)
print(f"Precisión del Árbol de Decisión: {dt_accuracy:.4f}")

# Modelo 2: K-Vecinos más Cercanos
knn_model = KNeighborsClassifier()
knn_model.fit(X_train, y_train)
knn_preds = knn_model.predict(X_test)
knn_accuracy = accuracy_score(y_test, knn_preds)
print(f"Precisión de K-Vecinos más Cercanos: {knn_accuracy:.4f}")

# 4. Guardar el mejor modelo
if dt_accuracy >= knn_accuracy:
    best_model = dt_model
    model_name = "Árbol de Decisión"
else:
    best_model = knn_model
    model_name = "K-Vecinos más Cercanos"

# Guardar el modelo y el codificador de etiquetas
joblib.dump(best_model, 'modelo_predictivo.pkl')
joblib.dump(le, 'label_encoder.pkl') # Guardamos el encoder para poder decodificar las predicciones después

print(f"\nEl mejor modelo fue '{model_name}' con una precisión de {max(dt_accuracy, knn_accuracy):.4f}.")
print("Modelo guardado como 'modelo_predictivo.pkl'.")
print("Codificador de etiquetas guardado como 'label_encoder.pkl'.")