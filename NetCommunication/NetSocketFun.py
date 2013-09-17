# -*- coding: UTF-8 -*-
NetSocketBufferSize = 8 * 1024

def NetSocketSetOpt(socketfd):
    import socket
    socketfd.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, NetSocketBufferSize)
    socketfd.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, NetSocketBufferSize)

def NetSocketRecv(socketfd,size = 1):
    total_len=0
    total_data=[]
    sock_data=''
    left_size = size
    while total_len<size:
        if left_size > NetSocketBufferSize:
            recv_size = NetSocketBufferSize
        else:
            recv_size = left_size
        sock_data=socketfd.recv(recv_size)
        if not sock_data:
            break
        else:
            total_data.append(sock_data)
        left_size -= len(sock_data)
        total_len += len(sock_data)
    return ''.join(total_data)

def NetSocketSend(socketfd,sendstr):
    data_list = []
    list_len = len(sendstr) / NetSocketBufferSize
    i = -1
    for i in range(list_len):
        data_list.append(sendstr[i * NetSocketBufferSize:(i + 1) * NetSocketBufferSize])
    data_list.append(sendstr[(i + 1) * NetSocketBufferSize:])
    total_size = 0
    for i in range(list_len + 1):
        send_size = 0
        while send_size < len(data_list[i]):
            sock_size = socketfd.send(data_list[i][send_size:])
            if not sock_size:
                return total_size
            send_size += sock_size
        total_size += send_size
    return total_size
    
        