// MPU6050 IMU - Raw Data Output (CSV Format)
// Movement Chain Golf Swing Analysis
//
// Wiring (I2C):
//   MPU6050 VCC → Arduino 5V (or 3.3V)
//   MPU6050 GND → Arduino GND
//   MPU6050 SDA → Arduino A4 (SDA)
//   MPU6050 SCL → Arduino A5 (SCL)
//
// Output: CSV format at configured sampling rate

#include <Wire.h>

// ============== CONFIGURATION ==============
const int MPU_ADDR = 0x68;        // I2C address (0x68 default, 0x69 if AD0=HIGH)
const long BAUD_RATE = 115200;    // Serial baud rate (match Python recorder)
const int SAMPLE_RATE_HZ = 100;   // Sampling rate (100 Hz recommended for IMU)
const int SAMPLE_DELAY_MS = 10;   // 1000 / SAMPLE_RATE_HZ

// Sensitivity settings (see datasheet)
// Accelerometer: 0=±2g, 1=±4g, 2=±8g, 3=±16g
// Gyroscope: 0=±250°/s, 1=±500°/s, 2=±1000°/s, 3=±2000°/s
const int ACCEL_RANGE = 0;        // ±2g (most sensitive for subtle movements)
const int GYRO_RANGE = 1;         // ±500°/s (good for golf swing speed)
// ===========================================

// Raw data variables
int16_t AcX, AcY, AcZ;
int16_t GyX, GyY, GyZ;
int16_t Tmp;

void setup() {
  Wire.begin();
  Serial.begin(BAUD_RATE);

  // Wake up MPU6050 (it starts in sleep mode)
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x6B);  // PWR_MGMT_1 register
  Wire.write(0);     // Set to 0 to wake up
  Wire.endTransmission(true);

  // Configure accelerometer range
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x1C);  // ACCEL_CONFIG register
  Wire.write(ACCEL_RANGE << 3);
  Wire.endTransmission(true);

  // Configure gyroscope range
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x1B);  // GYRO_CONFIG register
  Wire.write(GYRO_RANGE << 3);
  Wire.endTransmission(true);

  // Configure Digital Low Pass Filter (DLPF)
  // Setting 3 = 44Hz bandwidth, good balance of noise reduction and responsiveness
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x1A);  // CONFIG register
  Wire.write(3);     // DLPF_CFG = 3
  Wire.endTransmission(true);

  // Small delay for sensor to stabilize
  delay(100);

  // Print CSV header
  Serial.println("AcX,AcY,AcZ,GyX,GyY,GyZ,Tmp");
}

void loop() {
  // Request 14 bytes starting from ACCEL_XOUT_H (0x3B)
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x3B);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_ADDR, 14, true);

  // Read accelerometer data (3 x 16-bit values)
  AcX = Wire.read() << 8 | Wire.read();
  AcY = Wire.read() << 8 | Wire.read();
  AcZ = Wire.read() << 8 | Wire.read();

  // Read temperature (16-bit value)
  Tmp = Wire.read() << 8 | Wire.read();

  // Read gyroscope data (3 x 16-bit values)
  GyX = Wire.read() << 8 | Wire.read();
  GyY = Wire.read() << 8 | Wire.read();
  GyZ = Wire.read() << 8 | Wire.read();

  // Output CSV format: AcX,AcY,AcZ,GyX,GyY,GyZ,Tmp
  Serial.print(AcX); Serial.print(",");
  Serial.print(AcY); Serial.print(",");
  Serial.print(AcZ); Serial.print(",");
  Serial.print(GyX); Serial.print(",");
  Serial.print(GyY); Serial.print(",");
  Serial.print(GyZ); Serial.print(",");
  Serial.println(Tmp);

  delay(SAMPLE_DELAY_MS);
}
