# For uploading and checking credentials
import socket
import random
import threading
import sys

credentials = {"cisco":"cisco", "bob":"abc123", "anna":"abc123"}

# Define the maximum chunk size
MAX_CHUNK_SIZE = 1 * 1024 * 1024  # 1 MB

# Create a socket object
lb_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a random port
lb_socket.bind(('localhost', 30005))

# Get the port number of the load balancer
_, lb_port = lb_socket.getsockname()

# Set the load balancer to listen for incoming connections
lb_socket.listen()

# Define a function to handle client connections
def handle_client(conn, addr):
    print(f'New connection from {addr}')
    
    l = conn.recv(4)  # Receive 4 bytes (integer is 4 bytes long)
    l = int.from_bytes(l, 'big')  # Convert bytes to integer
    
    check_op = conn.recv(l).decode()
    
    if check_op == "true":
        print("exit")
        conn.close()
        sys.exit()
        
    l = conn.recv(4)  # Receive 4 bytes (integer is 4 bytes long)
    l = int.from_bytes(l, 'big')  # Convert bytes to integer
    
    ff = conn.recv(l).decode()
    
    print("file name",ff)
    
    l = conn.recv(4)  # Receive 4 bytes (integer is 4 bytes long)
    l = int.from_bytes(l, 'big')  # Convert bytes to integer
    # Split the file into chunks
    chunks = []
    i=0
    
    while i<l:
        
        j = conn.recv(4)  # Receive 4 bytes (integer is 4 bytes long)
        j = int.from_bytes(j, 'big')  # Convert bytes to integer
        print("Receiving Chunk size ",j)
        
        j= j*2
        print(j)
        data = conn.recv(j)
        print("data length size ",len(data))
        
        chunks.append(data)
       
        i=i+1
        
    file_data = b''.join(chunks)
    print(len(file_data))
    f= ff.replace("C:/","")
    ff = f.replace("/","")
    ff = 'Uploads/'+ ff
    print(ff)
    # Write the file to disk
    with open(ff, 'wb') as f:
        f.write(file_data)    
    
    print("data received in load balancer")

    print('server bye')
    conn.close()

# Start the load balancer and listen for incoming connections
print(f'Load balancer listening on port {lb_port}')
un=""
while True:
    # Wait for a connection
    conn, addr = lb_socket.accept()
    # Create a new thread to handle the connection
    un = conn.recv(1024).decode()
    print(un)
    ps = conn.recv(1024).decode()
    print(ps)
    if credentials[un]==ps:
        print('pass')
        conn.send("i".encode())
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        print("start")
        client_thread.start()
        
    else:
        conn.send("o".encode())
        conn.close()