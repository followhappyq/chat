from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

clients = {}
addresses = {}


addr = ('localhost', 8686)
server = socket(AF_INET, SOCK_STREAM)
server.bind(addr)


def accept_connection():
    while True:
        client, clients_address = server.accept()
        print(clients_address, ":has connected")
        client.send(b'give your name', 'utf8')
        addresses[client] = clients_address


def handle_client(client): #takes client socket as argument
    name = client.recv(1024).decode("utf8")
    message = "Hello, if you want quit, just write {quit}"
    client.send(bytes(message, "utf8"))
    msg = "{0} has joined the chat!".format(name)
    send_message(bytes(msg, "utf8"))
    clients[client] = name
    while True:
        msg = client.recv(1024)
        if msg != bytes("{quit}", "utf8"):
            send_message(msg, name + ": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            send_message(bytes("%s has left the chat." % name, "utf8"))
            break


def send_message(msg, prefix=""):  # prefix is for name identification.
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)


if __name__ == "__main__":
    server.listen(3)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_connection())
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    server.close()