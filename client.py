import sys
import atexit

from client_lib import *


def exit_handler():
    send("!DISCONNECT")


def handle_game():
    while True:
        receivation = receive()
        if receivation == "!GAME_END":
            break
        elif receivation == "!INPUT":
            action = input(receive())
            send(action)
        else:
            print(receivation)


if __name__ == '__main__':
    atexit.register(exit_handler)
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
        elif command[:11] == 'create room' and len(command) > 11 and int(command[12:]) > 1:
            send("!CREATE_ROOM")
            send(command[12:])
            while True:
                print(receive())
                handle_game()
        elif command == 'connect room':
            send("!CONNECT_ROOM")
            answer = receive()
            if answer == "!True":
                print(receive())
                handle_game()
            elif answer == "!False":
                print(receive())
