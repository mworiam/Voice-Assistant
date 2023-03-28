import gradio as gr
import openai
import API
import pyttsx3

openai.api_key = API.API_KEY

messages = [
            {"role": "system", "content": "You are a helpful assistant."}
]


def transcribe(audio):
    global messages

    audio_file = open(audio, "rb")

    transcript = openai.Audio.transcribe("whisper-1", audio_file)

    print(transcript)

    messages.append({"role": "user", "content": transcript["text"]})

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    system_message = response["choices"][0]["message"]["content"]

    engine = pyttsx3.init()
    engine.say(system_message)
    engine.runAndWait()

    messages.append({"role": "assistant", "content": system_message})

    chat_transcript = ""

    for message in messages:
        if message['role'] != 'system':
            chat_transcript += message['role'] + ": " + message['content'] + "\n\n"

    return chat_transcript


ui = gr.Interface(fn=transcribe, inputs=gr.Audio(source='microphone', type='filepath'), outputs="text").launch(share=True)
ui.launch(share=True)
