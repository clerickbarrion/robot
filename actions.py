from time import sleep

def action(action, arduino):
    
    def send_command(command):
        command += "\n"
        arduino.write(command.encode())
        sleep(0.1)
        return command
    action = action.replace("~action~", "")
    match action:
        case "clear_history":
            file = open("history.txt", "w")
            file.close()
            return "Chat history cleared."
        case "move_forward":
            return send_command("move_forward")
        case "move_backward":
            return send_command("move_backward")
        case "turn_left":
            return send_command("turn_left")
        case "turn_right":
            return send_command("turn_right")
        # case "stop_moving":
        #     return send_command("stop_moving")
        case "shake_head":
            return send_command("shake_head")
        case _:
            return "I'm sorry, I don't understand that action."