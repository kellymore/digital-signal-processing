from flask import Flask, render_template, request, send_from_directory
import librosa
import os
import soundfile as sf

app = Flask(__name__)

# Route for serving audio files
@app.route('/audio_files/<path:filename>')
def serve_audio(filename):
    return send_from_directory('audio_files', filename)

def change_frequency(audio_file, target_sr=None, res_type='sinc_best'):
    """
    This function uploads a song, changes its frequency to the target sampling rate,
    and saves the modified version.

    Args:
        audio_file (str): Path to the audio file to be modified.
        target_sr (int, optional): The desired sampling rate after resampling. Defaults to None (use value from request).
        res_type (str, optional): The resampling method. Defaults to 'sinc_best'.
    Returns:
        str: The path to the modified audio file.
    """

    # Upload the song
    y, orig_sr = librosa.load(audio_file)

    # Get target sampling rate from request (if not provided)
    if target_sr is None:
        target_sr = int(request.form.get('hz_option'))

    # Change frequency (resample)
    y_resampled = librosa.resample(y=y, orig_sr=orig_sr, target_sr=target_sr, res_type=res_type)

    # Create new file path
    base_dir = os.path.dirname(audio_file)
    new_file_name = f"{os.path.splitext(os.path.basename(audio_file))[0]}_modified_{target_sr}.wav"
    new_file_path = os.path.join(base_dir, new_file_name)
  
    sf.write(new_file_path, y_resampled, target_sr)

    return new_file_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'file' not in request.files:
            return 'No file part'

        file = request.files['file']

        if file.filename == '':
            return 'No selected file'

        # Get the selected Hz option
        hz_option = request.form.get('hz_option')  # Get value from form

        if hz_option is None:
            return 'Please select a Hz option (444 Hz or 528 Hz)'  # Handle missing selection

        target_sr = int(hz_option)

        file_path = os.path.join('audio_files', file.filename)
        file.save(file_path)

        # Change frequency using target_sr from Hz option
        modified_file_path = change_frequency(file_path, target_sr)

        return render_template('result.html', filename=file.filename, modified_filename=os.path.basename(modified_file_path))
    except Exception as e:
        app.logger.error(str(e))
        os.abort(500, 'An unexpected error occurred')

@app.errorhandler(404)
def page_not_found(e):
    app.logger.error(f'Page not found: {request.url}')
    return 'Page not found', 404

if __name__ == '__main__':
    app.run(debug=True)
