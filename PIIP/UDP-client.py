## https://docs.python.org/3/howto/sockets.html
# https://wiki.python.org/moin/UdpCommunication
# https://stackoverflow.com/questions/6289474/working-with-utf-8-encoding-in-python-source
from ast import Try
from socket import *

ip, port = '127.0.0.1', 5005
msg = 'Bieży pyton wąską dróżką'

try:
    print(f'{msg} => {ip}:{port} [UDP]')
    with socket(AF_INET, SOCK_DGRAM) as sock:
        sock.settimeout(1.0)
    
        # Send and wait for a response
        sock.sendto(msg.encode(), (ip, port))
        print(sock.recv(0x100).decode())
except IOError:
    print('Timeout error!')