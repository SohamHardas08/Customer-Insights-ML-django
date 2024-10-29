# Functions for pre-processing the data
import pandas as pd
import os
import joblib

model_path = os.path.join('website', 'notebooks', 'rf_model.pkl')
model = joblib.load(model_path)

encoder_path = os.path.join('website', 'notebooks', 'onehot_encoder.pkl')
encoder = joblib.load(encoder_path)



def get_predictions(customer):
    customer_data = {
    'tenure':customer.tenure,
    'MonthlyCharges': float(customer.monthly_charges),
    'TotalCharges': float(customer.total_charges),
    'PhoneService': customer.phone_service,
    'MultipleLines': customer.multiple_lines,
    'InternetService': customer.internet_service,
    'OnlineSecurity': customer.online_security,
    'OnlineBackup': customer.online_backup,
    'DeviceProtection': customer.device_protection,
    'TechSupport': customer.tech_support,
    'StreamingTV': customer.streaming_tv,
    'StreamingMovies': customer.streaming_movies,
    'Contract': customer.contract,
    'PaperlessBilling': customer.paperless_billing,
    'PaymentMethod': customer.payment_method,
    }
    
    df = pd.DataFrame([customer_data])
    cat_cols = df.select_dtypes(include = 'object').columns.tolist()
    encoding_data = encoder.transform(df[cat_cols])

    encoding_df = pd.DataFrame(encoding_data, columns=encoder.get_feature_names_out(cat_cols))
    df = df.drop(columns = cat_cols).reset_index(drop=True)
    df = pd.concat([df,encoding_df], axis=1)
    
    prediction = model.predict(df)[0]
    if prediction == 1:
        prediction = 'The customer is likely to churn. Immediate action is recommended'
    else:
        prediction = 'The customer is unlikely to churn. No immediate action is required'
    probability = model.predict_proba(df)[0][1]*100
    results = []
    results.append(prediction)
    results.append(probability)
    
    return results
    
  





