import socket
 
target_host = '127.0.0.1'
target_port = 9997
 
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

# Let the timeout = 1
timeout = 1  # 1s

# Retry to send the request ang receive the respond,the most try 5times
retries = 0
while retries < 5:
    try:
        # Send the request message
        filename = "example.txt"
        download_message = f"DOWNLOAD {filename}"
        client.sendto(download_message.encode(), (target_host,target_port))

        # Set the timeout
        client.settimeout(timeout)
        
        # Waiting for reponse
        response, _ = client.recvfrom(1024)
        print(f"Server response: {response.decode()}")
        break  # Tf receive the response ,exit the retry

    except socket.timeout:
        retries += 1
        timeout *= 2  # Add the tiomeout after every retry
        print(f"Timeout, retrying... Attempt {retries}")

#Receive some data
data,addr = client.recvfrom(1024)
print(data.decode())