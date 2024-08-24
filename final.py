import os
import sys
import json
import joblib
import numpy as np

base_path = os.path.dirname(__file__)  # Get the directory of the current script

def predict_disease_from_symptoms(symptom_vector, confidence_threshold=0.5):
    """
    Predict the disease given a symptom vector, only if confidence is 80% or higher.
    
    Parameters:
    - symptom_vector: A list of binary values representing the presence/absence of symptoms.
    - confidence_threshold: Minimum confidence level to print the disease (default is 0.8 or 80%).
    
    Returns:
    - predicted_disease: The name of the predicted disease if confidence is above the threshold, 
                         otherwise a message indicating low confidence.
    """
    # Load the model and encoder
    model_path = os.path.join(base_path, 'disease_prediction_model.joblib')
    encoder_path = os.path.join(base_path, 'label_encoder.joblib')    
    loaded_model = joblib.load(model_path)
    loaded_encoder = joblib.load(encoder_path)
    
    # Predict the probabilities of each disease
    symptom_vector = np.array(symptom_vector).reshape(1, -1)
    probabilities = loaded_model.predict_proba(symptom_vector)[0]
    
    # Get the highest probability and the corresponding disease
    max_prob = np.max(probabilities)
    predicted_index = np.argmax(probabilities)
    
    predicted_disease = loaded_encoder.inverse_transform([predicted_index])[0]
    return [predicted_disease, '%.2f' % max_prob]
    # if max_prob >= confidence_threshold:
    #     predicted_disease = loaded_encoder.inverse_transform([predicted_index])[0]
    #     # Decode the prediction to get the disease name
    #     return f"Predicted Disease: {predicted_disease} with confidence {100 * max_prob:.2f}%"
    # else:
    #     return f"Prediction confidence ({max_prob:.2f}) is below the threshold of {confidence_threshold * 100}%."
    
print(json.dumps(predict_disease_from_symptoms(json.loads(sys.argv[1]))))

# example_symptoms = [0] * (data.shape[1] - 1)
# Replace with actual symptoms
# predicted_disease = predict_disease_from_symptoms(example_symptoms)
# print(predicted_disease)

