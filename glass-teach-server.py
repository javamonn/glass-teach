import socket
import select
from time import sleep

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
#       2) Server sends packet to teacher socket 'file-pull=student-count' so teacher socket knows how many full files to anticipate. Server echos
#          the 'file-pull=file-name' packet to each of the student sockets. Student sockets will look for a file containing the name they recv, the actual
#          name of the student file will be different, as it will contain the student's name.
#       3) Student sockets will initially send back a packet of length 128 containing 'file-pull=acutal-file-name', which the server will echo to the teacher
#          socket. This is done so the teacher socket knows what the name of the file it is recv is.
#       4) After the initial 128 len packet, the student will send the file in 2048 byte chunks
#       5) Server iterates over the student sockets, echoing the complete file for each student socket to the teacher, ie, it echos all 2048 len packets from one
#          socket before echoing more packets from the next packet.

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
                print('new connection from: ' + str(address))
                new_socket.settimeout(None)
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
                        s.settimeout(.5)
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
                elif 'file-push' in op:
                    print('preparing file-push command')
                    # echo packet to teacher (to find and begin transfering file) and students (to begin listening for the file
                    teacher_socket.send(op)
                    for s in student_sockets:
                        s.send(op)
                    # as we begin to recv the file stream from teacher, echo it to all of the students
                    file_data = teacher_socket.recv(2048)
                    while True:
                        for sock in student_sockets:
                            sock.send(file_data)
                        if '\00' not in file_data:
                            file_data = teacher_socket.recv(2048)
                        else:
                            break
                elif 'file-pull' in op:
                    print('preparing file-pull command')
                    # send to teacher a packet containing the file-pull op and the number of student sockets
                    teacher_packet = 'file-pull=' + str(len(student_sockets))
                    while len(teacher_packet) < 128:
                        teacher_packet = teacher_packet + '\00'
                    teacher_socket.send(teacher_packet)
                    for student in student_sockets:
                        student.send(op)
                    # iterate over student sockets, echoing the file streams to the teacher socket as we recieve them 
                    for student in student_sockets:
                        # fetch and echo actual name of file before beginning stream
                        file_title = student.recv(128)
                        teacher_socket.send(file_title)
                        file_data = student.recv(2048)
                        while True:
                            teacher_socket.send(file_data)
                            if '\00' not in file_data:
                                file_data = student.recv(2048)
                            else:
                                break
                # retrieve a list of files/folders in the current directory
                elif 'file-dir' in op:
                    print('echoing file-dir command')
                    print('op length: ' + str(len(op)))
                    teacher_socket.send(op)

                elif 'video-store' in op:
                    print('preparing video-store command')
                    teacher_socket.send(op)
                    file_byte_count = int(op[op.rfind('='):])
                    print('total bytes to echo: ' + file_byte_count)
                    while file_byte_count > 2048:
                        op = glass_socket.recv(2048)
                        teacher_socket.send(op)
                        file_byte_count = file_byte_count - 2048
                    # echo leftover bytes
                    print('leftover bytes: ' + str(file_byte_count))
                    op = glass_socket.recv(file_byte_count)
                    teacher_socket.send(op)
                    print('done echoing video store')

            # file dir and file-push read data from teacher socket
            elif s == teacher_socket:
                op = s.recv(2048)
                if 'file-dir' in op:
                    print('begin echoing file-dir back to glass')

                    # send a ping to see which student sockets are still connected 
                    for sock in student_sockets:
                        ping = 'ping=ping'
                        while len(ping) < 128:
                            ping = ping + '\00'
                        try:
                            sock.send(ping)
                            res = sock.recv(128)
                            if 'ping' in res:
                                continue
                            else:
                                student_sockets.remove(sock)
                        except:
                            student_sockets.remove(sock)

                    # send back the number of student sockets connected
                    glass_socket.send(str(len(student_sockets)) + '\01')
                    # start echoing data back to glass, send until we see a '\00'
                    glass_socket.send(op)
                    # glass socket is java, newlines help delimit
                    glass_socket.send('\r\n')
            elif s in student_sockets:
                student_sockets.remove(s)
                            
if __name__ == '__main__':
    while True:
        try:
            glass_teach_server()
        except:
            print('server failed, about to try again')
            sleep(5)
