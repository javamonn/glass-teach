import socket


def glass_teach_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((socket.gethostname(), 38300))
    server_socket.listen(5)
    while 1:
        (client_socket, address) = server_socket.accept()
        print('accepted connection from: ' + str(address) + '\n') 


if __name__ == '__main__':
    glass_teach_server()
