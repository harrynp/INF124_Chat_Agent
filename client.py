__author__ = 'Harry'

import asyncore
import asynchat
import socket
import json
import threading

msg = ""

def user_input(handler, msg):
    while True:
        msg = input(handler.get_username() + ": ")
        if len(msg) > 0:
            handler.push(bytes("MESSAGE " + json.dumps(dict([("username", handler.get_username()),
                                                             ("message", msg)])) + "\n", 'UTF-8'))
        msg = ""


class Client(asynchat.async_chat):

    def __init__(self, host, port):
        asynchat.async_chat.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        self.set_terminator(b'\n')
        self._received_data = ""
        self._username = ""
        self._user_input_thread = threading.Thread(target=user_input, args=(self, msg,))


    def handle_connect(self):
        while self._username == "":
            self._username = input("Please enter username: ")
            if self._username == "":
                print("Username cannot be empty.")
        self.push(bytes("SET_USERNAME " + self._username + "\n", 'UTF-8'))
        self._user_input_thread.start()

    def collect_incoming_data(self, data):
        self._received_data += data.decode('UTF-8')

    def found_terminator(self):
        self._received_data.strip('\n')
        split_string = self._received_data.split(' ', 1)
        key = split_string[0]
        # print(self._received_data)
        if key == "MESSAGE":
            data = split_string[1]
            json_data = json.loads(data)
            print("{}: {}".format(json_data["username"], json_data["message"]))
        self._received_data = ""

    def get_username(self):
        return self._username



def main():
    # ip_addr = input("Please input server's IP address: ")
    client = Client("localhost", 8000)
    asyncore.loop(timeout=1)


if __name__ == "__main__":
    main()
