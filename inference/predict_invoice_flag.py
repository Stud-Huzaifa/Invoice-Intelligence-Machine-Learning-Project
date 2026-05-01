import joblib
import pandas as pd
from pathlib import Path
from typing import Union

MODEL_PATH = Path(__file__).resolve().parent.parent / "model" / "invoice_flag_model.pkl"


def load_model(model_path: Union[str, Path] = MODEL_PATH):
    """Load the trained invoice flagging model."""
    model_path = Path(model_path)
    if not model_path.exists():
        raise FileNotFoundError(f"Invoice flag model not found at {model_path}")

    with model_path.open("rb") as f:
        model = joblib.load(f)

    return model


def predict_invoice_flag(input_data):
    """Predict whether a vendor invoice should be flagged for manual approval."""
    model = load_model()
    input_df = pd.DataFrame(input_data)
    input_df["Predicted_Flag"] = model.predict(input_df).round()
    return input_df


if __name__ == "__main__":
    sample = {
        "invoice_quantity": [50],
        "invoice_dollars": [1000.0],
        "Freight": [20.0],
        "total_item_quantity": [50],
        "total_item_dollars": [3000.0],
        "avg_receiving_delay": [3.0],
    }
    print(predict_invoice_flag(sample))
