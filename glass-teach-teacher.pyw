from os import listdir, chdir
from os.path import isfile
import socket

def glass_teach_teacher():
    
    # Location that files will be pulled from/pushed to
    LOCAL_DIR = '/home/daniel/Desktop/testfolder/'
    chdir(LOCAL_DIR)
    monitor_off_proc = ''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # assume VPS is up and running at this point
    s.connect(('54.187.236.208', 8080))
    print('connected')
    # ident packet
    s.send('teacher\00\00\00')
    # loop
    while True:
        op = s.recv(128)
        ops = op[:op.index('\00')].split('=')
        print('recv op')

        # send back a list of the contents of LOCAL_DIR
        if 'file-dir' == ops[0]:
            print('recv file-dir command, building list to return')
            # build a list of files in the directory, prepare a string to send back
            dir_contents = listdir(LOCAL_DIR)
            dir_string = 'file-dir='
            for f in dir_contents:
                if isfile(f):
                   dir_string = dir_string + f + '\01'
                else:
                   dir_string = dir_string + '\02' + f + '\01'
            dir_string = dir_string[:(len(dir_string) -  1)]
            print('length of list, pre padding: ' + str(len(dir_string)))
            while len(dir_string) < 1024:
                dir_string = dir_string + '\00'
            s.send(dir_string)
        
        # stream the file specified back in 2048 byte packets
        elif 'file-push' == ops[0]:
            f = open(ops[1])
            # 2038 to account for file-push= length, so server knows what it is recv
            file_data = 'file-push=' +  f.read(2038)
            while len(file_data) == 2048:
                s.send(file_data)
                file_data = f.read(2048)
            # append null bytes until last packet is the right length
            while len(file_data) < 2048:
                file_data = file_data + '\00'
            s.send(file_data)
            
if __name__ == '__main__':
    glass_teach_teacher()
