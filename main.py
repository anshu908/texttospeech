from flask import Flask, request, jsonify, send_from_directory
from gtts import gTTS
import os

app = Flask(__name__)

audio_folder = "audio_files"
os.makedirs(audio_folder, exist_ok=True)

@app.route('/text-to-speech', methods=['GET', 'POST'])
def text_to_speech():
    text = request.args.get('text') or (request.json and request.json.get('text'))
    
    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    filename = "output.mp3"
    filepath = os.path.join(audio_folder, filename)
    
    tts = gTTS(text)  # No credit in audio
    tts.save(filepath)
    
    audio_url = f"/audio/{filename}"
    
    return jsonify({"message": "Audio generated successfully by AnshAPi", "audio_url": audio_url})

@app.route('/audio/<filename>')
def serve_audio(filename):
    return send_from_directory(audio_folder, filename)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))  # Cloudflare compatible port
    app.run(debug=True, host='0.0.0.0', port=port)
