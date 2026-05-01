import joblib
import pandas as pd
from pathlib import Path
from typing import Union

MODEL_PATH = Path(__file__).resolve().parent.parent / "model" / "freight_model.pkl"


def load_model(model_path: Union[str, Path] = MODEL_PATH):
    """Load the trained freight cost prediction model."""
    model_path = Path(model_path)
    if not model_path.exists():
        raise FileNotFoundError(f"Freight model not found at {model_path}")

    with model_path.open("rb") as f:
        model = joblib.load(f)

    return model


def predict_freight_cost(input_data):
    """Predict freight cost for new vendor invoices."""
    model = load_model()
    input_df = pd.DataFrame(input_data)
    input_df["Predicted_Freight"] = model.predict(input_df).round()
    return input_df


if __name__ == "__main__":
    sample = {"Quantity": [100], "Dollars": [2000.0]}
    print(predict_freight_cost(sample))
