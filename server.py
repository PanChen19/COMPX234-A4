import socket
import threading
 
bind_ip = '0.0.0.0'
bind_port = 9999
 
#Define the usage protocol as UDP
server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
 
#Configure the listening IP and port
server.bind((bind_ip,bind_port))
print('[*]Listening on %s:%d' % (bind_ip,bind_port))
 
 
def handle_client():
    #If get the data
    #data is the communication content data
    #client is the ip address information of the client（'ip',port）
    data,client = server.recvfrom(1024)
    print('[*]From:%s Received:%s'% (client,data))
    server.sendto('ok'.encode(),client)
    server.close() #Use this command to receive once,automatically send once and then shut down the server
 
#Use multi-threading to impllement the function for obtaining received data and pass in the client parameter
client_handler = threading.Thread(target=handle_client)
client_handler.start()
    