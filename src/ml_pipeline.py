"""
Pipeline ML pour la prédiction de réachat.

Split temporel
Assemblage features
Entraînement
Evaluation

La dernière commande de chaque user sert de test set, et non de split aléatoire.
"""
from __future__ import annotations

import pandas as pd
import numpy as np
import time
from dataclasses import dataclass, field
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix
)
from src.ml_features import build_all_features

# Colonnes exclues de l'entraînement

_ID_COLS = {"user_id", "product_id", "reordered", "order_id", "order_number"}

@dataclass
class ReorderPipeline:
    """Pipeline complet de prédiction de réachat.
    
    split > features > train
    """
    
    data: pd.DataFrame
    sample_frac: float = 1.0
    random_state: int = 42
    
    # Attributs
    train_raw_: pd.DataFrame | None = field(default=None, repr=False)
    test_raw_: pd.DataFrame | None = field(default=None, repr=False)
    X_train_: pd.DataFrame | None = field(default=None, repr=False)
    X_test_: pd.DataFrame | None = field(default=None, repr=False)
    y_train_: pd.Series | None = field(default=None, repr=False)
    y_test_: pd.Series | None = field(default=None, repr=False)
    feature_cols_: list | None = field(default=None, repr=False)
    results_: dict = field(default_factory=dict, repr=False)
    
    
    # ETAPE 1: Split temporel
    def split(self) -> "ReorderPipeline":
        """Split temporel : dernière commande de chaque user = test."""
        print("ETAPE 1 : Split temporel")
        last = self.data.groupby("user_id")["order_number"].max().reset_index(name="_last")
        merged = self.data.merge(last, on="user_id")

        self.train_raw_ = merged[merged["order_number"] < merged["_last"]].drop(columns=["_last"])
        self.test_raw_ = merged[merged["order_number"] == merged["_last"]].drop(columns=["_last"])

        print(f"  Train : {self.train_raw_.shape[0]:,} lignes")
        print(f"  Test  : {self.test_raw_.shape[0]:,} lignes")
        return self
        
    # ETAPE 2: Features + assemblage
    
    def build_features(self) -> "ReorderPipeline":
        """Calcule les features sur le train, assemble train et test sets."""
        assert self.train_raw_ is not None and self.test_raw_ is not None, \
            "Appeler .split() avant .build_features()"
        print("\nETAPE 2: FEature engineering")
        user_feat, prod_feat, up_feat = build_all_features(self.train_raw_)

        # Assemblage
        test_set = self._assemble(self.test_raw_, user_feat, prod_feat, up_feat)
        train_set = self._assemble(self.train_raw_, user_feat, prod_feat, up_feat)

        # Échantillonnage optionnel
        if self.sample_frac < 1.0:
            train_set = train_set.sample(frac=self.sample_frac, random_state=self.random_state)
            print(f"  Échantillonnage → {len(train_set):,} lignes ({self.sample_frac:.0%})")

        # Séparation X / y
        self.feature_cols_ = [c for c in train_set.columns if c not in _ID_COLS]
        self.X_train_, self.y_train_ = train_set[self.feature_cols_], train_set["reordered"]
        self.X_test_, self.y_test_ = test_set[self.feature_cols_], test_set["reordered"]

        print(f"  Train : {self.X_train_.shape[0]:,} × {len(self.feature_cols_)} features")
        print(f"  Test  : {self.X_test_.shape[0]:,} × {len(self.feature_cols_)} features")
        return self

    # ETAPE 3: Entraînement + évaluation

    def train_and_evaluate(self, models: dict | None = None) -> pd.DataFrame:
        """Entraîne plusieurs modèles et retourne un tableau comparatif"""
        assert (self.X_train_ is not None and self.y_train_ is not None
                and self.X_test_ is not None and self.y_test_ is not None), \
            "Appeler .build_features() avant .train_and_evaluate()"
        if models is None:
            models = self._default_models()

        print("\nETAPE 3: Entraînement du model")
        rows = []
        for name, model in models.items():
            t0 = time.time()
            model.fit(self.X_train_, self.y_train_)
            elapsed = time.time() - t0

            y_pred = model.predict(self.X_test_)
            y_proba = (model.predict_proba(self.X_test_)[:, 1]
                       if hasattr(model, "predict_proba") else y_pred.astype(float))

            m = {
                "model": name,
                "accuracy": accuracy_score(self.y_test_, y_pred),
                "precision": precision_score(self.y_test_, y_pred, zero_division=0),
                "recall": recall_score(self.y_test_, y_pred, zero_division=0),
                "f1": f1_score(self.y_test_, y_pred, zero_division=0),
                "roc_auc": roc_auc_score(self.y_test_, y_proba),
                "train_time_s": round(elapsed, 1),
            }
            self.results_[name] = {"model": model, "y_pred": y_pred, "y_proba": y_proba}
            rows.append(m)
            print(f"  [{name}] F1={m['f1']:.4f}  AUC={m['roc_auc']:.4f}  ({elapsed:.1f}s)")

        self.results_df_ = pd.DataFrame(rows).set_index("model")
        return self.results_df_

    # Utilitaires

    def get_feature_importance(self, model_name: str) -> pd.DataFrame:
        assert self.feature_cols_ is not None, "Appeler .build_features() d'abord"
        model = self.results_[model_name]["model"]
        imp = model.feature_importances_ if hasattr(model, "feature_importances_") else np.abs(model.coef_[0])
        return (pd.DataFrame({"feature": self.feature_cols_, "importance": imp})
                .sort_values("importance", ascending=False).reset_index(drop=True))

    def get_classification_report(self, model_name: str) -> str:
        assert self.y_test_ is not None, "Appeler .build_features() d'abord"
        report = classification_report(
            self.y_test_, self.results_[model_name]["y_pred"],
            target_names=["Nouveau", "Réacheté"], output_dict=False,
        )
        return str(report)

    def get_confusion_matrix(self, model_name: str) -> np.ndarray:
        assert self.y_test_ is not None, "Appeler .build_features() d'abord"
        return confusion_matrix(self.y_test_, self.results_[model_name]["y_pred"])

    # Privé

    def _assemble(
        self, raw: pd.DataFrame, user_feat: pd.DataFrame,
        prod_feat: pd.DataFrame, up_feat: pd.DataFrame,
    ) -> pd.DataFrame:
        out = raw[["user_id", "product_id", "reordered"]].copy()
        out = out.merge(user_feat, on="user_id", how="left")
        out = out.merge(prod_feat, on="product_id", how="left")
        out = out.merge(up_feat, on=["user_id", "product_id"], how="left")
        return out.fillna(0)

    def _default_models(self) -> dict:
        models = {
            "LogisticRegression": LogisticRegression(max_iter=500, random_state=self.random_state, n_jobs=-1),
            "RandomForest": RandomForestClassifier(
                n_estimators=200, max_depth=12, min_samples_leaf=50,
                random_state=self.random_state, n_jobs=-1,
            ),
        }
        try:
            import lightgbm as lgb
            models["LightGBM"] = lgb.LGBMClassifier(
                n_estimators=300, max_depth=8, learning_rate=0.05,
                num_leaves=63, min_child_samples=100,
                random_state=self.random_state, n_jobs=-1, verbose=-1,
            )
        except ImportError:
            print("  LightGBM non installé! Ignoré")
        return models