import socket
import select

# ~ some notes about the socket protocol ~
# python scripts running on student and teacher computer will try to connect on boot. after connection, client
# will send a message of length 10 (padded by '.') denoting what is the clients type, ie ['glass', 'student', 'teacher']

def glass_teach_server():
    unclassified_sockets = []
    student_sockets = []
    glass_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    teacher_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setblocking(0)
    server_socket.bind((socket.gethostname(), 8080))
    server_socket.listen(30)
    while 1:
        # See if glass has sent instructions or if new socket is trying to bind. Note that we don't care
        # about writing to anything unless Glass has passed along instructions.
        readable, writable, exceptional = select.select([glass_socket, server_socket] + unclassified_sockets, [], [])
        for s in readable:
            if s is server_socket:
                new_socket, address = s.accept()
                new_socket.setblocking(0)
                print('new connection from: ' + str(address))
                unclassified_sockets.append(new_socket)
            if s in unclassified_sockets:
                # get classification message, assign accordingly
                socket_type = s.recv(10)
                socket_type = socket_type[:socket_type.index('.')]
                print('classification message: ' + str(socket_type))
                if socket_type == 'teacher':
                    teacher_socket = s
                elif socket_type == 'student':
                    student_sockets.append(s)
                elif socket_type == 'glass':
                    glass_socket = s
                unclassified_sockets.remove(s)

if __name__ == '__main__':
    glass_teach_server()
