import socket

def glass_teach_client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('ec2-54-187-236-208.us-west-2.compute.amazonaws.com', 8080))
    print('connected')

if __name__ == '__main__':
    glass_teach_client()
