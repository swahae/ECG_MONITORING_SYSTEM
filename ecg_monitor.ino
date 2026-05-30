#include <ESP8266WiFi.h>
#include <FirebaseESP8266.h>

// WiFi credentials
#define WIFI_SSID "Varsh"
#define WIFI_PASS "varshini"

// Firebase credentials
#define FIREBASE_KEY "AIzaSyB49ftZvxsrwNZ8_dBv1yhRxPnTWgQdCFY"
#define FIREBASE_EMAIL "varshiniashok473@gmail.com"
#define FIREBASE_PASS "coriander"
#define DB_URL "https://esp-firebase-389ca-default-rtdb.asia-southeast1.firebasedatabase.app/"


#define ECG_PIN A0
#define LO_P D5
#define LO_M D6


const int BUF_SIZE = 100;
int buf[BUF_SIZE];
int idx = 0;
unsigned long lastTime = 0;
const unsigned long INTERVAL = 1000;  // Microseconds (adjust as needed)

// Firebase objects
FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;
String path;

void setup() {
  Serial.begin(115200);
  Serial.println("\nStarting ECG Monitoring System");

  // Connect to Wi-Fi
  Serial.print("Connecting to ");
  Serial.print(WIFI_SSID);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println("\nWiFi connected!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  // Setup Firebase config
  config.api_key = FIREBASE_KEY;
  config.database_url = DB_URL;

  auth.user.email = FIREBASE_EMAIL;
  auth.user.password = FIREBASE_PASS;

  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);

  while (!Firebase.ready()) {
    Serial.print(".");
    delay(500);
  }
  Serial.println("\nFirebase connected!");
  Serial.print("User UID: ");
  Serial.println(auth.token.uid.c_str());

  // Set base Firebase path
  path = "/UsersData/" + String(auth.token.uid.c_str()) + "/ecgReadings";
  Serial.print("Database path: ");
  Serial.println(path);

  // ECG hardware setup
  pinMode(LO_P, INPUT);
  pinMode(LO_M, INPUT);
  Serial.println("System Ready!\n");
}

void loop() {
  if (micros() - lastTime < INTERVAL) return;
  lastTime = micros();

  // Lead-off detection
  if (digitalRead(LO_P) && digitalRead(LO_M)) {
    if (idx != 0) Serial.println("Leads Off! Resetting buffer.");
    idx = 0;
    return;
  }

  // Sample collection
  buf[idx++] = analogRead(ECG_PIN);
  if (idx % 10 == 0) Serial.print(".");  // Progress indicator

  if (idx < BUF_SIZE) return;

  // Prepare data for Firebase
  Serial.print("\nCollected ");
  Serial.print(BUF_SIZE);
  Serial.println(" samples. Sending to Firebase...");

  FirebaseJson json;
  FirebaseJsonArray arr;

  for (int i = 0; i < BUF_SIZE; i++) {
    arr.add(buf[i]);
  }

  json.set("ecg", arr);

  // Upload to Firebase
  if (Firebase.setJSON(fbdo, (path + "/" + millis()).c_str(), json)) {
    Serial.println("Upload successful!");
    Serial.print("Payload size: ");
    Serial.print(fbdo.payloadLength());
    Serial.println(" bytes");
  } else {
    Serial.println("Firebase Error:");
    Serial.println(fbdo.errorReason());
  }

  idx = 0;
  Serial.println("Waiting for new samples...\n");
}