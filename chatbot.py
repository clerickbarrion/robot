from openai import OpenAI
from datetime import datetime
from actions import action

with open(".env", "r") as file:
    api_key = file.read()

client = OpenAI(api_key=api_key)

def send_message(message, audio_file, audio=False):
    file = open("./history.txt", "r")
    history = file.readlines()
    file.close()
    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": f'''
        The current time is {datetime.now().strftime("%H:%M:%S")}.
        Here is the conversation so far:
        --
        {history}
        --
        If you interpret the user to be giving you a command, respond only with the following and nothing else:
        ~action~ACTION_NAME
        
        For example, the user says "Please clear the chat history" you respond with:
        ~action~clear_history
        
        Currently, the following actions are supported:
        ~action~clear_history
        '''},
        {"role": "user", "content": message}
    ],
    temperature=1,)
    response = response.choices[0].message.content
    file = open("history.txt", "a")
    file.write(f"User: {message}\n")
    file.write(f"BMO: {response}\n")
    file.close()
    if audio:
        if response.startswith("~action~"):
            response = action(response)
        response = action(response)
        client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=response
        ).stream_to_file(f"{audio_file}.mp3")

    return response

if __name__ == "__main__":
    while True:
        audio_file = f"{datetime.now().strftime('%Y%m%d%H%M%S')}"
        message = input("You: ")
        print("BMO:",send_message(message, audio_file))