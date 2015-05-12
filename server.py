__author__ = 'Harry'

import asyncore
import asynchat
import socket
import json
import urllib.request
import traceback

clients = {}
room = []

class MessageHandler(asynchat.async_chat):
    def __init__(self, sock, addr):
        asynchat.async_chat.__init__(self, sock=sock, map=clients)
        self.set_terminator(b'\n')
        self._username = ""
        self._received_data = ""

    def handle_close(self):
        pass

    def collect_incoming_data(self, data):
        self._received_data += data.decode('UTF-8')

    def found_terminator(self):
        self._received_data = self._received_data.strip('\n')
        split_string = self._received_data.split(' ', 1)
        key = split_string[0]
        print(self._received_data)
        if key == "SET_USERNAME":
            self._username = split_string[1]
        elif key == "MESSAGE":
            # data = split_string[1]
            # json_data = json.loads(data)
            # for client in clients:
            #     try:
            #         if client != self:
            #             client.push(bytes("MESSAGE " + json.dumps(data) + "\n", 'UTF-8'))
            #     except:
            #         pass
            for client in room:
                if client != self:
                    client.push(bytes(self._received_data + "\n", 'UTF-8'))
                # try:
                #     client.push(bytes(self._received_data + "\n"))
                # except Exception as e:
                #     print(e)
        self._received_data = ""

    # def handle_error(self):
    #     '''Handle any uncaptured error in the core. Overrides asyncore's handle_error
    #     This prevents the server from disconnecting when it use to send something twice
    #     and then disconnect.'''
    #     trace = traceback.format_exc()
    #     try:
    #         print(trace)
    #     except Exception as e:
    #         print('Uncaptured error!' + e)



class Server(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self, map=clients)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
        print("Server started.")
        print("Waiting for connections...")

    def handle_accepted(self, sock, addr):
        print("Incoming conection from {}".format(repr(addr)))
        handler = MessageHandler(sock, addr)
        room.append(handler)


def main():
    # my_ip = json.loads(urllib.request.urlopen('https://api.ipify.org/?format=json'))['ip']
    server = Server("localhost", 8000)
    asyncore.loop(timeout=1, map=clients)



if __name__ == '__main__':
    main()