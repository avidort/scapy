class ClientModel:
    def __init__(self, name, ip_address):
        self.__name = name
        self.__ip_address = ip_address
        self.__message_queue = []

    def push_message(self, message):
        print 'pushing ' + message
        self.__message_queue.append(message)

    def pop_message(self, message):
        self.__message_queue.remove(message)

    def get_messages(self):
        return self.__message_queue