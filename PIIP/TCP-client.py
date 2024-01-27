# https://www.geeksforgeeks.org/socket-programming-python/
# https://stackoverflow.com/questions/2719017/how-to-set-timeout-on-pythons-socket-recv-method
from socket	import *

# Create a socket object 
with socket() as s:
    s.settimeout(1.0)
    try:
        # Reserving a port
        port = 12345			

        # Connecting to the server
        s.connect(('127.0.0.1', port)) 

        s.send('zażółcą nóż jaźwców...'.encode())
        # Receiving data from the server
        # and decoding to get the string.
        print(s.recv(0x100).decode())
        # close the connection (once and for all)
        s.close()
    except:
        print('Connection problem!')