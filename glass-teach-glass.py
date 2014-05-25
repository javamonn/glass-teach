import socket
from subprocess import Popen
from os import chdir, listdir


def glass_teach_student():
    LOCAL_DIR = 'this/is/the/local/dir'
    chdir(LOCAL_DIR)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # assume VPS is up and running at this point
    s.connect(('54.187.236.208', 8080))
    print('connected')
    # ident packet
    s.send('glass\00\00\00\00\00')
    # push file testing
    push_string = 'file-push=test-file1.txt'
    while len(push_string) < 128:
        push_string = push_string + '\00'
    s.send(push_string)


if __name__ == '__main__':
    glass_teach_student()
