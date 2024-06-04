from flask import Flask, render_template, request, send_file, abort
import librosa
import os
import soundfile as sf
import tempfile

app = Flask(__name__)

def change_frequency(audio_file, target_sr, res_type='sinc_best'):
    y, orig_sr = librosa.load(audio_file)
    y_resampled = librosa.resample(y=y, orig_sr=orig_sr, target_sr=target_sr, res_type=res_type)

    # Create a temporary file for the modified audio
    temp_dir = tempfile.gettempdir()
    new_file_name = f"{os.path.splitext(os.path.basename(audio_file))[0]}_modified_{target_sr}.wav"
    new_file_path = os.path.join(temp_dir, new_file_name)
    
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

        hz_option = request.form.get('hz_option')

        if hz_option is None or not hz_option.isdigit():
            return 'Please enter a valid Hz value (20 Hz to 20,000 Hz)'

        target_sr = int(hz_option)

        if target_sr < 20 or target_sr > 20000:
            return 'Please enter a Hz value between 20 and 20,000'

        # Save the uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            file.save(temp_file.name)
            temp_file_path = temp_file.name

        # Change frequency
        modified_file_path = change_frequency(temp_file_path, target_sr)

        # Send the modified file to the client
        response = send_file(modified_file_path, as_attachment=True)

        # Clean up the temporary files
        os.remove(temp_file_path)
        os.remove(modified_file_path)

        return response
    except Exception as e:
        app.logger.error(str(e))
        abort(500, description='An unexpected error occurred')

@app.errorhandler(404)
def page_not_found(e):
    app.logger.error(f'Page not found: {request.url}')
    return 'Page not found', 404

if __name__ == '__main__':
    app.run(debug=True)
