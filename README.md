# Movement Chain Hardware

Hardware components for Movement Chain golf swing analyzer: firmware, PCB designs, and sensor tools.

## Repository Structure

```
movement-chain-hardware/
├── firmware/                    # Arduino/ESP32 firmware
│   ├── emg_sensor/             # EMG sensor (1000 Hz)
│   ├── imu_mpu6050/            # MPU6050 IMU (100 Hz)
│   └── i2c_scanner/            # I2C diagnostic tool
├── tools/                       # Python recording & analysis
│   ├── record_emg.py           # EMG data recorder
│   ├── record_imu.py           # IMU data recorder
│   ├── analyze_emg.py          # Signal processing
│   └── requirements.txt
├── pcb/                         # KiCad PCB designs (future)
└── docs/                        # Documentation
    └── sensor-recording.md     # Sensor recording guide
```

## Quick Start

### 1. Install Python Dependencies

```bash
cd tools
pip3 install --user --break-system-packages -r requirements.txt
```

### 2. Upload Arduino Firmware

1. Open Arduino IDE
2. Open firmware (e.g., `firmware/emg_sensor/emg_sensor.ino`)
3. Select Board: Arduino Uno
4. Select Port
5. Click Upload

### 3. Record Sensor Data

```bash
# EMG recording (1000 Hz)
python3 tools/record_emg.py

# IMU recording (100 Hz)
python3 tools/record_imu.py
```

- Press **ENTER** to start recording
- Press **Ctrl+C** to stop and save

## Hardware Setup

### EMG Sensor

```
EMG Sensor          Arduino Uno
┌─────────┐        ┌───────────┐
│  + VCC  │───────→│    5V     │
│  - GND  │───────→│    GND    │
│  S SIG  │───────→│    A0     │
└─────────┘        └───────────┘
```

### IMU (MPU6050)

```
MPU6050             Arduino Uno
┌─────────┐        ┌───────────┐
│   VCC   │───────→│    5V     │
│   GND   │───────→│    GND    │
│   SDA   │───────→│    A4     │
│   SCL   │───────→│    A5     │
└─────────┘        └───────────┘
```

## Documentation

- [Sensor Recording Guide](docs/sensor-recording.md) - Detailed recording instructions

## Commit Message Format

Use [Conventional Commits](https://www.conventionalcommits.org/):

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation |
| `fw` | Firmware changes |
| `pcb` | PCB layout changes |
| `sch` | Schematic changes |
| `bom` | Bill of Materials |

## License

MIT License - see [LICENSE](LICENSE)

---

**Project**: Movement Chain
**Last Updated**: January 2026
