# EMG Recorder - Movement Chain

Record and analyze EMG sensor data for golf swing analysis.

## Quick Start

### 1. Hardware Setup

```
EMG Sensor          Arduino Uno
┌─────────┐        ┌───────────┐
│  + VCC  │───────→│    5V     │
│  - GND  │───────→│    GND    │
│  S SIG  │───────→│    A0     │
└─────────┘        └───────────┘
                         │
                         ▼
                    USB to Computer
```

### 2. Upload Arduino Code

1. Open Arduino IDE
2. Open `arduino/emg_sensor/emg_sensor.ino`
3. Select Board: Arduino Uno
4. Select Port
5. Click Upload

### 3. Install Python Dependencies

```bash
cd emg-recorder
pip3 install --user --break-system-packages -r requirements.txt
```

### 4. Record EMG Data

```bash
python3 record_emg.py
```

Press `Ctrl+C` to stop recording.

### 5. Analyze Data

```bash
python3 analyze_emg.py emg_20260111_173000.csv
```

This generates:
- `emg_*_processed.csv` - Processed data with envelope
- `emg_*_plot.png` - Visualization of raw vs processed signal

## File Structure

```
emg-recorder/
├── arduino/
│   └── emg_sensor/
│       └── emg_sensor.ino    # Arduino code (1000 Hz sampling)
├── record_emg.py             # Recording script
├── analyze_emg.py            # Signal processing script
├── requirements.txt          # Python dependencies
└── README.md
```

## Configuration

### Arduino (`emg_sensor.ino`)

```cpp
const int EMG_PIN = A0;           // Analog pin
const int SAMPLE_DELAY_MS = 1;    // 1ms = 1000 Hz
const long BAUD_RATE = 115200;    // Serial speed
```

### Python (`record_emg.py`)

```python
PORT = ''              # Auto-detect, or set manually
BAUD_RATE = 115200     # Must match Arduino
SAMPLE_RATE_HZ = 1000  # Must match Arduino
```

### Analysis (`analyze_emg.py`)

```python
SAMPLE_RATE_HZ = 1000      # Must match recording
BANDPASS_LOW_HZ = 20       # Low cutoff (motion artifacts)
BANDPASS_HIGH_HZ = 450     # High cutoff (noise)
ENVELOPE_WINDOW_MS = 100   # Smoothing window
```

## Output Format

### Raw Recording (`emg_*.csv`)

```csv
# EMG Recording - Movement Chain
# Start time: 2026-01-11T17:30:45.123456
# Sample rate: 1000 Hz
# Port: /dev/cu.usbmodem3101
#
timestamp,emg_raw
2026-01-11 17:30:45.001,512
2026-01-11 17:30:45.002,518
2026-01-11 17:30:45.003,520
```

### Processed Data (`emg_*_processed.csv`)

```csv
timestamp,emg_raw,emg_filtered,emg_rectified,emg_envelope
2026-01-11 17:30:45.001,512,0.5,0.5,0.3
2026-01-11 17:30:45.002,518,2.1,2.1,0.4
```

## Signal Processing Pipeline

```
Raw EMG → DC Offset Removal → Bandpass Filter → Rectify → Envelope
                              (20-450 Hz)       (|x|)    (smooth)
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Port not found | Close Arduino IDE Serial Monitor |
| Values always 940-1023 | Reduce EMG board gain (turn potentiometer) |
| Values always ~512 | Check electrode contact with skin |
| No data | Check USB cable and Arduino upload |

## Dependencies

- Python 3.10+
- pyserial
- numpy
- pandas
- scipy
- matplotlib
