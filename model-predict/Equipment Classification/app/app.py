from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)
model = tf.keras.models.load_model('./models/equipments.h5')

credit = credentials.Certificate('./serviceAccountKey.json')
firebase_admin.initialize_app(credit)
db = firestore.client()

def save_to_firestore(predict_equipment, status):
    flattened_predictions = [float(pred) for pred in predict_equipment[0]]
    # Simpan ke Firestore
    doc_ref = db.collection('predict_equipment').add({
        'predictions': flattened_predictions,
        'status': status,
        'timestamp': firestore.SERVER_TIMESTAMP
    })
    print("Prediksi berhasil disimpan ke Firestore")


# Endpoint untuk menerima data dan mengembalikan prediksi
@app.route('/api/predict/equipments', methods=['POST'])
def predict():
    try:
        # input request
        file = request.files.get('file')  # Mengambil file gambar

        if not file:
            return jsonify({"error": "File tidak ditemukan!"}), 400

        # Membaca dan memproses gambar
        image = Image.open(file)
        image = image.resize((224, 224))
        image_array = np.array(image) / 255.0
        image_array = np.expand_dims(image_array, axis=0)

        # Prediksi menggunakan model
        predictions = model.predict(image_array)
        predicted_class = np.argmax(predictions)
        predictions_list = predictions.tolist()

        class_labels = ['Diving Fins', 'Diving Mask', 'Diving Oxygen Tank', 'Diving Regulators', 'Diving Wetsuit']
        status = class_labels[predicted_class]

        # Menyimpan ke Firestore
        save_to_firestore(predictions_list, status)

        # Kirim hasil prediksi
        return jsonify({
            'predictions': predictions.tolist(),
            'status': status
            })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
