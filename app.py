from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load the pre-trained pipeline (with data preprocessing and Random Forest model)
with open('random_forest_model(3).pkl', 'rb') as f:
    model_pipeline = pickle.load(f)

# Define class mapping (assuming the model outputs 0, 1, 2)
class_mapping = {0: 'Good', 1: 'Standard', 2: 'Poor'}

@app.route('/')
def index():
    # Render the main form page
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract JSON data from request
        data = request.get_json()

        # Convert JSON to DataFrame for the model
        input_data = pd.DataFrame([data])

        # One-hot encode categorical variables (extend this list based on your model)
        categorical_columns = ['Payment_of_Min_Amount', 'Credit_Mix', 'Type_of_Loan']  # Include all categorical features here
        input_data = pd.get_dummies(input_data, columns=categorical_columns, drop_first=True)

        # Ensure that input_data has the same columns as expected by the model
        input_data = input_data.reindex(columns=model_pipeline.feature_names_in_, fill_value=0)

        # Check for missing features
        missing_features = set(model_pipeline.feature_names_in_) - set(input_data.columns)
        if missing_features:
            return jsonify({'error': f'Missing features: {missing_features}'})

        # Make prediction
        prediction = model_pipeline.predict(input_data)[0]  # Single prediction
        prediction_proba = model_pipeline.predict_proba(input_data)[0]  # Probabilities

        # Map the predicted class to its label (Good, Standard, Poor)
        predicted_class = class_mapping.get(prediction, 'Unknown')

        # Prepare the result with probabilities mapped to class labels
        proba_with_labels = {class_mapping[i]: round(prob, 4) for i, prob in enumerate(prediction_proba)}

        return jsonify({
            'prediction': predicted_class,
            'probability': proba_with_labels
        })

    except Exception as e:
        # Log error for debugging
        print(f"Error occurred: {e}")
        # Return error message in case something goes wrong
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)  # Turn off debug mode in production
