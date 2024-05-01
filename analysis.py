import librosa
import librosa.display
import matplotlib.pyplot as plt

# Load the audio file
audio_path = 'audio-files/alex-fox-guitar-on-fire.mp3'
y, sr = librosa.load(audio_path)

# Compute the Short-time Fourier Transform (STFT)
D = librosa.stft(y)

# Convert magnitude to decibels
D_db = librosa.amplitude_to_db(abs(D))

# Plot the spectrogram
librosa.display.specshow(D_db, sr=sr, x_axis='time', y_axis='linear')
plt.colorbar(format='%+2.0f dB')
plt.title('Spectrogram')
plt.show()
