class View():

    def print_user_info(json_data):
        print("\r{}: {}\n{}: ".format(json_data["username"],
                                      json_data["message"],
                                      end='')
              )

    def print_message(json_data):
        print(json_data["message"])
