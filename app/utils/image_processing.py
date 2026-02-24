# Fonctions pour le traitement d'images
import cv2
import numpy as np
import tensorflow as tf

MODEL_PATH = 'models/waste_classifier_model.h5'
CLASS_NAMES = ['Plastique', 'Verre', 'Métal', 'Papier', 'Carton', 'Déchet Organique']

model = tf.keras.models.load_model(MODEL_PATH)

def classify_waste(image_path):
    image = cv2.imread(image_path)
    image = cv2.resize(image, (224, 224))
    image = image / 255.0
    image = np.expand_dims(image, axis=0)

    predictions = model.predict(image)
    predicted_class = CLASS_NAMES[np.argmax(predictions)]
    confidence = np.max(predictions) * 100

    return predicted_class, confidence