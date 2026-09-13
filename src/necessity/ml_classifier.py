"""
PII Exposure Detection - ML Necessity Classifier (M Component)
Trains classical interpretable models (Ridge, Random Forest) on ordinal target {0.0, 0.5, 1.0}
using multi-modal context features (field_type, document_type, surrounding context window, field value)
with inverse-frequency class weighting to handle minority categories.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, root_mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

LABEL_TO_SCORE: Dict[str, float] = {
    "unnecessary": 0.0,
    "contextual": 0.5,
    "necessary": 1.0,
}


def extract_context_window(text: str, start: int, end: int, window_chars: int = 120) -> str:
    """Extracts text surrounding a span [start, end] for contextual feature representation."""
    if start is None or end is None or not text:
        return ""
    w_start = max(0, start - window_chars)
    w_end = min(len(text), end + window_chars)
    left = text[w_start:start].replace("\n", " ").strip()
    right = text[end:w_end].replace("\n", " ").strip()
    return f"{left} [TARGET] {right}"


class MLNecessityClassifier:
    """ML-based continuous necessity regressor (M component)."""

    def __init__(self, model_type: str = "random_forest", random_state: int = 42):
        self.model_type = model_type
        self.random_state = random_state
        self.pipeline: Optional[Pipeline] = None
        self.is_trained: bool = False

    def _build_pipeline(self) -> Pipeline:
        """Constructs feature extraction and regression pipeline."""
        preprocessor = ColumnTransformer(
            transformers=[
                (
                    "categorical",
                    OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                    ["field_type", "document_type"],
                ),
                (
                    "context_tfidf",
                    TfidfVectorizer(max_features=400, ngram_range=(1, 2), stop_words="english"),
                    "context_text",
                ),
                (
                    "value_tfidf",
                    TfidfVectorizer(max_features=150, ngram_range=(1, 2), stop_words="english"),
                    "field_value",
                ),
            ],
            remainder="drop",
        )

        if self.model_type == "random_forest":
            regressor = RandomForestRegressor(
                n_estimators=120,
                max_depth=14,
                min_samples_split=4,
                random_state=self.random_state,
                n_jobs=-1,
            )
        else:
            regressor = Ridge(alpha=1.0, random_state=self.random_state)

        return Pipeline([
            ("preprocessor", preprocessor),
            ("regressor", regressor),
        ])

    def prepare_dataset(
        self,
        dataset_dir: Union[str, Path],
        split_name: str,
    ) -> Tuple[List[Dict[str, Any]], np.ndarray, np.ndarray]:
        """
        Loads documents for a split and extracts feature dictionaries, targets, and sample weights.
        """
        dataset_path = Path(dataset_dir)
        split_file = dataset_path / "splits" / f"{split_name}.json"

        with open(split_file, "r", encoding="utf-8") as f:
            split_data = json.load(f)

        features: List[Dict[str, Any]] = []
        targets: List[float] = []

        for item in split_data["documents"]:
            doc_id = item["document_id"]
            doc_type = item["document_type"]

            text_path = dataset_path / doc_type / "text" / f"{doc_id}.txt"
            label_path = dataset_path / doc_type / "labels" / f"{doc_id}.json"

            if not (text_path.exists() and label_path.exists()):
                continue

            text_content = text_path.read_text(encoding="utf-8")
            with open(label_path, "r", encoding="utf-8") as lf:
                label_data = json.load(lf)

            for field_entry in label_data.get("fields", []):
                ft = field_entry["field_type"]
                fv = field_entry["field_value"]
                nec_label = field_entry["necessity_label"].lower()
                target_score = LABEL_TO_SCORE.get(nec_label, 0.5)

                span = field_entry.get("span", {})
                start, end = span.get("start", 0), span.get("end", 0)
                context_str = extract_context_window(text_content, start, end)

                features.append({
                    "field_type": ft,
                    "document_type": doc_type,
                    "context_text": context_str,
                    "field_value": str(fv),
                })
                targets.append(target_score)

        y_array = np.array(targets, dtype=np.float32)

        # Compute balanced class weights for training: w_c = N / (3 * N_c)
        classes, counts = np.unique(y_array, return_counts=True)
        total_n = len(y_array)
        class_weight_dict = {c: total_n / (len(classes) * cnt) for c, cnt in zip(classes, counts)}
        sample_weights = np.array([class_weight_dict[val] for val in y_array], dtype=np.float32)

        return features, y_array, sample_weights

    def train(self, train_features: List[Dict[str, Any]], y_train: np.ndarray, sample_weights: np.ndarray) -> None:
        """Fits the pipeline with sample weighting."""
        import pandas as pd
        df = pd.DataFrame(train_features)
        self.pipeline = self._build_pipeline()

        if self.model_type == "random_forest":
            self.pipeline.fit(df, y_train, regressor__sample_weight=sample_weights)
        else:
            self.pipeline.fit(df, y_train, regressor__sample_weight=sample_weights)

        self.is_trained = True

    def predict(self, features: List[Dict[str, Any]]) -> np.ndarray:
        """Predicts continuous necessity scores clamped to [0.0, 1.0]."""
        if not self.is_trained or self.pipeline is None:
            raise RuntimeError("ML model has not been trained yet.")
        import pandas as pd
        df = pd.DataFrame(features)
        preds = self.pipeline.predict(df)
        return np.clip(preds, 0.0, 1.0)

    def evaluate_on_split(
        self,
        features: List[Dict[str, Any]],
        y_true: np.ndarray,
    ) -> Dict[str, float]:
        """Calculates MAE and RMSE against ground truth ordinal targets."""
        preds = self.predict(features)
        mae = float(mean_absolute_error(y_true, preds))
        rmse = float(root_mean_squared_error(y_true, preds))
        return {
            "mae": round(mae, 4),
            "rmse": round(rmse, 4),
        }
