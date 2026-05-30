import numpy as np
import matplotlib.pyplot as plt
import firebase_admin
from firebase_admin import credentials, db
import os
import time
from google.colab import files
from IPython.display import clear_output
import tensorflow as tf

print("📁 Upload your Firebase credentials JSON file (e.g. service-account.json)")
uploaded_cred = files.upload()

cred_filename = None
for filename in uploaded_cred:
    if filename.endswith(".json"):
        cred_filename = filename
        break

if cred_filename is None:
    raise ValueError("Firebase JSON file not uploaded.")

# =============================
# 🔥 Initialize Firebase
# =============================
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(cred_filename)
        firebase_admin.initialize_app(cred, {
            "databaseURL": "https://esp-firebase-389ca-default-rtdb.asia-southeast1.firebasedatabase.app/"
        })
        print("Firebase initialized successfully.")
    except Exception as e:
        print(f"Firebase initialization failed: {e}")

print("📁 Upload your trained ECG model (e.g. ecg_transformer.keras)")
uploaded_model = files.upload()

model_filename = None
for filename in uploaded_model:
    if filename.endswith(".keras"):
        model_filename = filename
        break

if model_filename is None:
    raise ValueError("ECG model file (.keras) not uploaded.")

try:
    model = tf.keras.models.load_model(model_filename)
    print(f"Model '{model_filename}' loaded successfully.")
except Exception as e:
    print(f" Error loading model: {e}")

USER_ID = "c2jJeYcdOAXo2JtToQzP2oPvYer1"
REF_PATH = f"/UsersData/{USER_ID}/ecgReadings"


def fetch_latest_ecg():
    try:
        ecg_readings = db.reference(REF_PATH).get()
        if not ecg_readings:
            return None
        if isinstance(ecg_readings, dict):
            keys = sorted(map(int, ecg_readings.keys()))
            latest_key = keys[-1]
            latest_ecg = ecg_readings[str(latest_key)].get("ecg", [])
            return np.array(latest_ecg, dtype=np.float32) if latest_ecg else None
        return None
    except Exception as e:
        print(f"Error fetching ECG data: {e}")
        return None


def delete_old_ecg_data(keep_last_n=5):
    try:
        ecg_readings = db.reference(REF_PATH).get()
        if isinstance(ecg_readings, dict):
            # Sort by keys assuming they represent timestamps or are sortable strings
            sorted_keys = sorted(ecg_readings.keys())

            if len(sorted_keys) > keep_last_n:
                keys_to_delete = sorted_keys[:-keep_last_n]
                for key in keys_to_delete:
                    db.reference(f"{REF_PATH}/{key}").delete()
                print(f"🗑️ Deleted {len(keys_to_delete)} old ECG entries.")
            else:
                print("✅ No old entries to delete.")
        else:
            print("⚠️ ECG readings format is unexpected.")
    except Exception as e:
        print(f"❌ Error deleting old ECG data: {e}")


CLASS_NAMES = ["APC", "PVC", "Normal", "LBBB", "RBBB"]


def classify_ecg(ecg_signal):
    if ecg_signal is None or model is None:
        return "Unknown"
    try:
        ecg_input = np.expand_dims(ecg_signal, axis=0)
        prediction = model.predict(ecg_input, verbose=0)

        if prediction.shape[-1] > 1:
            class_index = np.argmax(prediction)
            confidence = prediction[0][class_index]
            return f"{CLASS_NAMES[class_index]} ({confidence*100:.1f}%)"
        else:
            class_label = "Normal" if prediction[0][0] < 0.5 else "Abnormal"
            return f"{class_label} ({(1 - prediction[0][0]) * 100:.1f}%)"
    except Exception as e:
        print(f"Classification error: {e}")
        return "Error"


REFRESH_INTERVAL = 5  # seconds
NUM_CYCLES = 10       # Use while True: for continuous loop

for cycle in range(NUM_CYCLES):
    clear_output(wait=True)
    print(f"Refresh Cycle: {cycle + 1}/{NUM_CYCLES}")

    delete_old_ecg_data(keep_last_n=5)

    ecg_signal = fetch_latest_ecg()
    if ecg_signal is not None:
        plt.figure(figsize=(12, 4))
        plt.plot(ecg_signal)
        plt.title("📈 Real-Time ECG Signal")
        plt.xlabel("Time")
        plt.ylabel("Amplitude")
        plt.grid(True)
        plt.show()

        result = classify_ecg(ecg_signal)
        print(f"ECG Classification Result: {result}")
    else:
        print("No ECG data available.")

    time.sleep(REFRESH_INTERVAL)
