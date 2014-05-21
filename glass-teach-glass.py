import socket
import time


def glass_teach_glass():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # assume VPS is up and running at this point
    s.connect(('54.187.236.208', 8080))
    print('connected')
    # ident packet
    s.send('glass~~~~~')

    # debug test code
    op = 'monitor=off'
    op = op + "".join(['~' for i in range(128 - len(op))])
    s.send(op)
    time.sleep(1)
    op = 'monitor=on'
    op = op + "".join(['~' for i in range(128 - len(op))])
    s.send(op)

    # loop
    while 1:
        s.recv(128)

if __name__ == '__main__':
    glass_teach_glass()
