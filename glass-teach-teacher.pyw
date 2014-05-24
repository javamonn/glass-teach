
from os import listdir
from os.path import isfile
import socket

def glass_teach_teacher():
    
    # Location that files will be pulled from/pushed to
    LOCAL_DIR = '/home/daniel/Desktop/testfolder/'
    
    monitor_off_proc = ''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # assume VPS is up and running at this point
    s.connect(('54.187.236.208', 8080))
    print('connected')
    # ident packet
    s.send('teacher\00\00\00')
    # loop
    while 1:
        op = s.recv(128)
        ops = op[:op.index('\00')].split('=')
        if 'file-dir' == ops[0]:
            print('recv file-dir command, building list to return')
            # build a list of files in the directory, prepare a string to send back
            dir_contents = listdir(LOCAL_DIR)
            dir_string = ''
            for f in dir_contents:
                if isfile(f):
                    dir_string = dir_string + f.name.rfind('/') + '\01'
                else:
                    dir_string = dir_string + '\02' + f.name.rfind('/') + '\01'
            dir_string = dir_string[:dir_string.length -  1]
            print('length of list, pre padding: ' + str(dir_string.length))
            while dir_string.length < 1024:
                dir_string = 'file-dir=' +  dir_string + '\00'
            s.send(dir_string)

        if 'file-push' == ops[0]:
            file_name = ops[1]

if __name__ == '__main__':
    glass_teach_teacher()
