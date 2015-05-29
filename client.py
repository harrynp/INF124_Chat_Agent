__author__ = 'Harry'

import asyncore
import asynchat
import socket
import json
import threading
import controller

msg = ""
chat_log = []


class Client(asynchat.async_chat):

    def __init__(self, host, port, view_mode):
        asynchat.async_chat.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        self.set_terminator(b'\0')
        self._received_data = ""
        self._username = ""
        self._user_input_thread_running = False
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
        self.push(bytes("SET_VIEW {}\0".format(self._view_mode), 'UTF-8'))
        while self._username == "":
            self._username = input("Please enter username: ")
            if self._username == "":
                print("Username cannot be empty.")
        self.push(bytes("SET_USERNAME {}\0".format(self._username), 'UTF-8'))
        # if self._view_mode == "user":
        #     json_data = controller.get_user_info()
        #     self.push(bytes("COMMAND {}\0".format(json_data), 'UTF-8'))
        #     print("Waiting for agent to enter chat room...")
        # elif self._view_mode == "agent":
        #     print("Waiting for client to enter information...")

    def collect_incoming_data(self, data):
        self._received_data += data.decode('UTF-8')

    def found_terminator(self):
        self._received_data.strip('\0')
        split_string = self._received_data.split(' ', 1)
        key = split_string[0]
        # print(self._received_data)
        if key == "CHAT_START":
            controller.chat_open = True
            if not self._user_input_thread_running:
                self._user_input_thread.start()
                self._user_input_thread_running = True
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
            self._view.print_message(json_data, self._username)
            chat_log.append((json_data["username"], json_data["message"]))
        elif key == "ROOM_FULL":
            print("We're sorry.  Our agent is currently occupied with another customer.  Please wait...")
        elif key == "ROOM_ENTER":
            if self._view_mode == "user":
                json_data = controller.get_user_info(self._username)
                self.push(bytes("COMMAND {}\0".format(json_data), 'UTF-8'))
                print("Thank you for waiting.  Our agent is now ready to chat with you.  Please wait for agent to start the chat.")
            elif self._view_mode == "agent":
                print("Waiting for client to enter information...")
            # self._user_input_thread.start()
        elif key == "AGENT_ALREADY_IN_ROOM":
            input("An agent is already connect.  Please press enter to close.")
            self.close()
        elif key == "NO_AGENT":
            print("\rWe're sorry.  Our agent is currently not connected to the chat room right now.  Please input :q to quit.\n{}: ".format(self._username))
            controller.chat_open = False
            self.close()
        elif key == "ROOM_LEAVE":
            username = split_string[1]
            print("\r{} has left the room".format(username))
            controller.chat_open = False
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
