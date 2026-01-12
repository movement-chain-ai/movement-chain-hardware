// I2C Scanner - Find connected I2C devices
// Upload this to check if MPU6050 is detected
//
// Expected output if MPU6050 is connected correctly:
//   "I2C device found at address 0x68" (or 0x69)
//
// If you see "No I2C devices found" = wiring problem!

#include <Wire.h>

void setup() {
  Wire.begin();
  Serial.begin(115200);
  while (!Serial);

  Serial.println();
  Serial.println("=================================");
  Serial.println("  I2C Scanner - Movement Chain");
  Serial.println("=================================");
  Serial.println();
  Serial.println("Scanning for I2C devices...");
  Serial.println();
}

void loop() {
  byte error, address;
  int deviceCount = 0;

  for (address = 1; address < 127; address++) {
    Wire.beginTransmission(address);
    error = Wire.endTransmission();

    if (error == 0) {
      Serial.print("  I2C device found at address 0x");
      if (address < 16) Serial.print("0");
      Serial.print(address, HEX);

      // Identify common devices
      if (address == 0x68) Serial.print("  <-- MPU6050 (AD0=LOW)");
      if (address == 0x69) Serial.print("  <-- MPU6050 (AD0=HIGH)");
      if (address == 0x1E) Serial.print("  <-- HMC5883L Magnetometer");
      if (address == 0x77) Serial.print("  <-- BMP180/BMP280 Barometer");
      if (address == 0x76) Serial.print("  <-- BME280 Sensor");

      Serial.println();
      deviceCount++;
    }
    else if (error == 4) {
      Serial.print("  Unknown error at address 0x");
      if (address < 16) Serial.print("0");
      Serial.println(address, HEX);
    }
  }

  Serial.println();
  if (deviceCount == 0) {
    Serial.println("*** No I2C devices found! ***");
    Serial.println();
    Serial.println("Check your wiring:");
    Serial.println("  MPU6050 VCC --> Arduino 5V (or 3.3V)");
    Serial.println("  MPU6050 GND --> Arduino GND");
    Serial.println("  MPU6050 SDA --> Arduino A4");
    Serial.println("  MPU6050 SCL --> Arduino A5");
  }
  else {
    Serial.print("Found ");
    Serial.print(deviceCount);
    Serial.println(" device(s)");
  }

  Serial.println();
  Serial.println("---------------------------------");
  Serial.println("Scanning again in 5 seconds...");
  Serial.println();

  delay(5000);
}
