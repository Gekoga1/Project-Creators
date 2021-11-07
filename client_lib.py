import socket
import pickle
import sys
import base64
import time
from math import ceil
from collections import defaultdict
import threading


HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
SERVER = input("Server IP.v4: ")
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
        if client.recv(2).decode(FORMAT) == "!1":
            pass
        else:
            print("error")
    except ConnectionError:
        raise SystemExit


def send_bytes(msg):
    try:
        msg_length = len(msg)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)  # msg with length of next msg
        time.sleep(0.1)
        client.send(msg)
        if client.recv(2).decode(FORMAT) == "!1":
            pass
        else:
            print("error")
    except ConnectionError:
        raise SystemExit


def receive():
    try:
        while True:
            msg_length = client.recv(HEADER)
            msg_length = msg_length.decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = client.recv(msg_length).decode(FORMAT)
                client.send("!1".encode(FORMAT))
                return msg
    except ConnectionError:
        raise SystemExit


def receive_int():
    try:
        while True:
            msg = client.recv(1)
            msg = msg.decode(FORMAT)
            client.send("!1".encode(FORMAT))
            return msg
    except ConnectionError:
        raise SystemExit


def receive_bytes():
    try:
        while True:
            msg_length = client.recv(HEADER).decode(FORMAT)
            time.sleep(0.1)
            if msg_length:
                msg_length = int(msg_length)
                msg = client.recv(msg_length)
                time.sleep(0.1)
                client.send("!1".encode(FORMAT))
                print("!1")
                return msg
    except ConnectionError:
        raise SystemExit


def create_character():
    send_bytes(pickle.dumps([input("Name of OC: "), 35, 35, 15, 15, [1, 1, 1, 1, 1, 1, 1, 1], None, None, []], 3))
