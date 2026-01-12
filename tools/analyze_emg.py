#!/usr/bin/env python3
"""
EMG Signal Analyzer - Movement Chain
Process and visualize EMG recordings.

Usage:
    python3 analyze_emg.py <filename.csv>
    python3 analyze_emg.py emg_20260111_173000.csv

Features:
    - Bandpass filtering (20-450 Hz)
    - Full-wave rectification
    - Envelope extraction (smoothing)
    - Before/after visualization
"""

import sys
import numpy as np
import pandas as pd
from datetime import datetime

# ============== CONFIGURATION ==============
# Sampling rate (must match recording)
SAMPLE_RATE_HZ = 1000

# Bandpass filter settings (standard EMG range)
BANDPASS_LOW_HZ = 20    # Remove low-frequency motion artifacts
BANDPASS_HIGH_HZ = 450  # Remove high-frequency noise

# Envelope extraction (smoothing)
ENVELOPE_WINDOW_MS = 100  # Moving average window in milliseconds
# ===========================================


def load_emg_data(filename):
    """Load EMG data from CSV file."""
    print(f"Loading {filename}...")

    # Read CSV, skip metadata lines starting with #
    df = pd.read_csv(filename, comment='#')

    print(f"  Loaded {len(df):,} samples")

    return df


def bandpass_filter(signal, lowcut, highcut, fs, order=4):
    """Apply bandpass filter to signal."""
    from scipy.signal import butter, filtfilt

    nyquist = fs / 2
    low = lowcut / nyquist
    high = highcut / nyquist

    # Ensure frequencies are valid
    low = max(0.001, min(low, 0.99))
    high = max(low + 0.01, min(high, 0.99))

    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, signal)


def rectify(signal):
    """Full-wave rectification (absolute value)."""
    return np.abs(signal)


def envelope(signal, window_size):
    """Extract envelope using moving average."""
    return pd.Series(signal).rolling(window=window_size, center=True).mean().fillna(0).values


def process_emg(raw_signal, fs):
    """
    Apply standard EMG processing pipeline:
    1. Remove DC offset
    2. Bandpass filter (20-450 Hz)
    3. Full-wave rectification
    4. Envelope extraction (smoothing)
    """
    # Step 1: Remove DC offset (center around zero)
    centered = raw_signal - np.mean(raw_signal)

    # Step 2: Bandpass filter
    filtered = bandpass_filter(centered, BANDPASS_LOW_HZ, BANDPASS_HIGH_HZ, fs)

    # Step 3: Rectify (absolute value)
    rectified = rectify(filtered)

    # Step 4: Envelope (smooth)
    window_samples = int(ENVELOPE_WINDOW_MS * fs / 1000)
    smoothed = envelope(rectified, window_samples)

    return {
        'centered': centered,
        'filtered': filtered,
        'rectified': rectified,
        'envelope': smoothed
    }


def plot_comparison(raw, processed, fs, output_file=None):
    """Plot raw vs processed EMG signals."""
    import matplotlib.pyplot as plt

    time_axis = np.arange(len(raw)) / fs  # Convert to seconds

    fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)

    # Plot 1: Raw signal
    axes[0].plot(time_axis, raw, 'b-', linewidth=0.5, alpha=0.7)
    axes[0].set_ylabel('Raw EMG')
    axes[0].set_title('EMG Signal Processing Pipeline')
    axes[0].grid(True, alpha=0.3)

    # Plot 2: Filtered signal
    axes[1].plot(time_axis, processed['filtered'], 'g-', linewidth=0.5, alpha=0.7)
    axes[1].set_ylabel(f'Filtered\n({BANDPASS_LOW_HZ}-{BANDPASS_HIGH_HZ} Hz)')
    axes[1].grid(True, alpha=0.3)

    # Plot 3: Rectified signal
    axes[2].plot(time_axis, processed['rectified'], 'orange', linewidth=0.5, alpha=0.7)
    axes[2].set_ylabel('Rectified')
    axes[2].grid(True, alpha=0.3)

    # Plot 4: Envelope
    axes[3].plot(time_axis, processed['envelope'], 'r-', linewidth=1.5)
    axes[3].set_ylabel('Envelope\n(Muscle Activation)')
    axes[3].set_xlabel('Time (seconds)')
    axes[3].grid(True, alpha=0.3)

    plt.tight_layout()

    if output_file:
        plt.savefig(output_file, dpi=150)
        print(f"  Plot saved to: {output_file}")
    else:
        plt.show()


def save_processed(df, processed, output_file):
    """Save processed data to CSV."""
    result = df.copy()
    result['emg_filtered'] = processed['filtered']
    result['emg_rectified'] = processed['rectified']
    result['emg_envelope'] = processed['envelope']

    result.to_csv(output_file, index=False)
    print(f"  Processed data saved to: {output_file}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 analyze_emg.py <filename.csv>")
        print()
        print("Example:")
        print("  python3 analyze_emg.py emg_20260111_173000.csv")
        sys.exit(1)

    filename = sys.argv[1]

    print()
    print("=" * 50)
    print("  EMG Signal Analyzer")
    print("=" * 50)

    # Load data
    df = load_emg_data(filename)

    # Get raw signal
    raw_signal = df['emg_raw'].values.astype(float)

    # Process signal
    print("Processing EMG signal...")
    print(f"  Sample rate: {SAMPLE_RATE_HZ} Hz")
    print(f"  Bandpass: {BANDPASS_LOW_HZ}-{BANDPASS_HIGH_HZ} Hz")
    print(f"  Envelope window: {ENVELOPE_WINDOW_MS} ms")

    processed = process_emg(raw_signal, SAMPLE_RATE_HZ)

    # Statistics
    print()
    print("Signal Statistics:")
    print(f"  Raw - Min: {raw_signal.min():.0f}, Max: {raw_signal.max():.0f}, Range: {raw_signal.max() - raw_signal.min():.0f}")
    print(f"  Envelope - Min: {processed['envelope'].min():.1f}, Max: {processed['envelope'].max():.1f}")

    # Save processed data
    base_name = filename.replace('.csv', '')
    processed_file = f"{base_name}_processed.csv"
    save_processed(df, processed, processed_file)

    # Plot
    print()
    print("Generating plot...")
    plot_file = f"{base_name}_plot.png"

    try:
        plot_comparison(raw_signal, processed, SAMPLE_RATE_HZ, plot_file)
    except ImportError:
        print("  matplotlib not installed. Skipping plot.")
        print("  Install with: pip3 install matplotlib")

    print()
    print("=" * 50)
    print("  Analysis Complete!")
    print("=" * 50)
    print()


if __name__ == '__main__':
    main()
