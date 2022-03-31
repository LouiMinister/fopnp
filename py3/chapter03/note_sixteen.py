import argparse
import socket


def recvall(sock, length):
    recvdData = b''
    while len(recvdData) < length:
        more = sock.recv(length - len(recvdData))
        if not more:
            raise EOFError('was expecting %d bytes but only received'
                           ' %d bytes before the socket closed'
                           % (length, len(recvdData)))
        recvdData += more
    return recvdData


def client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print('Client has been assigned socket name', sock.getsockname())
    sock.sendall(b'Hi there, server')
    reply = recvall(sock, 16)
    print('The server said', repr(reply))
    sock.close()


def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((interface, port))
    sock.listen(1)
    print('Listening at', sock.getsockname())
    while True:
        print('Wating to accept a new connection')
        sc, sockname = sock.accept()
        print('We have accept a connection from', sockname)
        print(' Socket name:', sc.getsockname())
        print(' Socket peer:', sc.getpeername())
        message = recvall(sc, 16)
        print(' Incoming sixteen-octet message:', repr(message))
        sc.sendall(b'Farewell, client')
        sc.close()
        print(' Reply sent, socket closed')


if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser()
    parser.add_argument('role', choices=choices)
    parser.add_argument('host')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060)
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)
