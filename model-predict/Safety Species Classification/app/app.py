from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image

app = Flask(__name__)
model = tf.keras.models.load_model('./models/safety.h5')

@app.route('/api/predict/species', methods=['POST'])
def predict():
    try:
        species = request.files.get('species')
        if not species:
            return jsonify({"error": "File tidak ditemukan!"}), 400

        image = Image.open(species)
        image = image.resize((224, 224))
        image_array = np.array(image) / 255.0
        image_array = np.expand_dims(image_array, axis=0)
        # Prediksi menggunakan model
        predictions = model.predict(image_array)
        # Mendapatkan probabilitas tertinggi
        predicted_class = np.argmax(predictions)
        #0 = Danger, 1 = Safe
        class_labels = ["Danger", "Safe"]
        status = class_labels[predicted_class]
        return jsonify({
            'status': status,
            'predictions': predictions.tolist()
            })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)