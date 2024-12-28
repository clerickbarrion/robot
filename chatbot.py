from openai import OpenAI
from datetime import datetime

with open(".env", "r") as file:
    api_key = file.read()

client = OpenAI(api_key=api_key)

def send_message(message, audio_file, audio=False):
    file = open("./history.txt", "r")
    history = file.readlines()
    file.close()
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": f'''
        Here is the conversation so far:
        --
        {history}
        --
        '''},
        #
        {"role": "user", "content": message}
    ],
    temperature=1,)
    file = open("history.txt", "a")
    file.write(f"User: {message}\n")
    file.write(f"BMO: {response.choices[0].message.content}\n")
    file.close()
    if audio:
        client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=response.choices[0].message.content
        ).stream_to_file(f"audio/{audio_file}.mp3")

    return response.choices[0].message.content

if __name__ == "__main__":
    while True:
        audio_file = f"{datetime.now().strftime('%Y%m%d%H%M%S')}"
        message = input("You: ")
        print("BMO:",send_message(message, audio_file))