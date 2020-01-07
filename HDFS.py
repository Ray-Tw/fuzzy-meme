#-*-coding: utf-8-*-

import socket
import sys
import cv2
import os 
import numpy as np
import threading
import warnings
warnings.simplefilter("ignore", DeprecationWarning) #fromstring is deprecated

def recvall(s, recv_size):
    recv_buffer = []
    while 1:
        data = s.recv(recv_size - len(recv_buffer))
        if not data:
            break
        recv_buffer.extend(data)
        if len(recv_buffer) >= recv_size:
            break

    return recv_buffer

def service(client_socket, file_name, client_number):
    c = 0
    print(client_socket)
    num_frame = int(client_socket.recv(16).decode('utf-8'))

    file_name = file_name[:file_name.find('.')]
    directory = '/HW2/frame'+str(client_number)
    os.chdir('/HW2')
    f_handler=open(str(client_number)+ '_' + str(file_name)+ '.txt', 'w')

    while( c < num_frame ): #total num of frame
        length = int(client_socket.recv(16).decode('utf-8'))
        print('frame size : '+ str(length)) #277090

        frame = np.array(recvall(client_socket, length))
        npframe = np.fromstring(frame, 'uint8')
        img_np  = cv2.imdecode(npframe, cv2.IMREAD_COLOR) # cv2.IMREAD_COLOR
        

        detect = client_socket.recv(16).decode('utf-8')
        print("frame number: "+ str(c) + "detect: " + str(detect))
        os.chdir(directory)
        cv2.imwrite( str(c)+'.jpg' , img_np)

        if int(detect) == 1:
            f_handler.write(str(c)+'\n')
            f_handler.flush()
        c += 1

    f_handler.close() #The end of this client's service.
    print("thread " + str(client_number) + " DONE!")
    return 0

if __name__ == '__main__':
    hdfs_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    hdfs_ip='172.31.6.99'
    port = 7785
    hdfs_socket.bind( (hdfs_ip, port) )
    hdfs_socket.listen(10)
    print("start listening -- ")

    cn = 0
    while(cn < 5):

        client_socket,addr = hdfs_socket.accept() #wait to accept a connection - blocking call
        #print('Connect Successfully\n' + str(addr))
        #multi thread
        file_name_raw = client_socket.recv(16) #ljust(16)
        file_name = str(file_name_raw.decode('utf-8'))
        #file_name = bytes(recvall(client_socket, 64)).decode('utf-8')

        cn += 1
        if(cn == 5):
            service(client_socket, file_name, cn) 
        else:
            client_thread = threading.Thread(target = service, args = (client_socket, file_name, cn))
            client_thread.start()
        