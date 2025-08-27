from __future__ import annotations

import json
import pickle
from pathlib import Path

import matplotlib
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score, roc_curve

# Usar backend "headless" para CI
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ARTIFACTS = Path("artifacts")
ARTIFACTS.mkdir(exist_ok=True)


def train_and_evaluate(n_samples: int = 400, random_state: int = 42) -> dict:
    # Datos sintéticos
    X, y = make_classification(
        n_samples=n_samples,
        n_features=8,
        n_informative=5,
        n_redundant=0,
        random_state=random_state,
    )

    # Modelo
    model = LogisticRegression(max_iter=1_000)
    model.fit(X, y)

    # Predicciones
    y_pred = model.predict(X)
    y_score = model.predict_proba(X)[:, 1]

    # Métricas
    acc = accuracy_score(y, y_pred)
    try:
        roc_auc = roc_auc_score(y, y_score)
    except ValueError:
        roc_auc = None

    # Guardar modelo
    with open(ARTIFACTS / "model.pkl", "wb") as f:
        pickle.dump(model, f)

    # Guardar métricas (mantiene claves esperadas por tests)
    metrics = {
        "accuracy": float(acc),
        "roc_auc": float(roc_auc) if roc_auc is not None else None,
        "n_samples": int(n_samples),
    }
    with open(ARTIFACTS / "metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    # Curva ROC (artefacto adicional)
    fpr, tpr, _ = roc_curve(y, y_score)
    plt.figure()
    label = f"ROC AUC={metrics['roc_auc']:.3f}" if metrics["roc_auc"] else "ROC"
    plt.plot(fpr, tpr, label=label)
    plt.plot([0, 1], [0, 1], linestyle="--")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC curve")
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(ARTIFACTS / "roc_curve.png", dpi=150)
    plt.close()

    return metrics
