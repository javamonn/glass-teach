import socket
from subprocess import Popen
from os import chdir, listdir
from time import sleep


monitor = True
monitor_off_proc = ''

def glass_teach_student():
    global monitor
    global monitor_off_proc
    LOCAL_DIR = 'C:\Users\David\Documents\GitHub\glass-teach'
    chdir(LOCAL_DIR)
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
        
        # turn monitors on and off
        if ops[0] == 'monitor':
            if ops[1] == 'off' and monitor:
                print('monitor off')
                monitor_off_proc = Popen(['glass-teach.exe'])
                monitor = False
            elif ops[1] == 'on':
                print('monitor on')
                monitor_off_proc.terminate()
                monitor = True

        # recieve a file from the teacher computer (get assignment)
        elif ops[0] == 'file-push':
            f = open(ops[1], 'w+')
            # Note that first packet originates from glass length 128, then we start getting packets originating from teacher socket
            file_data = s.recv(2048)
            while '\00' not in file_data:
                f.write(file_data)
                file_data = s.recv(2048)
            file_data = file_data[:file_data.index('\00')]
            f.write(file_data)
            f.flush()
            f.close()

        # send a file to the teacher computer (turn in assignment)
        elif ops[0] == 'file-pull':
            # find file to send back the name, then stream
            file_name_return = 'file-pull='
            file_name = ''
            match_file = ops[1][1:]
            print('trying to match: ' + match_file)
            for f in listdir(LOCAL_DIR):
                if match_file in f:
                    file_name = f
                    break
            file_name_return = file_name_return + file_name
            if len(file_name) == 0:
                # student hasn't turned anything in, alert teacher
                file_name_return = file_name_return + 'none'
            while len(file_name_return) < 128:
                file_name_return = file_name_return + '\00'
            s.send(file_name_return)
            # begin streaming file back in len 2048 packets
            if len(file_name) > 0:
                f = open(file_name)
                file_data = f.read(2048)
                while len(file_data) == 2048:
                    s.send(file_data)
                    file_data = f.read(2048)
                # append null bytes until last packet is the right length
                while len(file_data) < 2048:
                    file_data = file_data + '\00'
                s.send(file_data)
                f.close()

        elif ops[0] == 'ping':
            # send back a ping to confirm connection
            ping = 'ping'
            while len(ping) < 128:
                ping = ping + '\00'
            s.send(ping)


if __name__ == '__main__':
    while True:
        try:
            glass_teach_student()
        except:
            print('unable to connect to server')
            sleep(5)
            
