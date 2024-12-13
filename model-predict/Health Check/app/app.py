from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np

app = Flask(__name__)
model = tf.keras.models.load_model('./models/model_HealthCheck.h5')

@app.route('/api/predict/healthcheck', methods=['POST'])
def predict():
    try:
        # input request (dalam format JSON)
        data = request.get_json()
        required_fields = [
            'Masalah Pernafasan/Jantung/Covid', 'Umur > 45 Tahun', 
            'Tidak Dapat Olahraga Ringan', 'Masalah Mata/Telinga/Sinus', 
            'Operasi Terakhir 12 Bulan', 'Masalah Neurologis', 
            'Perawatan Psikologis', 'Masalah Punggung/Diabetes', 
            'Masalah Perut/Usus', 'Mengonsumsi Obat'
        ]

        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Field '{field}' diperlukan"}), 400

        input_data = np.array([[
            data['Masalah Pernafasan/Jantung/Covid'],
            data['Umur > 45 Tahun'],
            data['Tidak Dapat Olahraga Ringan'],
            data['Masalah Mata/Telinga/Sinus'],
            data['Operasi Terakhir 12 Bulan'],
            data['Masalah Neurologis'],
            data['Perawatan Psikologis'],
            data['Masalah Punggung/Diabetes'],
            data['Masalah Perut/Usus'],
            data['Mengonsumsi Obat']
        ]])

        input_data = input_data / np.max(input_data)
        predictions = model.predict(input_data)
        status = "Siap diving" if predictions[0] > 0.5 else "Tidak"

        return jsonify({'status': status})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
