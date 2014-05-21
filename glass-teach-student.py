import socket

def glass_teach_student():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # assume VPS is up and running at this point
    s.connect(('54.187.236.208', 8080))
    print('connected')
    s.send('student...')

if __name__ == '__main__':
    glass_teach_student()
