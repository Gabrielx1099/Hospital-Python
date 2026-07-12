import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import classification_report, accuracy_score, f1_score

def entrenar():
    if not os.path.exists('data/sintomas_especialidad.csv'):
        print("❌ Error: No se encontró el dataset en 'data/sintomas_especialidad.csv'. Corre 'generar_dataset_sintomas.py' primero.")
        return

    # Cargar datos
    df = pd.read_csv('data/sintomas_especialidad.csv')
    X = df['texto']
    y = df['especialidad']

    # Dividir en 80/20 train/test estratificado
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    # Vectorizador TF-IDF
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), lowercase=True)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # 1. Regresión Logística
    print("Entrenando Regresión Logística...")
    param_grid_lr = {'C': [0.1, 1.0, 10.0]}
    lr_grid = GridSearchCV(
        LogisticRegression(max_iter=1000, random_state=42),
        param_grid_lr,
        cv=5,
        scoring='f1_macro'
    )
    lr_grid.fit(X_train_vec, y_train)
    best_lr = lr_grid.best_estimator_
    y_pred_lr = best_lr.predict(X_test_vec)
    acc_lr = accuracy_score(y_test, y_pred_lr)
    f1_lr = f1_score(y_test, y_pred_lr, average='macro')
    print(f"-> Logistic Regression: C={lr_grid.best_params_['C']} - Accuracy: {acc_lr:.4f} - F1-macro: {f1_lr:.4f}")

    # 2. Linear SVC
    print("\nEntrenando Linear SVC...")
    param_grid_svc = {'C': [0.1, 1.0, 10.0]}
    svc_grid = GridSearchCV(
        LinearSVC(random_state=42, dual=False),
        param_grid_svc,
        cv=5,
        scoring='f1_macro'
    )
    svc_grid.fit(X_train_vec, y_train)
    best_svc = svc_grid.best_estimator_
    y_pred_svc = best_svc.predict(X_test_vec)
    acc_svc = accuracy_score(y_test, y_pred_svc)
    f1_svc = f1_score(y_test, y_pred_svc, average='macro')
    print(f"-> Linear SVC: C={svc_grid.best_params_['C']} - Accuracy: {acc_svc:.4f} - F1-macro: {f1_svc:.4f}")

    # Comparar modelos
    if f1_svc >= f1_lr:
        print("\n🏆 Ganador: Linear SVC")
        # Calibrar Linear SVC para obtener probabilidades (predict_proba)
        # Usamos cv=5 para calibrar con validación cruzada y evitar sobreajuste
        winner_model = CalibratedClassifierCV(
            estimator=LinearSVC(C=best_svc.C, random_state=42, dual=False),
            cv=5
        )
        winner_model.fit(X_train_vec, y_train)
        winner_name = f"LinearSVC (C={best_svc.C})"
    else:
        print("\n🏆 Ganador: Regresión Logística")
        winner_model = best_lr
        winner_name = f"LogisticRegression (C={best_lr.C})"

    # Evaluar ganador final
    y_pred_winner = winner_model.predict(X_test_vec)
    final_acc = accuracy_score(y_test, y_pred_winner)
    final_f1 = f1_score(y_test, y_pred_winner, average='macro')

    print("\n=== Reporte de Clasificación (Modelo Ganador) ===")
    print(classification_report(y_test, y_pred_winner))

    # Guardar modelo y vectorizador
    os.makedirs('models', exist_ok=True)
    joblib.dump(winner_model, 'models/modelo_sintomas.pkl')
    joblib.dump(vectorizer, 'models/vectorizer_sintomas.pkl')

    print(f"\nMejor modelo: {winner_name} — Accuracy: {final_acc:.4f} — F1-macro: {final_f1:.4f}")
    print("Artefactos guardados exitosamente en 'models/'.")

if __name__ == '__main__':
    entrenar()
