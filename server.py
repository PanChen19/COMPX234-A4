import socket
import threading
import os 
import base64
import random

bind_ip = '0.0.0.0'
bind_port = 9996

#Define the usage protocol as UDP
server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
 
#Configure the listening IP and port
server.bind((bind_ip,bind_port))
print(f"[*] Server listening on {bind_ip}:{bind_port}")

def handle_file_transfer(filename, client_addr, port):
    
    # Create new socket for this transfer
    transfer_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    transfer_socket.bind((bind_ip, port))
    print(f"[*] Transferring {filename} on port {port}")

    try:
        with open(filename, 'rb') as file:
            while True:
                # Wait for client request
                data, addr = transfer_socket.recvfrom(1024)
                request = data.decode()
                
                if request.startswith('FILE'):
                    parts = request.split()
                    
                    # Handle data request
                    if parts[2] == 'GET':
                        start = int(parts[4])
                        end = int(parts[6])
                        
                        # Read requested chunk
                        file.seek(start)
                        chunk = file.read(end - start + 1)
                        
                        # Send encoded data
                        encoded = base64.b64encode(chunk).decode()
                        response = (f"FILE {filename} OK START {start} "
                                   f"END {end} DATA {encoded}")
                        transfer_socket.sendto(response.encode(), addr)
                    
                    # Handle transfer completion
                    elif parts[2] == 'CLOSE':
                        transfer_socket.sendto(
                            f"FILE {filename} CLOSE_OK".encode(),
                            addr
                        )
                        break
    finally:
        transfer_socket.close()

def handle_requests():
    """Main server loop to handle incoming requests"""
    while True:
        # Wait for download request
        data, addr = server.recvfrom(1024)
        print(f"[*] Received request from {addr}")
        
        if data.startswith(b'DOWNLOAD'):
            filename = data.decode().split()[1].strip()
            
            # Check if file exists
            if os.path.exists(filename):
                # Assign random port for transfer
                port = random.randint(50000, 51000)
                size = os.path.getsize(filename)
                
                # Send OK response
                response = f"OK {filename} SIZE {size} PORT {port}"
                server.sendto(response.encode(), addr)
                
                # Start transfer thread
                threading.Thread(
                    target=handle_file_transfer,
                    args=(filename, addr, port)
                ).start()
            else:
                # Send error response
                response = f"ERR {filename} NOT_FOUND"
                server.sendto(response.encode(), addr)

# Start server
threading.Thread(target=handle_requests).start()

