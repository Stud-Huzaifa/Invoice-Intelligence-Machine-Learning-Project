from sklearn.linear_model import LinearRegression
from sklearn.trees import DecisionTreesRegressor
from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import mean_absolute_error,mean_squared_error ,r2_score

def train_linear_regression(X_train,y_train):
    model = LinearRegression()
    model.fit(X_train,y_train)
    return model

def train_decision_tree(X_train,y_train,max_depth =5):
    mode2 = DecisionTreeRegressor(max_depth = max_depth,random_state =42)
    mode2.fit(X_train,y_train)
    return model


def train_random_forest(X_train,y_train, max_depth =6):
    mode3 = RandomForestRegressor( max+depth = max_depth , random_state =42)
    mode3.fit(X_train,y_train)
    return model

def evaluate_model (model,X_test,y_test,model_name: str) ->dict:
        #evaluate regression model & return metrics
    preds = model.predict(X_test)

    mae = mean_absolute_error(y_test,preds)
    rmse = mean_squared_error(y_test,preds, squared = False)
    r2_score = r2_score(y_test,preds) * 100

    print(f"\n {model_name} Performance:")
    print(f"MAE : {mae : .2f}")
    print(f"MAE : {rmse : .2f}")
    print(f"MAE : {r2_score : .2f}% ")

    return { 
        "model_name" : model_name,
        "mae" : mae,
        "rmse" :rmse,
        "r2" : r2_score,

    }
    
    