from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np
import os  
app = Flask(__name__) 

try:
    model = joblib.load('xgboost_model.pkl')
    print("Modèle chargé avec succès !")
except Exception as e:
    print(f"Erreur lors du chargement du modèle : {e}")
    raise

def predict_price(model, input_data):
    expected_columns = ['ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'log_CRIM', 'log_LSTAT', 'log_DIS']
    input_df = pd.DataFrame([input_data])
    for col in expected_columns:
        if col not in input_df.columns:
            input_df[col] = 0.0
    input_df = input_df[expected_columns]
    try:
        prediction_log = model.predict(input_df)
        return 10 ** prediction_log[0]
    except Exception as e:
        raise ValueError(f"Erreur de prédiction : {e}")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Aucune donnée fournie'}), 400
        prediction = predict_price(model, data)
        return jsonify({'predicted_price': prediction})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))  # Compatible avec Heroku
