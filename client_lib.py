import socket
import pickle


HEADER = 64
PORT = 41480
FORMAT = 'utf-8'
SERVER = '25.73.197.223'
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg, count=0):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)    # msg with length of next msg
    client.send(message)
    if client.recv(2048).decode(FORMAT) == "Msg received":  # receiving test
        pass
    else:
        count += 1
        if count == 11:
            print('Something wrong with connection')
            raise SystemExit
        send(msg, count)


def send_bytes(msg, count=0):
    msg_length = len(msg)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)  # msg with length of next msg
    client.send(msg)
    if client.recv(2048).decode(FORMAT) == "Msg received":  # receiving test
        pass
    else:
        count += 1
        if count == 11:
            print('Something wrong with connection')
            raise SystemExit
        send_bytes(msg, count)


def reception_response() -> None:
    client.send("Msg received".encode(FORMAT))


def receive():
    while True:
        msg_length = client.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = client.recv(msg_length).decode(FORMAT)
            reception_response()
            return msg


def receive_bytes():
    while True:
        msg_length = client.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = client.recv(msg_length)
            reception_response()
            return msg


def create_character():
    send_bytes(pickle.dumps([input("Name of OC: "), 35, 35, 15, 15, [1, 1, 1, 1, 1, 1, 1, 1], None, None, []], 3))
