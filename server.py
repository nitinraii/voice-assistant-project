import base64
import json
from flask import Flask, render_template, request
from worker import speech_to_text, text_to_speech, openai_process_message
from flask_cors import CORS
import os

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/speech-to-text', methods=['POST'])
def speech_to_text_route():
    print("processing speech-to-text")

    # Browser se aayi audio
    audio_binary = request.data

    # Watson Speech-to-Text call
    text = speech_to_text(audio_binary)

    # Browser ko JSON me converted text bhejo
    response = app.response_class(
        response=json.dumps({"text": text}),
        status=200,
        mimetype="application/json"
    )

    print(response)
    print(response.data)
    return response


@app.route('/process-message', methods=['POST'])
def process_prompt_route():
   # User ka text aur selected voice
    user_message = request.json["userMessage"]
    print("user_message:", user_message)

    voice = request.json["voice"]
    print("voice:", voice)

    # OpenAI se text response
    openai_response_text = openai_process_message(user_message)

    # Empty lines remove karo
    openai_response_text = os.linesep.join(
        [line for line in openai_response_text.splitlines() if line]
    )

    # Text ko speech/WAV audio me badlo
    openai_response_speech = text_to_speech(
        openai_response_text,
        voice
    )

    # Audio ko JSON me bhejne layak base64 text me convert karo
    openai_response_speech = base64.b64encode(
        openai_response_speech
    ).decode("utf-8")

    # Browser ko text + audio dono bhejo
    response = app.response_class(
        response=json.dumps({
            "openaiResponseText": openai_response_text,
            "openaiResponseSpeech": openai_response_speech
        }),
        status=200,
        mimetype="application/json"
    )

    print(response)
    return response


if __name__ == "__main__":
    app.run(port=8000, host='0.0.0.0')
