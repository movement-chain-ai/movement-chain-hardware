// EMG Sensor - 1000 Hz Sampling Rate
// Movement Chain Golf Swing Analysis
//
// Wiring:
//   EMG VCC → Arduino 5V (or 3.3V if signal saturates)
//   EMG GND → Arduino GND
//   EMG SIG → Arduino A0
//
// Sampling rate: 1000 Hz (1 sample per millisecond)

// ============== CONFIGURATION ==============
const int EMG_PIN = A0;           // Analog pin for EMG sensor
const int SAMPLE_DELAY_MS = 1;    // 1ms delay = 1000 Hz sampling rate
const long BAUD_RATE = 115200;    // Serial baud rate
// ===========================================

void setup() {
  Serial.begin(BAUD_RATE);
  pinMode(EMG_PIN, INPUT);
}

void loop() {
  int rawValue = analogRead(EMG_PIN);
  Serial.println(rawValue);
  delay(SAMPLE_DELAY_MS);
}
