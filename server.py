import socket
import threading
import os 
bind_ip = '0.0.0.0'
bind_port = 9999

#Define the usage protocol as UDP
server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
 
#Configure the listening IP and port
server.bind((bind_ip,bind_port))

def handle_client():
    #If get the data
    #data is the communication content data
    #client is the ip address information of the client（'ip',port）
    data,client = server.recvfrom(1024)
    print('[*]From:%s Received:%s'% (client,data))
    if data.startswith(b'DOWNLOAD'):
        filename = data.decode().split()[1]  # Get the file name
        if os.path.exists(filename):  # Check if the file exists
            file_size = os.path.getsize(filename)  # get the size of the file
            response = f"OK {filename} SIZE {file_size} PORT 50000"  # the information of port and file
            server.sendto(response.encode(), client)
        else:
            response = f"ERR {filename} NOT_FOUND"  # If the file don't exist,return error
            server.sendto(response.encode(), client)
 
#Use multi-threading to impllement the function for obtaining received data and pass in the client parameter
client_handler = threading.Thread(target=handle_client)
client_handler.start()    