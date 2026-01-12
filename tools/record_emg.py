#!/usr/bin/env python3
"""
EMG Data Recorder - Movement Chain
Records EMG sensor data with real timestamps.

Usage:
    python3 record_emg.py

Controls:
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
SAMPLE_RATE_HZ = 1000

# Output format
INCLUDE_HEADER_METADATA = True  # Add recording info at top of CSV
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
    print("  EMG Recorder - Movement Chain")
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
    ser.reset_input_buffer()  # Clear any startup garbage

    # Generate filename with timestamp
    start_time = datetime.now()
    filename = f"emg_{start_time.strftime('%Y%m%d_%H%M%S')}.csv"

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

    # Update start time to when recording actually begins
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
            f.write(f"# EMG Recording - Movement Chain\n")
            f.write(f"# Start time: {start_time.isoformat()}\n")
            f.write(f"# Sample rate: {SAMPLE_RATE_HZ} Hz\n")
            f.write(f"# Port: {PORT}\n")
            f.write(f"#\n")

        # Write CSV header
        f.write("timestamp,emg_raw\n")

        try:
            while True:
                if ser.in_waiting:
                    try:
                        # Read line from Arduino
                        line = ser.readline().decode('utf-8').strip()

                        # Validate it's a number
                        if line.isdigit() or (line.startswith('-') and line[1:].isdigit()):
                            # Get current timestamp
                            now = datetime.now()
                            timestamp = now.strftime('%Y-%m-%d %H:%M:%S.') + f"{now.microsecond // 1000:03d}"

                            # Write to file
                            f.write(f"{timestamp},{line}\n")
                            sample_count += 1

                            # Progress indicator every 1000 samples
                            if sample_count % 1000 == 0:
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
    print(f"  Actual rate: {sample_count / duration:.0f} Hz")
    print(f"  Saved to:    {filename}")
    if error_count > 0:
        print(f"  Errors:      {error_count} (decode errors, ignored)")
    print()
    print("  Next steps:")
    print(f"    - View in Excel: open {filename}")
    print(f"    - Analyze: python3 analyze_emg.py {filename}")
    print("=" * 50)
    print()


if __name__ == '__main__':
    main()
