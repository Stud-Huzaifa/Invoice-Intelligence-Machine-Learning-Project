
# load the data
df = load_data_data()

df = apply_labels(df)


#prepare the data 
     X_train,X_test,y_train,y_test = split_date(df,FEATURES,TARGET)
    X_train_scaled,X_test_scaled = scale_features(
        X_train,X_test, 'models/scaler.pkl'

    )

#Train and evaluate models

    grid_search = train_random_forest(X_train_scaled,y_train)

    evaluate_classifier(
        grid_search.best_estimator_,
        X_test_scaled,
        y_test,
        "Random Forest Classifier"

    )

    # save best model
    joblib.dump(grid_search.best_estimaotrs_, "models/predict_flag_invoice.pkl')


if __name__ == "__main__"
    main()