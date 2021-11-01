from client_lib import *


def handle_game():
    while True:
        receivation = receive()
        if receivation == "!GAME_END":
            print(receive())
            break
        elif receivation == "!INPUT":
            action = input(receive())
            send(action)
        else:
            print(receivation)


def handle_client():
    while True:
        command = input('command: ').lower()

        if command[:11] == 'create room' and len(command) > 11 and int(command[12:]) > 1:
            send("!CREATE_ROOM")
            send(command[12:])
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

        elif command == 'disconnect':
            break


if __name__ == '__main__':
    try:
        while True:

            command = input('command: ').lower()

            if command == 'register':
                send("!REGISTRATION")
                send(';'.join([input('name: '), input('password: ')]))
                answer = receive()

                if answer == "!False":
                    print("Try another Name")
                else:
                    print("You successfully registered")
                    print("You need to create your character")
                    create_character()
                    y_id = int(answer)
                    handle_client()

            elif command == 'login':
                send("!LOGIN")
                send(';'.join([input('name: '), input('password: ')]))
                answer = receive()
                if answer == "!False":
                    print("Where is no such account")
                else:
                    y_id = int(answer)
                    answer = receive()
                    if answer == "!NO_CHAR":
                        print("You need to create your character")
                        create_character()
                        handle_client()
                    else:
                        handle_client()

    except SystemExit:
        send("!DISCONNECT")
