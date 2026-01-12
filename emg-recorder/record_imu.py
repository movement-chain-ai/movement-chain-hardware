#!/usr/bin/env python3
"""
IMU (MPU6050) Data Recorder - Movement Chain
Records accelerometer and gyroscope data with real timestamps.

Usage:
    python3 record_imu.py

Controls:
    ENTER  = Start recording
    Ctrl+C = Stop recording and save
"""

import serial
import serial.tools.list_ports
import time
import sys
from datetime import datetime

# ============== CONFIGURATION ==============
# Serial port (auto-detected if empty)
PORT = ''  # e.g., '/dev/cu.usbmodem3101' or 'COM3'

# Serial settings
BAUD_RATE = 115200

# Sampling (must match Arduino)
SAMPLE_RATE_HZ = 100

# Output format
INCLUDE_HEADER_METADATA = True
# ===========================================


def find_port():
    """Auto-detect Arduino serial port."""
    ports = serial.tools.list_ports.comports()

    # Priority 1: Look for USB modem/serial (Arduino Uno, etc.)
    for p in ports:
        if 'usbmodem' in p.device.lower() or 'usbserial' in p.device.lower():
            return p.device

    # Priority 2: Look for Arduino in description
    for p in ports:
        if any(x in p.description.lower() for x in ['arduino', 'ch340', 'ftdi']):
            return p.device

    # Priority 3: Windows COM ports (but not Bluetooth)
    for p in ports:
        if p.device.startswith('COM') and 'bluetooth' not in p.device.lower():
            return p.device

    return None


def main():
    global PORT

    print()
    print("=" * 50)
    print("  IMU Recorder (MPU6050) - Movement Chain")
    print("=" * 50)

    # Auto-detect port if not specified
    if not PORT:
        PORT = find_port()
        if PORT:
            print(f"  Auto-detected port: {PORT}")
        else:
            print("  ERROR: No Arduino found!")
            print()
            print("  To find your port manually:")
            print("    Mac:     ls /dev/cu.usb*")
            print("    Windows: Check Device Manager")
            print()
            print("  Then set PORT in this script.")
            sys.exit(1)

    # Connect to Arduino
    print(f"  Connecting to {PORT}...")
    try:
        ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
    except serial.SerialException as e:
        print(f"  ERROR: Cannot connect to {PORT}")
        print(f"    {e}")
        print()
        print("  Make sure:")
        print("    1. Arduino is plugged in")
        print("    2. Arduino IDE Serial Monitor is CLOSED")
        sys.exit(1)

    # Wait for Arduino to reset
    time.sleep(2)
    ser.reset_input_buffer()

    # Skip the CSV header line from Arduino
    header_line = ser.readline().decode('utf-8').strip()
    print(f"  Arduino header: {header_line}")

    # Generate filename with timestamp
    filename = f"imu_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    print(f"  Output file: {filename}")

    print()
    print("=" * 50)
    print("  Ready to record!")
    print("=" * 50)
    print()
    print("  Press ENTER to start recording...")
    print()

    # Wait for Enter key to start
    try:
        input()
    except EOFError:
        pass

    # Clear any buffered data before starting
    ser.reset_input_buffer()

    # Now start recording
    start_time = datetime.now()

    print()
    print("  Recording started!")
    print("  Press Ctrl+C to stop and save.")
    print("=" * 50)
    print()

    sample_count = 0
    error_count = 0

    # Start recording
    with open(filename, 'w') as f:
        # Write metadata header
        if INCLUDE_HEADER_METADATA:
            f.write(f"# IMU Recording (MPU6050) - Movement Chain\n")
            f.write(f"# Start time: {start_time.isoformat()}\n")
            f.write(f"# Sample rate: {SAMPLE_RATE_HZ} Hz\n")
            f.write(f"# Port: {PORT}\n")
            f.write(f"#\n")

        # Write CSV header
        f.write("timestamp,AcX,AcY,AcZ,GyX,GyY,GyZ,Tmp\n")

        try:
            while True:
                if ser.in_waiting:
                    try:
                        # Read line from Arduino
                        line = ser.readline().decode('utf-8').strip()

                        # Validate it looks like CSV data (has commas, not header)
                        if ',' in line and not line.startswith('AcX'):
                            # Get current timestamp
                            now = datetime.now()
                            timestamp = now.strftime('%Y-%m-%d %H:%M:%S.') + f"{now.microsecond // 1000:03d}"

                            # Write to file
                            f.write(f"{timestamp},{line}\n")
                            sample_count += 1

                            # Progress indicator every 100 samples (1 second at 100Hz)
                            if sample_count % 100 == 0:
                                elapsed = (datetime.now() - start_time).total_seconds()
                                actual_rate = sample_count / elapsed if elapsed > 0 else 0
                                print(f"  Samples: {sample_count:,}  |  Time: {elapsed:.1f}s  |  Rate: {actual_rate:.0f} Hz")

                    except UnicodeDecodeError:
                        error_count += 1

        except KeyboardInterrupt:
            pass

    # Close serial connection
    ser.close()

    # Print summary
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    print()
    print("=" * 50)
    print("  Recording Complete!")
    print("=" * 50)
    print(f"  Duration:    {duration:.1f} seconds")
    print(f"  Samples:     {sample_count:,}")
    if duration > 0:
        print(f"  Actual rate: {sample_count / duration:.0f} Hz")
    print(f"  Saved to:    {filename}")
    if error_count > 0:
        print(f"  Errors:      {error_count} (decode errors, ignored)")
    print()
    print("  Data columns:")
    print("    AcX, AcY, AcZ = Accelerometer (raw values)")
    print("    GyX, GyY, GyZ = Gyroscope (raw values)")
    print("    Tmp = Temperature (raw value)")
    print()
    print("  To convert raw values:")
    print("    Accel (±2g):  value / 16384.0 = g-force")
    print("    Gyro (±500):  value / 65.5 = degrees/sec")
    print("    Temp:         value / 340.0 + 36.53 = Celsius")
    print("=" * 50)
    print()


if __name__ == '__main__':
    main()
