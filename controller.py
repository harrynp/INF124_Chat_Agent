__author__ = 'Harry'
import json
import os

def get_user_info():
    keyword = ""
    extra_info = ""
    while keyword != "QUESTION" and keyword != "FEEDBACK" and keyword != "OTHER":
        keyword = input("Please choose from one of the following keywords:\nQUESTION: Ask a live agent a question.\nFEEDBACK: Send us some feedback.\nOTHER: Any other option not listed above.\n")
    if keyword == "QUESTION":
        extra_info = input("Please enter your question that will be sent to the agent: ")
    elif keyword == "FEEDBACK":
        extra_info = input("Please enter your feedback that want to talk to the agent about: ")
    elif keyword == "OTHER":
        extra_info = input("Please enter any information that may help the agent with this request: ")
    return json.dumps(dict([("command", keyword),
                            ("info", extra_info)]))


def user_input(handler, msg, chat_log):
    while True:
        msg = input(handler.get_username() + ": ")
        if len(msg) > 0:
            if msg.startswith(":s"):
                msg.strip()
                split_string = msg.split(' ', 1)
                if len(split_string) == 1:
                    path = "log.txt"
                else:
                    path = split_string[1] + "\\log.txt"
                f = open(path, 'w')
                for message in chat_log:
                    f.write("{}: {}\n".format(message[0], message[1]))
                f.close()
                if path == "log.txt":
                    print("Log file saved at {}{}!".format(os.getcwd(), "\\log.txt"))
                else:
                    print("Log file saved at {}!".format(path))
            elif msg == ":q":
                handler.close()
                return
            else:
                handler.push(bytes("MESSAGE " + json.dumps(dict([("username", handler.get_username()),
                                                                 ("message", msg)])) + "\0", 'UTF-8'))
                chat_log.append((handler.get_username(), msg))
        msg = ""
