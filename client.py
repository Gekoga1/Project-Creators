from client_lib import *


if __name__ == '__main__':
    while True:
        command = input('command: ').lower()
        if command == 'register':
            send("!REGISTRATION")
            send(';'.join([input('name: '), input('password: ')]))
        elif command == 'login':
            send("!LOGIN")
            send(';'.join([input('name: '), input('password: ')]))
            print(receive())
        elif command == 'disconnect':
            send("!DISCONNECT")
            break
        elif command == 'create room':
            send("!CREATE_ROOM")
            while True:
                print(receive())
        elif command == 'connect room':
            send("!CONNECT_ROOM")
            while True:
                print(receive())
