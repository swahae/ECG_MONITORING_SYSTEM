# ❤️ ECG Monitoring and Classification System

A real-time IoT-based ECG Monitoring System that acquires ECG signals using an AD8232 sensor and ESP8266, stores data in Firebase Realtime Database, visualizes ECG waveforms, and classifies heart conditions using a Deep Learning model.

---

## 📋 Project Description

This project combines IoT, Cloud Computing, and Artificial Intelligence to monitor ECG signals in real time.

The ESP8266 reads ECG signals from the AD8232 sensor and uploads them to Firebase Realtime Database. A Python application continuously retrieves the latest ECG data, displays the waveform, and uses a trained TensorFlow/Keras model to classify the ECG signal into different cardiac conditions.

---

## 🚀 Features

* Real-time ECG signal acquisition
* Wireless data transmission via Wi-Fi
* Firebase Realtime Database integration
* Live ECG waveform visualization
* Deep Learning based ECG classification
* Automatic database maintenance
* Easy deployment using ESP8266 NodeMCU

---

## 🛠 Hardware Requirements

* ESP8266 NodeMCU
* AD8232 ECG Sensor Module
* ECG Electrodes
* Jumper Wires
* USB Cable
* Computer/Laptop

---

## 💻 Software Requirements

### Arduino IDE Libraries

```text
ESP8266WiFi
FirebaseESP8266
```

### Python Libraries

```bash
pip install numpy
pip install matplotlib
pip install firebase-admin
pip install tensorflow
pip install google-colab
```

---

## 📂 Project Structure

```text
ECG-Monitoring-System/
│
├── ESP8266_ECG.ino
│   ├── Connects to Wi-Fi
│   ├── Reads ECG values
│   ├── Uploads ECG data to Firebase
│   └── Handles lead-off detection
│
├── ecg_monitor.py
│   ├── Connects to Firebase
│   ├── Fetches ECG readings
│   ├── Displays ECG graph
│   ├── Loads trained model
│   └── Predicts ECG class
│
├── ecg_transformer.keras
│   └── Trained Deep Learning Model
│
├── firebase_credentials.json
│   └── Firebase Service Account Key
│
└── README.md
```

---

## ⚙️ Working Flow

```text
AD8232 Sensor
      │
      ▼
ESP8266 NodeMCU
      │
      ▼
Firebase Realtime Database
      │
      ▼
Python Monitoring Application
      │
      ▼
TensorFlow Model
      │
      ▼
ECG Classification Result
```

---

## 🧠 ECG Classification Classes

| Class  | Description                       |
| ------ | --------------------------------- |
| APC    | Atrial Premature Contraction      |
| PVC    | Premature Ventricular Contraction |
| Normal | Normal Heartbeat                  |
| LBBB   | Left Bundle Branch Block          |
| RBBB   | Right Bundle Branch Block         |

---

## 🔥 Firebase Database Structure

```json
{
  "UsersData": {
    "USER_UID": {
      "ecgReadings": {
        "timestamp": {
          "ecg": [512, 514, 520, 518]
        }
      }
    }
  }
}
```

---

## ▶️ How to Run

### Step 1: Upload ESP8266 Code

1. Open Arduino IDE
2. Install required libraries
3. Update Wi-Fi and Firebase credentials
4. Upload code to ESP8266

### Step 2: Configure Firebase

1. Create Firebase Project
2. Enable Realtime Database
3. Download Service Account JSON file
4. Update database URL

### Step 3: Run Python Program

```bash
python ecg_monitor.py
```

or run the notebook in Google Colab.

---

## 📈 Sample Output

```text
Refresh Cycle: 1/10

ECG Classification Result:
Normal (98.7%)
```

---
<img width="1500" height="844" alt="WhatsApp Image 2026-05-30 at 7 02 24 PM" src="https://github.com/user-attachments/assets/2a5811b7-36e6-4385-be81-3e4399207646" />


## 🎯 Applications

* Remote Patient Monitoring
* Telemedicine
* Healthcare IoT Systems
* Cardiac Health Tracking
* Educational and Research Projects

---


## 🏆 Technologies Used

* ESP8266 NodeMCU
* AD8232 ECG Sensor
* Firebase Realtime Database
* Python
* TensorFlow/Keras
* NumPy
* Matplotlib
* Google Colab

---


