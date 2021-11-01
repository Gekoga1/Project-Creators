import socket
import pickle


HEADER = 64
PORT = 41480
FORMAT = 'utf-8'
SERVER = '192.168.1.207'
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    try:
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)    # msg with length of next msg
        client.send(message)
    except ConnectionError:
        raise SystemExit


def send_bytes(msg):
    try:
        msg_length = len(msg)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)  # msg with length of next msg
        client.send(msg)
    except ConnectionError:
        raise SystemExit


def receive():
    try:
        while True:
            msg_length = client.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = client.recv(msg_length).decode(FORMAT)
                return msg
    except ConnectionError:
        raise SystemExit


def receive_bytes():
    try:
        while True:
            msg_length = client.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = client.recv(msg_length)
                return msg
    except ConnectionError:
        raise SystemExit


def create_character():
    send_bytes(pickle.dumps([input("Name of OC: "), 35, 35, 15, 15, [1, 1, 1, 1, 1, 1, 1, 1], None, None, []], 3))
