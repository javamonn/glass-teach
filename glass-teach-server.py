import socket
import select

# ~ some notes about the socket protocol ~
# python scripts running on student and teacher computer will try to connect on boot. after connection, client
# will send a message of length 10 (padded by '~') denoting what is the clients type, ie ['glass', 'student', 'teacher']
#
# messages sent by glass will be monitor=off, monitor=on, file-push='filename' file-pull='filename' file-list
# length 128, padded by '~'
def glass_teach_server():
    unclassified_sockets = []
    student_sockets = []
    connected_sockets = []
    glass_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    teacher_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setblocking(0)
    server_socket.bind((socket.gethostname(), 8080))
    server_socket.listen(30)
    connected_sockets.append(server_socket)
    while 1:
        # See if glass has sent instructions or if new socket is trying to bind. Note that we don't care
        # about writing to anything unless Glass has passed along instructions.
        readable, writable, exceptional = select.select(connected_sockets, [], [])
        for s in readable:
            if s == server_socket:
                new_socket, address = s.accept()
                new_socket.setblocking(0)
                print('new connection from: ' + str(address))
                unclassified_sockets.append(new_socket)
                connected_sockets.append(new_socket)
            elif s in unclassified_sockets:
                # get classification message, assign accordingly
                socket_type = s.recv(10)
                print('recv from unclassified socket: ' + str(s))
                if socket_type:
                    socket_type = socket_type[:socket_type.index('~')]
                    print('classification message: ' + str(socket_type))
                    if socket_type == 'teacher':
                        print('connected teacher')
                        teacher_socket = s
                    elif socket_type == 'student':
                        print('connected student')
                        student_sockets.append(s)
                    elif socket_type == 'glass':
                        print('connected glass socket')
                        glass_socket = s
                    unclassified_sockets.remove(s)
            elif s == glass_socket:
                op = s.recv(128)
                # we can just echo certain commands to student sockets and let them handle it
                if 'monitor' in op:
                    print('sending monitor command')
                    for s in student_sockets:
                        s.send(op)

if __name__ == '__main__':
    glass_teach_server()
