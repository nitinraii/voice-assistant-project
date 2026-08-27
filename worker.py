from openai import OpenAI
import requests

openai_client = OpenAI()


def speech_to_text(audio_binary):
   # Watson Speech-to-Text API URL
    base_url = "https://sn-watson-stt.labs.skills.network"
    api_url = base_url + "/speech-to-text/api/v1/recognize"

    # English (US) speech model
    params = {
        "model": "en-US_Multimedia",
    }

    # Send audio to Watson
    response = requests.post(
        api_url,
        params=params,
        data=audio_binary
    ).json()

    # Get converted text from the response
    text = "null"
    if response.get("results"):
        print("speech to text response:", response)
        text = response["results"][0]["alternatives"][0]["transcript"]
        print("recognised text:", text)

    return text


def text_to_speech(text, voice=""):
    # Watson Text-to-Speech API URL
    base_url = "https://sn-watson-tts.labs.skills.network"
    api_url = (
        base_url
        + "/text-to-speech/api/v1/synthesize?output=output_text.wav"
    )

    # User ne specific voice select ki ho to use add karo
    if voice != "" and voice != "default":
        api_url += "&voice=" + voice

    # Request headers
    headers = {
        "Accept": "audio/wav",
        "Content-Type": "application/json",
    }

    # Text that Watson will speak
    json_data = {
        "text": text,
    }

    # Send text to Watson and receive WAV audio
    response = requests.post(api_url, headers=headers, json=json_data)
    print("text to speech response:", response)

    return response.content

def openai_process_message(user_message):
    prompt = (
        "Act like a personal assistant. You can respond to questions, "
        "translate sentences, summarize news, and give recommendations. "
        "Keep responses concise - 2 to 3 sentences maximum."
    )

    openai_response = openai_client.chat.completions.create(
        model="gpt-5-nano",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_message}
        ],
        max_completion_tokens=1000
    )

    print("openai response:", openai_response)

    response_text = openai_response.choices[0].message.content
    return response_text