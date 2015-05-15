__author__ = 'Harry'
import json

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
                    path = split_string + "\\log.txt"
                f = open("log.txt", 'w')
                for message in chat_log:
                    f.write("{}: {}\n".format(message[0], message[1]))
                f.close()
                print("Log file saved!")
            elif msg == ":q":
                handler.close()
                return
            else:
                handler.push(bytes("MESSAGE " + json.dumps(dict([("username", handler.get_username()),
                                                                 ("message", msg)])) + "\0", 'UTF-8'))
                chat_log.append((handler.get_username(), msg))
        msg = ""
