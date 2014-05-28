from os import listdir, chdir
from os.path import isfile
import socket
from time import sleep

def glass_teach_teacher():
    
    # Location that files will be pulled from/pushed to
    LOCAL_DIR = '/home/daniel/Documents/teacherFolder/'
    chdir(LOCAL_DIR)
    monitor_off_proc = ''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # assume VPS is up and running at this point
    s.connect(('54.187.236.208', 8080))
    print('connected')
    s.settimeout(None)
    # ident packet
    s.send('teacher\00\00\00')
    # loop
    while True:
        op = s.recv(128)
        ops = op[:op.index('\00')].split('=')

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
            while len(dir_string) < 2048:
                dir_string = dir_string + '\00'
            s.send(dir_string)
        
        # stream the file specified back in 2048 byte packets
        elif 'file-push' == ops[0]:
            print('recv file-push command, opening: ' + ops[1])
            f = open(ops[1])
            file_data = f.read(2048)
            print('data read first: ' + file_data)
            while len(file_data) == 2048:
                print('read iteration')
                s.send(file_data)
                file_data = f.read(2048)
            # append null bytes until last packet is the right length
            while len(file_data) < 2048:
                file_data = file_data + '\00'
            print('final packet sent: ' + file_data)
            print('final packet len: ' + str(len(file_data)))
            s.send(file_data)
            f.close()

        # pull files from every student's computer 
        elif 'file-pull' == ops[0]:
            student_count = ops[1]
            print('student count: ' + student_count)
            op = s.recv(128)
            ops = op[:op.index('\00')].split('=')
            chdir(LOCAL_DIR + ops[1][1:])

            for i in range(int(student_count)):
                # fetch the name of this file first
                file_name = s.recv(128)
                print('packet recv: ' + file_name)
                print('packet len: ' + str(len(file_name)))
                name = file_name[(file_name.index('=') + 1):file_name.index('\00')]
                print('file_name: ' + name)
                f = open(name, 'w+')
                # fetch data 
                file_data = s.recv(2048)
                while '\00' not in file_data:
                    f.write(file_data)
                    file_data = s.recv(2048)
                file_data = file_data[:file_data.index('\00')]
                f.write(file_data)
                f.close()
            chdir(LOCAL_DIR)
            print('finished file pull')
        # store a video on the teacher computer 
        elif 'video-store' == ops[0]:
            print('preparing video store command')
            f = open(ops[1], 'w+')
            file_byte_count = int(ops[2])
            print('total bytes to write: ' + str(file_byte_count))
            packet_count = 0
            while file_byte_count > 2048:
                file_data = s.recv(2048)
                f.write(file_data)
                file_byte_count = file_byte_count - 2048
                packet_count = packet_count + 1
            # write leftover bytes
            print('leftover bytes: ' + str(file_byte_count))
            file_data = s.recv(file_byte_count)
            f.write(file_data)
            f.close()
            print('finished video store command ' + str(packet_count))
            

if __name__ == '__main__':
   glass_teach_teacher()
   # while True:
   #     try:
   #         glass_teach_teacher()
   #     except:
   #         print('unable to connect to server')
   #         sleep(5)
