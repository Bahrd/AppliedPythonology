## https://docs.python.org/3/howto/sockets.html
# https://wiki.python.org/moin/UdpCommunication
# https://stackoverflow.com/questions/6289474/working-with-utf-8-encoding-in-python-source
from socket import *

ip, port = '127.0.0.1', 5005
with socket(AF_INET, SOCK_DGRAM) as sock:# Internet, UDP
    sock.bind((ip, port))
    sock.settimeout(10.0)

    while True:
        try:
            data, addr = sock.recvfrom(0x100)               # wait for data
            print(f'{addr} [UDP] => {data.decode()}')       # utf-8 decoding
            sock.sendto('Żarna żytnie...'.encode(), addr)   # echo back
        except IOError:
            print('OIOI error!')
            break
        except KeyboardInterrupt:
            print('♪♫It''s a wrong key, my friend...♫♪')
            break