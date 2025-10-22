from time import sleep
from subprocess import run
import os
import re
class ActionHandler:
    def __init__(self, history_path="history.txt"):
        self.sleep = sleep
        self.history_path = history_path

    def send_command(self, command, arduino):
        command += "\n"
        arduino.write(command.encode())
        self.sleep(0.1)

    def handle(self, action, message, arduino, client=None):
        action = action.replace("~action~", "")
        match action:
            case "clear_history":
                file = open(self.history_path, "w")
                file.close()
            case "move_forward":
                self.send_command("move_forward", arduino)
            case "move_backward":
                self.send_command("move_backward", arduino)
            case "turn_left":
                self.send_command("turn_left", arduino)
            case "turn_right":
                self.send_command("turn_right", arduino)
            # case "stop_moving":
            #     return self.send_command("stop_moving", arduino)
            case "shake_head":
                self.send_command("shake_head", arduino)
            case "take_picture":
                device = re.findall(r'"([^"]+)" \(video\)', run('ffmpeg -list_devices true -f dshow -i dummy', shell=True, text=True, capture_output=True).stderr)[0]
                run(f'ffmpeg -f dshow -i video="{device}" -frames:v 1 ./pictures/photo.jpg')
                sleep(2)
                with open("./pictures/photo.jpg", "rb") as img_file:
                    file = client.files.create(
                        file=img_file,
                        purpose="vision"
                    )
                response = client.responses.create(
                    model="gpt-4.1-mini",
                    input=[{
                        "role": "user",
                        "content": [
                            {"type": "input_text", "text": message},
                            {
                                "type": "input_image",
                                "file_id": file.id,
                            },
                        ],
                    }],
                )
                os.remove("./pictures/photo.jpg")
                return response.output_text
            case _:
                return "I'm sorry, I don't understand that action."