class View():

    def __init__(self):
        pass

    def print_user_info(self, json_data):
        print("Username: {}\nCommand: {}\nInfo: {}".format(json_data["username"],
                                                           json_data["command"],
                                                           json_data["info"]))

    def print_message(self, json_data, username):
        print("\r{}: {}\n{}: ".format(json_data["username"],
                                      json_data["message"],
                                      username), end='')