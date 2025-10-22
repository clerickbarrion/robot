from actions import ActionHandler
import os
from RealtimeTTS import TextToAudioStream,  GTTSEngine, GTTSVoice, SystemEngine, SystemVoice, OpenAIEngine, OpenAIVoice
from openai import OpenAI
from datetime import datetime
import re
import pyaudio

class ChatBot:
    def __init__(self, env_path=".env", history_path="history.txt"):
        self.OpenAI = OpenAI
        self.datetime = datetime
        self.re = re
        with open(env_path, "r") as file:
            api_key = file.read().strip()
        self.client = OpenAI(api_key=api_key)
        os.environ["OPENAI_API_KEY"] = api_key
        self.history_path = history_path
        self.action_handler = ActionHandler(history_path)
        self.engine = OpenAIEngine(speed=1.1, voice="fable")
        self.stream = TextToAudioStream(self.engine)
        for path in ["./pictures", "./audio"]:
            if not os.path.exists(path):
                os.makedirs(path) 

    def send_message(self, message, audio=False, arduino=None):
        with open(self.history_path, "r") as file:
            history = file.readlines()
        response_chunks = []
        stream = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f'''
                The current time is {self.datetime.now().strftime("%H:%M:%S")}.
                Here is the conversation so far:
                --
                {history}
                --
                Your primary goal is to chat with the user.
                Never use emojis in your responses.
                Keep your responses at a maximum of 4 sentences.
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
                ~action~take_picture
                '''},
                {"role": "user", "content": message}
            ],
            temperature=1,
            stream=True,
        )
        print("BMO: ", end="", flush=True)
        for chunk in stream:
            if hasattr(chunk.choices[0].delta, "content"):
                content = chunk.choices[0].delta.content
                if content is not None:
                    print(content, end="", flush=True)
                    response_chunks.append(content)
        response = "".join(response_chunks)
        print()  # Newline after streaming
        with open(self.history_path, "a") as file:
            file.write(f"User: {message}\n")
            file.write(f"BMO: {response}\n")
        match = self.re.match(r"(~action~\w+)\s*(.*)", response)
        if match:
            response = [match.group(1), match.group(2)]
            action_response = self.action_handler.handle(response[0], message, arduino, self.client)
            response = action_response or response[1]
            print(response) if action_response else ""
        if audio:
            self.stream.feed(response)
            self.stream.play_async()

if __name__ == "__main__":
    import serial
    # arduino = serial.Serial(port="/dev/ttyACM0", baudrate=9600, timeout=1)
    bot = ChatBot()
    while True:
        message = input("You: ")
        bot.send_message(message, audio=True)
