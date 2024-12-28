def action(action):
    action = action.replace("~action~", "")
    match action:
        case "clear_history":
            file = open("history.txt", "w")
            file.close()
            return "Chat history cleared."
        case _:
            return "I'm sorry, I don't understand that action."