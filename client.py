import socket
 
target_host = '127.0.0.1'
target_port = 9999
 
#Create a socket object
client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# Request to doenload file
filename = "file.txt"
download_message = f"DOWNLOAD {filename}"
#Request to download part of the file
start_byte = 0
end_byte = 1023
file_request = f"FILE example.txt GET START {start_byte} END {end_byte}"
socket.sendto(file_request.encode(), (target_host,target_port))
#Receive some data
data,addr = client.recvfrom(1024)
 
print(data.decode())