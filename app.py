from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf
import pickle
import requests
import os
from google.cloud import firestore
from datetime import datetime

# Pastikan variabel lingkungan Google Application Credentials diatur
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "pedulibumil-2792a-93cce54defcb.json"

# URL publik untuk model TFLite dan scaler (ganti dengan URL Anda)
MODEL_URL = os.getenv("MODEL_URL", "https://storage.googleapis.com/bucket-peduli-bumil/modelml.tflite")
SCALER_URL = os.getenv("SCALER_URL", "https://storage.googleapis.com/bucket-peduli-bumil/scaler.pkl")

# Lokasi sementara untuk menyimpan file yang diunduh
MODEL_PATH = "modelml.tflite"
SCALER_PATH = "scaler.pkl"

# Inisialisasi Flask
app = Flask(__name__)

# Fungsi untuk mengunduh file dari URL
def download_file(url, destination):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(destination, 'wb') as f:
            f.write(response.content)
        print(f"File berhasil diunduh: {destination}")
    else:
        raise Exception(f"Gagal mengunduh file dari {url}. Status code: {response.status_code}")

# Unduh model dan scaler jika belum ada
if not os.path.exists(MODEL_PATH):
    print(f"Mengunduh model dari {MODEL_URL}...")
    download_file(MODEL_URL, MODEL_PATH)

if not os.path.exists(SCALER_PATH):
    print(f"Mengunduh scaler dari {SCALER_URL}...")
    download_file(SCALER_URL, SCALER_PATH)

# Muat model TFLite
interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

# Muat scaler yang telah disimpan
with open(SCALER_PATH, 'rb') as f:
    scaler = pickle.load(f)

# Mendapatkan input dan output details untuk interpreter
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Inisialisasi Firestore
db = firestore.Client()

@app.route("/", methods=["GET"])
def home():
    return "Server Berjalan :)", 200

@app.route("/get", methods=["GET"])
def get_latest_data():
    try:
        # Ambil parameter name dari query
        name = request.args.get("name")
        if not name:
            return jsonify({"error": "Parameter 'name' is required"}), 400

        # Ambil data prediksi terbaru berdasarkan nama
        doc_ref = db.collection("predictions").document(name)
        doc = doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            print("Data ditemukan di Firestore:", data)  # Debug log

            # Cari data terbaru berdasarkan timestamp
            try:
                # Gunakan parsing dengan format yang fleksibel untuk mendukung berbagai format timestamp
                latest_entry = max(data.items(), key=lambda x: datetime.strptime(x[0], "%d/%m/%Y %H:%M"))
            except ValueError as ve:
                try:
                    # Coba format ISO 8601 jika format sebelumnya gagal
                    latest_entry = max(data.items(), key=lambda x: datetime.fromisoformat(x[0]))
                except ValueError as ve2:
                    print("Error dalam parsing timestamp:", ve2)
                    return jsonify({"error": "Invalid timestamp format in Firestore"}), 500

            latest_data = latest_entry[1]
            # Hapus detail `prediction` jika ada
            latest_data.pop("prediction", None)
            return jsonify({
                "timestamp": latest_entry[0],
                "data": latest_data
            }), 200
        else:
            return jsonify({"error": f"No data found for name '{name}'"}), 404

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Pastikan request memiliki data JSON
        data = request.get_json()

        # Validasi input
        if "name" not in data:
            return jsonify({"error": "Field 'name' is required"}), 400
        if "input" not in data or not isinstance(data["input"], list):
            return jsonify({"error": "Field 'input' must be a list"}), 400

        name = data["name"]  # Ambil name dari request
        input_data = np.array(data["input"]).reshape(1, -1)  # Ubah input menjadi array 2D

        # Normalisasi input data
        input_data_scaled = scaler.transform(input_data)

        # Berikan input ke model TFLite
        interpreter.set_tensor(input_details[0]['index'], input_data_scaled.astype(np.float32))

        # Lakukan inferensi
        interpreter.invoke()

        # Ambil hasil output dari model
        output_data = interpreter.get_tensor(output_details[0]['index'])


        # Pastikan urutan label ini sesuai dengan model Anda
        predicted_class_index = np.argmax(output_data)
        risk_category = ['Resiko Tinggi', 'Resiko Rendah', 'Resiko Sedang'][predicted_class_index]


        # Simpan data prediksi ke Firestore
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
        prediction_data = {
            "input": data["input"],
            "risk_category": risk_category
        }
        db.collection("predictions").document(name).set({timestamp: prediction_data})

        return jsonify({
            "risk_category": risk_category
        }), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    # Mendapatkan port dari variabel lingkungan atau default ke 8080
    PORT = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host="0.0.0.0", port=PORT)


