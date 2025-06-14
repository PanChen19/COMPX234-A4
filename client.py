import socket
 
target_host = '127.0.0.1'
target_port = 9996
# Create a UDP socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Read file names from "file.txt" to download
with open("file.txt", "r") as file_list:
    files_to_download = file_list.readlines()

# Strip newline characters from each filename
files_to_download = [filename.strip() for filename in files_to_download]
def send_and_receive(socket, message, address, max_retries=5):
    # Let the timeout = 1
    timeout = 1  # 1s
    # Retry to send the request ang receive the respond,the most try 5times
    retries = 0
    while retries < 5:
        try:
            # Send the message
            sock.sendto(message.encode(), address)
            
            # Wait for response with timeout
            sock.settimeout(timeout)
            response, _ = sock.recvfrom(2048)  # Larger buffer for base64 data
            return response.decode()
            
        except socket.timeout:
            retries += 1
            timeout *= 2  # Exponential backoff
            print(f"Timeout, retrying... Attempt {retries}")
    return None

# Read list of files to download
with open("file.txt", "r") as file_list:
    files_to_download = [filename.strip() for filename in file_list.readlines()]

# Process each file sequentially
for filename in files_to_download:
    print(f"Requesting {filename}...")
    
    # Phase 1: Send DOWNLOAD request
    response = send_and_receive(
        client,
        f"DOWNLOAD {filename}",
        (target_host, target_port)
    )
    
    # Check if file exists on server
    if not response or response.startswith("ERR"):
        print(f"Failed: {response}")
        continue
        
    # Parse server response (OK filename SIZE size PORT port)
    parts = response.split()
    file_size = int(parts[3])
    transfer_port = int(parts[5])  # Port for file transfer
    
    # Phase 2: Download file in chunks
    with open(filename, 'wb') as f:  # Open in binary write mode
        start_byte = 0
        while start_byte < file_size:
            # Calculate current chunk range
            end_byte = min(start_byte + 999, file_size - 1)
            
            # Request file chunk
            chunk_response = send_and_receive(
                client,
                f"FILE {filename} GET START {start_byte} END {end_byte}",
                (target_host, transfer_port)
            )
            
            # Verify response
            if not chunk_response or not "DATA" in chunk_response:
                print("Chunk request failed")
                break
                
            # Extract and decode base64 data
            data_part = chunk_response.split("DATA ")[1]
            f.write(base64.b64decode(data_part.encode()))
            start_byte = end_byte + 1
            print(f"Downloaded {start_byte}/{file_size} bytes")
    
    # Phase 3: Close connection
    send_and_receive(
        client,
        f"FILE {filename} CLOSE",
        (target_host, transfer_port)
    )
    print(f"Completed: {filename}")