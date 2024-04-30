import soundfile as sf
import librosa

def change_frequency(audio_file, target_sr=444, res_type='sinc_best'):
  """
  This function uploads a song, changes its frequency to the target sampling rate,
  and saves the modified version.

  Args:
      audio_file (str): Path to the audio file to be modified.
      target_sr (int, optional): The desired sampling rate after resampling. Defaults to 444 Hz.
  """

  # Upload the song
  y, orig_sr = librosa.load(audio_file)

  # Change frequency (resample)
  y_resampled = librosa.resample(y=y, orig_sr=orig_sr, target_sr=target_sr, res_type=res_type)

  # Save the modified song with new sampling rate
  new_file_name = f"{audio_file[:-4]}_modified_{target_sr}.wav"  # Create new filename with suffix
  sf.write(new_file_name, y_resampled, target_sr)

  print(f"Audio modified and saved as: {new_file_name}")

change_frequency('audio-files/alex-fox-guitar-on-fire.mp3')
