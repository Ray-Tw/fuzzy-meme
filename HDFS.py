import socket
import sys
import cv2
import os 
import numpy as np
import threading
import time
import warnings
warnings.simplefilter("ignore", DeprecationWarning) #fromstring is deprecated

def recvall(s, recv_size):
    recv_buffer = []
    print(recv_buffer)
    while 1:
        data = s.recv(recv_size - len(recv_buffer))
        print(data)
        if not data:
            break
        recv_buffer.extend(data)
        if len(recv_buffer) >= recv_size:
            break

    return recv_buffer

def service(client_socket, file_name, client_number):
    c = 0

    num_frame = int(client_socket.recv(16).decode('utf-8'))
    directory = '\HW2\frame'+str(client_number)
    f_handler=open(str(client_number)+ '_' + str(file_name)+ '.txt', 'a')
    __console__ = sys.stdout
    while( c < num_frame ): #total num of frame
        length = int(client_socket.recv(16).decode('utf-8'))

        print('frame size : '+ str(length)) #277090

        frame = np.array(recvall(client_socket, length), 'uint8')
        
        
        #frame = client_socket.recv(length)
        #print("frame length : " + str(len(frame)))
        #nparr = np.fromstring(frame, 'uint8')

        img_np = cv2.imdecode(frame, cv2.IMREAD_COLOR) # cv2.IMREAD_COLOR
        #cv2.imshow('img_np', img_np) 
        #cv2.waitKey(0)
        detect = client_socket.recv(16).decode('utf-8')
        #path = 'frame' + str(client_number)
        os.chdir(directory) 
        cv2.imwrite( str(c)+'.jpg' , img_np)

        if int(detect) == 1:
            sys.stdout=f_handler  #print to file.txt
            print(str(c)) #racing condition
        c += 1
        
    f_handler.close() #The end of this client's service.
    sys.stdout = __console__
    #print("thread DONE")
    return 0

if __name__ == '__main__':
    hdfs_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    hdfs_ip=''
    port=7778
    hdfs_socket.bind( (hdfs_ip, port) )
    hdfs_socket.listen(5)
    print("start listening -- ")

    cn = 0
    while(1):

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
        