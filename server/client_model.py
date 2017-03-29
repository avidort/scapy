class ClientModel:
    def __init__(self, ip_address, name):
        self.ip_address = ip_address
        self.name = name
        self.__message_queue = []

    def push_message(self, message):
        print '[debug] pushing ' + message
        self.__message_queue.append(message)

    def pop_message(self, message):
        self.__message_queue.remove(message)

    def get_messages(self):
        return self.__message_queue
