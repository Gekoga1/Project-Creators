import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = '192.168.2.2'
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))


if __name__ == '__main__':
    while True:
        command = input('command: ').lower()
        if command == 'register':
            send("!REGISTRATION")
            send(';'.join([input('name: '), input('password: ')]))
        if command == 'login':
            send("!LOGIN")
            send(';'.join([input('name: '), input('password: ')]))
            print(client.recv(2048).decode(FORMAT))
        elif command == 'disconnect':
            send(DISCONNECT_MESSAGE)
            break
