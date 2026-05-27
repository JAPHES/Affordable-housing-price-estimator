from functools import lru_cache
from pathlib import Path
import warnings

import joblib
import numpy as np
from django.conf import settings


MODEL_PATH = Path(settings.BASE_DIR) / "affordable_price_model.pkl"
FALLBACK_FEATURE_NAMES = [
    "financing_cost_ksh",
    "construction_cost_ksh",
    "markup_ksh",
    "monthly_repayment_ksh",
    "size_sqm",
    "cost_per_sqm_ksh",
    "interest_rate_pct",
    "housing_levy_contribution_ksh",
    "buyer_monthly_income_ksh",
]


@lru_cache(maxsize=1)
def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
    return joblib.load(MODEL_PATH)


def get_feature_names():
    model = load_model()
    feature_names = getattr(model, "feature_names_in_", None)
    if feature_names is None:
        return FALLBACK_FEATURE_NAMES
    return list(feature_names)


def predict_price(values):
    feature_names = get_feature_names()
    row = [float(values[name]) for name in feature_names]
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="X does not have valid feature names")
        prediction = load_model().predict(np.array([row]))[0]
    return max(0, float(prediction))
