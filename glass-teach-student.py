import socket

def glass_teach_student():
    monitor_off_proc = ''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # assume VPS is up and running at this point
    s.connect(('54.187.236.208', 8080))
    print('connected')
    # ident packet
    s.send('student~~~')
    # loop
    while 1:
        op = s.recv(128)
        ops = op[:op.index('~')].split('=')
        if ops[0] == 'monitor':
            if ops[1] == 'off':
                print('monitor off')
                monitor_off_proc = Popen(['glass-teach.exe'])
            if ops[1] == 'on':
                print('monitor on')
                monitor_off_proc.terminate()

if __name__ == '__main__':
    glass_teach_student()
