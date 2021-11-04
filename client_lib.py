import socket
import pickle
import sys
import base64
from math import ceil
from collections import defaultdict
import threading


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
        while not client.recv(48).decode(FORMAT) == "!True":
            pass
    except ConnectionError:
        raise SystemExit


def send_bytes(msg):
    try:
        msg_length = len(msg)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)  # msg with length of next msg
        client.send(msg)
        while not client.recv(48).decode(FORMAT) == "!True":
            pass
    except ConnectionError:
        raise SystemExit


def send_image(image):
    count = ceil(sys.getsizeof(image) / 2048)
    send(str(count))

    for i in range(count):
        if i == count - 1:
            send_bytes(image[2048 * i:])
        else:
            send_bytes(image[2048 * i:2048 * (i + 1)])


def receive():
    try:
        while True:
            msg_length = client.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = client.recv(msg_length).decode(FORMAT)
                client.send("!True".encode(FORMAT))
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
                client.send("!True".encode(FORMAT))
                return msg
    except ConnectionError:
        raise SystemExit


def receive_image():
    book = b''
    for i in range(int(receive())):
        book += receive_bytes()
    return book


def create_character():
    send_bytes(pickle.dumps([input("Name of OC: "), 35, 35, 15, 15, [1, 1, 1, 1, 1, 1, 1, 1], None, None, []], 3))
