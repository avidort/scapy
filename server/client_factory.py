import client_model
client_registry = {}


def add(ip_address, name):
    client_registry[ip_address] = client_model.ClientModel(ip_address, name)


def remove(ip_address):
    del client_registry[ip_address]


def message(ip_address, text):
    print "[debug] sending to {0}: {1}".format(client_registry[ip_address].name, text)
    client_registry[ip_address].push_message(text)


def message_all(text):
    for client in client_registry:
        message(client, text)
