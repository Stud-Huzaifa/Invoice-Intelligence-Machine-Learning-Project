import joblib 
import pandas as pd

MODEL_PATH ="model/predict_freight_model.pkl"

def load_model(model_path : str = MODEL_PATH):
    """
    load trained freight cost prediction model,
    """

    with open(model_path,"rb") as f:
        model = joblib.load(f)

    return model


def predict_freight_cost(input_data):

    """"
        Predict freight cost for new vendor invoices,

    parameters 
    ----------
    input_data : dict

    returns
    -------

     pd.dataframe with predicted freight cost
     ------

     """"
 model = load_model()
    input_df = pd.DataFrame(input_data)
    input_df['Predicted_Freight'] = model.predict(input_df).round()
    return input_df

if __name__ == "__main__":
              