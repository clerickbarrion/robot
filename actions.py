from time import sleep

class ActionHandler:
    def __init__(self, history_path="history.txt"):
        self.sleep = sleep
        self.history_path = history_path

    def send_command(self, command, arduino):
        command += "\n"
        arduino.write(command.encode())
        self.sleep(0.1)
        return command

    def handle(self, action, arduino):
        action = action.replace("~action~", "")
        match action:
            case "clear_history":
                file = open(self.history_path, "w")
                file.close()
                return "Chat history cleared."
            case "move_forward":
                return self.send_command("move_forward", arduino)
            case "move_backward":
                return self.send_command("move_backward", arduino)
            case "turn_left":
                return self.send_command("turn_left", arduino)
            case "turn_right":
                return self.send_command("turn_right", arduino)
            # case "stop_moving":
            #     return self.send_command("stop_moving", arduino)
            case "shake_head":
                return self.send_command("shake_head", arduino)
            case _:
                return "I'm sorry, I don't understand that action."