import argparse
import socket

MAX_BYTES = 65535


def server(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", port))
    while True:
        data, address = sock.recvfrom(MAX_BYTES)
        receivedText = data.decode('ascii')
        if(len(receivedText) % 2 == 0):
            dataWillSend = 'Received data size is {}'.format(
                len(receivedText)).encode('ascii')
            sock.sendto(dataWillSend, address)
        else:
            dataWillSend = "Error 403 Forbidden".encode('ascii')
            sock.sendto(dataWillSend, address)


def client(port, data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(data.encode('ascii'), ('127.0.0.1', port))
    data, address = sock.recvfrom(MAX_BYTES)
    print(data.decode('ascii'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    choices = {'client': client, 'server': server}
    parser.add_argument('role', choices=choices)
    parser.add_argument('-p', metavar='PORT', type=int, default=1060)
    parser.add_argument('-d', metavar='DATA', type=str, default='Hello World')
    args = parser.parse_args()

    function = choices[args.role]
    if(args.role == 'client'):
        function(args.p, args.d)
    else:
        function(args.p)
