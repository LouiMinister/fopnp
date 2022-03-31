import socket
import ssl
from urllib.parse import quote_plus

request_text = """\
GET /iss-pass.json?lat={}&lon={} HTTP/1.1\r\n\
Host: api.open-notify.org\r\n\
User-Agent: 20170517\r\n\
Connection: close\r\n\
\r\n\
"""


def whenIssFly(coords):
    sock = socket.socket()
    sock.connect(('api.open-notify.org', 80))

    request = request_text.format(coords['lat'], coords['lon'])
    sock.sendall(request.encode('ascii'))
    raw_reply = b''
    while True:
        more = sock.recv(4096)
        if not more:
            break
        raw_reply += more
    print(raw_reply.decode('utf-8'))
    print(raw_reply)


if __name__ == '__main__':
    coords = {'lat': 45, 'lon': 180}
    whenIssFly(coords)
