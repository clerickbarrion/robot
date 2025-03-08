from openai import OpenAI
from datetime import datetime
from actions import action
import re

with open(".env", "r") as file:
    api_key = file.read().strip()

client = OpenAI(api_key=api_key)

def send_message(message, audio_file, audio=False, arduino=None):
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
        Your primary goal is to chat with the user.
        If you interpret the user to be giving you a command, respond like so:
        ~action~ACTION_NAME The rest of your response here
        
        For example, the user says "Please clear the chat history" you respond with:
        ~action~clear_history Okay, I have cleared the chat history.
        
        Currently, the following actions are supported:
        ~action~clear_history
        ~action~move_forward
        ~action~move_backward
        ~action~turn_left
        ~action~turn_right
        ~action~stop_moving
        ~action~shake_head
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
            client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=response[1]
            ).stream_to_file(f"{audio_file}.mp3")
    if response.startswith("~action~"):
        match = re.match(r"(~action~\w+)\s*(.*)", response)
        if match:
            response = [match.group(1), match.group(2)]
        action(response[0], arduino)

    return response[1] or response

if __name__ == "__main__":
    import serial
    arduino = serial.Serial(port="COM3", baudrate=9600, timeout=1)
    while True:
        audio_file = f"audio/{datetime.now().strftime('%Y%m%d%H%M%S')}"
        message = input("You: ")
        print("BMO:",send_message(message, audio_file, arduino=arduino))
