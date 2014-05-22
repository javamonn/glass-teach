import socket

def glass_teach_student():
    
    # Location that files will be pulled from/pushed to
    LOCAL_DIR = ''
    
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
        if 'file-push' == ops[0]:
            file_name = ops[1]

if __name__ == '__main__':
    glass_teach_student()
