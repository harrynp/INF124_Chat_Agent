__author__ = 'Harry'

import asyncore
import asynchat
import socket
import json
import threading
import controller

msg = ""
chat_log = []


# def user_input(handler, msg):
#     while True:
#         msg = input(handler.get_username() + ": ")
#         if len(msg) > 0:
#             if msg.startswith(":s"):
#                 msg.strip()
#                 split_string = msg.split(' ', 1)
#                 if len(split_string) == 1:
#                     path = "log.txt"
#                 else:
#                     path = split_string + "\\log.txt"
#                 f = open(path, 'w')
#                 for message in chat_log:
#                     f.write("{}: {}\n".format(message[0], message[1]))
#                 f.close()
#                 print("Log file saved!")
#             elif msg == ":q":
#                 handler.close()
#                 asyncore.close_all()
#                 return
#             else:
#                 handler.push(bytes("MESSAGE " + json.dumps(dict([("username", handler.get_username()),
#                                                                  ("message", msg)])) + "\0", 'UTF-8'))
#                 chat_log.append((handler.get_username(), msg))
#         msg = ""


class Client(asynchat.async_chat):

    def __init__(self, host, port, view_mode):
        asynchat.async_chat.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        self.set_terminator(b'\0')
        self._received_data = ""
        self._username = ""
        self. _user_input_thread= threading.Thread(target=controller.user_input, args=(self, msg, chat_log,))
        self._view_mode = view_mode
        if view_mode == "user":
            import user_view as view
        else:
            import agent_view as view
            self._keyword = ""
            self._info = ""
        self._view = view.View()

    def handle_connect(self):
        while self._username == "":
            self._username = input("Please enter username: ")
            if self._username == "":
                print("Username cannot be empty.")
        self.push(bytes("SET_USERNAME " + self._username + "\0", 'UTF-8'))
        if self._view_mode == "user":
            json_data = controller.get_user_info()
            self.push(bytes("COMMAND " + json_data + "\0", 'UTF-8'))
            print("Waiting for agent to enter chat room...")
        elif self._view_mode == "agent":
            print("Waiting for client to enter information...")

    def collect_incoming_data(self, data):
        self._received_data += data.decode('UTF-8')

    def found_terminator(self):
        self._received_data.strip('\0')
        split_string = self._received_data.split(' ', 1)
        key = split_string[0]
        # print(self._received_data)
        if key == "CHAT_START":
            self._user_input_thread.start()
        elif key == "COMMAND":
            data = split_string[1]
            json_data = json.loads(data)
            self._view.print_user_info(json_data)
            input("Please press enter to start chat with the user.")
            self.push(bytes("CHAT_START\0", 'UTF-8'))
        elif key == "MESSAGE":
            data = split_string[1]
            json_data = json.loads(data)
            # print("\r{}: {}\n{}: ".format(json_data["username"], json_data["message"], self._username), end='')
            self._view.print_message(json_data)
            chat_log.append((json_data["username"], json_data["message"]))
        elif key == "ROOM_FULL":
            input("We're sorry.  Our agent is currently occupied with another customer.  Please press enter to close this chat client")
            self.close()
        self._received_data = ""

    def get_username(self):
        return self._username


def check_ip_addr(ip_addr):
    try:
        socket.inet_pton(socket.AF_INET, ip_addr)
        return True
    except socket.error:
        return False

def main():
    # client = Client("localhost", 8888)
    ip_addr = ""
    while not check_ip_addr(ip_addr):
        ip_addr = input("Please input server's IP address: ")
    port = ""
    while not port.isdigit():
        port = input("Please input server's port: ")
    view_mode = ""
    while view_mode != "user" and view_mode != "agent":
        view_mode = input("Please enter if you're a user or agent: ")
    client = Client(ip_addr, int(port), view_mode)
    asyncore.loop(timeout=1)


if __name__ == "__main__":
    main()
