import librosa
import matplotlib.pyplot as plt
import numpy as np

# Load audio file
audio_file = "audio_files/fredericchopin_ nocturne.mp3"
y, sr = librosa.load(audio_file)

# Extract pitch
pitches, magnitudes = librosa.piptrack(y=y, sr=sr)

# Filter out invalid pitches (negative or zero frequencies)
valid_pitches = pitches[pitches > 0]
valid_magnitudes = magnitudes[pitches > 0]

# Convert pitch to MIDI notes
midi_notes = librosa.hz_to_midi(valid_pitches)

# Check if midi_notes is a 2D array
if len(midi_notes.shape) == 1:
    # If it's 1D, reshape to 2D array with one row
    midi_notes = np.expand_dims(midi_notes, axis=0)

# Get the time frames where pitch detection succeeded
valid_frames = np.where(midi_notes != -np.inf)[1]

times = librosa.times_like(valid_pitches)

# Plot the MIDI notes over time for valid frames
plt.figure(figsize=(10, 4))
plt.scatter(times[valid_frames], midi_notes[0, valid_frames], c=valid_magnitudes[valid_frames], cmap='viridis')
plt.xlabel('Time (s)')
plt.ylabel('MIDI Note')
plt.title('Detected Notes')
plt.colorbar(label='Magnitude')
plt.tight_layout()
plt.show()

