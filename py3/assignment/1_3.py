import argparse
import random
import socket
import sys


def server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(1)  # passive socket listening.

    while True:
        print("Wating for game start...")
        # active socket created when client try to connect.
        sc, sockname = sock.accept()

        # wating for client send message for starting game.
        msg = sc.recv(1024)
        if(msg.decode('ascii') == "start"):
            print("Game Start!")
            # send game start message to client
            sc.sendall(
                "Game server connection is successful! Guess number between 1 to 10!".encode('ascii'))

            randNum = random.randrange(1, 11)  # random number for guess
            leftTryCnt = 5                    # count left opportunity for client to guess
            while leftTryCnt > 0:
                leftTryCnt -= 1
                msgRecv = sc.recv(1024).decode('ascii')
                if(msgRecv == ''):  # EOF handling
                    break
                guessNum = int(msgRecv)

                # client msg check
                if guessNum == randNum:  # when guess is correct
                    sc.sendall("Congratulations you did it.".encode('ascii'))
                    break
                else:  # when guess is wrong
                    if leftTryCnt == 0:  # when try count is all used
                        sc.sendall("YOU LOSE!".encode('ascii'))
                        break
                    if guessNum > randNum:
                        sc.sendall("You guessed too high!".encode('ascii'))
                    else:
                        sc.sendall("You guessed too small!".encode('ascii'))
                sys.stdout.flush()
            sc.close()  # close socket when game is end


def client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))  # connect to remote
    sock.sendall("start".encode('ascii'))  # send start message

    gameStartMsg = sock.recv(1024).decode('ascii')
    print(gameStartMsg)

    while True:
        try:
            guess = input('number of you guess: ')
            try:
                int(guess)
            except ValueError:  # Exception handling at input is not number
                print("Enter number type value!")
                continue
            sock.sendall(guess.encode("ascii"))

            msg = sock.recv(1024).decode('ascii')
            print(msg)
            # When game is end
            if (msg == 'Congratulations you did it.' or msg == "YOU LOSE!"):
                break
            sys.stdout.flush()
        except KeyboardInterrupt:  # Exception handling at terminal process end
            print("Client is closed by KeyboardInterrupt!")
            break
        except BrokenPipeError:  # Exception handling at server is down
            print("Server is closed")
            break
    sock.close()


if __name__ == '__main__':
    roles = {'client': client, 'server': server}
    parser = argparse.ArgumentParser()
    parser.add_argument('role', choices=roles)
    parser.add_argument('host')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    function = roles[args.role]
    function(args.host, args.p)
