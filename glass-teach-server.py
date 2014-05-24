import socket
import select

# ~ some notes about the socket protocol ~
#
# python scripts running on student and teacher computer will try to connect on boot. after connection, client
# will send a message of length 10 (padded by '\00') denoting what is the clients type, ie ['glass', 'student', 'teacher']
#
# messages sent by glass will be monitor=off, monitor=on, file-push='filename' file-pull='filename' file-list
# length 128, padded by '\00'
#
# Glass can query teacher program for contents of local dir before file push with a 'file-list' command
#
# protocol implementation:
#   file-dir:
#       1) Glass sends packet 'file-dir' (length 128, padded by \00)  to server.
#       2) Server echoes 'file-dir' (length 128, padded by \00) to teacher-socket.
#       3) Teacher-socket sends back a list of files and folders in the directory.
#          These packets are of length 1024, the first of which has 'file-dir' (so that the server knows what it is recieving), the last
#          packet will be padded by \00. Names will be separated by \01 characters, folders denoted with a prepended \02
#       4) Server is echoing these packets back to Glass as it recieves them
#
#   At this point the glass user will pick a file from the displayed list, glass begins file-push or file-pull protocol
#
#   file-push:
#       1) Glass sends packet 'file-push=file-name' to server
#       2) Server echos packet to teacher-socket and student-sockets
#       3) Teacher socket starts streaming the file back to the server. These packets are of length 2048, the first of which is prepended
#          by a 'file-push' so the server knows what it recieving. The server echos each of these packets to student-sockets, up until the
#          last packet, which is padded by \00
#       4) Server will send back an ack packet when it sees the null delimmitted packet to the glass so glass can initiate another 'file-push'
#          if it needs to transfer an entire folder
#
#   file-pull:
#       1) Glass sends packet 'file-pull=file-name' to server
#       2) Server echos packet to teacher-socket and student-sockets (to prepare for listenting)
#       3) Student-socket looks for file in local directory that contains file_name (it will also contain their name). These sockets will start
#          streaming this file back to the server, packets of length 2048, the last of which will be padded by \00. The first packet sent by each
#          student-socket will contain a 'file-pull=file-name' with the full file name (including student name). Server will build a map of student-socket
#          to recieved file 

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
                    socket_type = socket_type[:socket_type.index('\00')]
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
                # echo monitor command to students, no other data transfer necessary
                if 'monitor' in op:
                    print('sending monitor command')
                    for s in student_sockets:
                        s.send(op)
                # prepare for file push, teacher sends back file data (which we echo to students), students prepare to recv
                if 'file-push' in op:
                    print('preparing file-push command')
                    teacher_socket.send(op)
                    for s in student_sockets:
                        s.send(op)
                # retrieve a list of files/folders in the current directory
                if 'file-dir' in op:
                    print('echoing file-dir command')
                    teacher_socket.send(s)
            # file dir and file-push read data from teacher socket
            elif s == teacher_socket:
                if 'file-dir' in op:
                    print('recv file-dir from teacher socket, echoing back to glass')
                    # start echoing data back to glass, send until we see a '\00'
                    op = recv(1024)
                    while True:
                        glass_socket.send(op)
                        if '\00' not in op:
                            op = recv(1024)
                        else:
                            break
                            
if __name__ == '__main__':
    glass_teach_server()
