# Functions for pre-processing the data
import pandas as pd
import os
import joblib

data_path = model_path = os.path.join('website',  'records.csv')
df = pd.read_csv(data_path)


model_path = os.path.join('website', 'notebooks', 'rf_model.pkl')
model = joblib.load(model_path)

# mapping function
def mapping_cols(df,columns):
        mapping = {'Yes' : 2, 'No':1, 'No internet service': 0, 'No phone service':0}
        for col in columns:
            df[col] = df[col].astype(str)
            df[col] = df[col].str.strip().str.capitalize()
            df[col]=df[col].map(mapping)
        return df
    
    
# get predictions
def get_predictions(customer):
    model_columns = model.feature_names_in_
   #match column names to those in the model
    customer_data = {
    'PhoneService': customer.phone_service,
    'MultipleLines': customer.multiple_lines,
    'OnlineSecurity': customer.online_security,
    'OnlineBackup': customer.online_backup,
    'DeviceProtection': customer.device_protection,
    'TechSupport': customer.tech_support,
    'StreamingTV': customer.streaming_tv,
    'StreamingMovies': customer.streaming_movies,
    'PaperlessBilling': customer.paperless_billing,
    'MonthlyCharges': customer.monthly_charges,
    'TotalCharges': customer.total_charges,
    'PaymentMethod': customer.payment_method,
    'InternetService': customer.internet_service,
    'Contract': customer.contract,
    'tenure':customer.tenure,
    }
    
    df = pd.DataFrame([customer_data])

    final_df = pd.DataFrame(0, index=df.index, columns=model_columns) #matching the number of columns in model and sequence

    #handling the numeric columns
    final_df['tenure'] = df['tenure']
    final_df['MonthlyCharges'] = df['MonthlyCharges']
    final_df['TotalCharges'] = df['TotalCharges']

    #handling columns with values 'Yes', 'No', 'No internet/phone service'
    map_cols=['PhoneService', 'MultipleLines',
       'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport',
       'StreamingTV', 'StreamingMovies','PaperlessBilling']

    df = mapping_cols(df,map_cols)

    # Map the numbers to the final_df
    for col in map_cols:
        final_df[col] = df[col]
  
  
    # mapping the contract  
    contract_mapping = {
        'Month-to-month': 'Contract_Month-to-month',
        'One year': 'Contract_One year',
        'Two year': 'Contract_Two year'
        }
    for contract_type, col_name in contract_mapping.items():
        final_df[col_name] = (df['Contract'] == contract_type).astype(int)
    
    payment_mapping = {
        'Bank transfer': 'PaymentMethod_Bank transfer (automatic)',
        'Credit card': 'PaymentMethod_Credit card (automatic)',
        'Electronic check': 'PaymentMethod_Electronic check',
        'Mailed check': 'PaymentMethod_Mailed check'
        }
    for payment_type, col_name in payment_mapping.items():
        final_df[col_name] = (df['PaymentMethod'] == payment_type).astype(int)

    # Handle InternetService dummy variables
    internet_mapping = {
        'DSL': 'InternetService_DSL',
        'Fiber optic': 'InternetService_Fiber optic',
        'No': 'InternetService_No'
        }
    for service_type, col_name in internet_mapping.items():
        final_df[col_name] = (df['InternetService'] == service_type).astype(int)

    prediction = model.predict(final_df)[0]
    if prediction == 1:
        prediction = 'The customer is likely to churn. Immediate action is recommended'
    else:
        prediction = 'The customer is unlikely to churn. No immediate action is required'
    probability = model.predict_proba(final_df)[0][1]*100
    results = []
    results.append(prediction)
    results.append(probability)
    
    return results






