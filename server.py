import socket
import threading
import os 
import base64

bind_ip = '0.0.0.0'
bind_port = 9997

#Define the usage protocol as UDP
server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
 
#Configure the listening IP and port
server.bind((bind_ip,bind_port))
filename = "file.txt"
with open(filename, 'rb') as file:
    while True:
        # Receive the request
        data, client_address = server.recvfrom(1024)
        request = data.decode()
        if request.startswith('FILE'):
            # decode
            _, file_name, _, start, _, end = request.split()
            start_byte = int(start)
            end_byte = int(end)
            
            # read the special part
            file.seek(start_byte)
            file_data = file.read(end_byte - start_byte + 1)
            encoded_data = base64.b64encode(file_data).decode()

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