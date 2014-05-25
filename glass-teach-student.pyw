import socket
from subprocess import Popen
from os import chdir


def glass_teach_student():
    LOCAL_DIR = 'this/is/the/local/dir'
    chdir(LOCAL_DIR)
    monitor_off_proc = ''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # assume VPS is up and running at this point
    s.connect(('54.187.236.208', 8080))
    print('connected')
    # ident packet
    s.send('student\00\00\00')
    # loop
    while 1:
        op = s.recv(128)
        ops = op[:op.index('\00')].split('=')
        if ops[0] == 'monitor':
            if ops[1] == 'off':
                print('monitor off')
                monitor_off_proc = Popen(['glass-teach.exe'])
            if ops[1] == 'on':
                print('monitor on')
                monitor_off_proc.terminate()
        elif ops[0] == 'file-push':
            f = open(ops[1])
            file_data = s.recv(2048)
            while '\00' not in file_data:
                f.write(file_data)
                file_data = s.recv(2048)
            file_data = file_data[:file_data.index('\00')]
            f.write(file_data)
            f.flush()
            f.close()

if __name__ == '__main__':
    glass_teach_student()
