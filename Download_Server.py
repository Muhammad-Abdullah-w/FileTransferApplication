# Downloading
import socket
import threading

MAX_CHUNK_SIZE = 1 * 1024 * 1024  # 1 MB

# Create a socket object for the load balancer
lb_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the load balancer
lb_socket.bind(('localhost', 40002))

_, lb_port = lb_socket.getsockname()

lb_socket.listen()

def handle_client(conn, addr):
    print(f'New connection from {addr}')
        
    filename = conn.recv(1024).decode()
    print(filename)
    #filename = 'download/'+filename
    with open(filename, 'rb') as f:
        file_data = f.read()

# Split the file into chunks
    chunks = [file_data[i:i+MAX_CHUNK_SIZE] for i in range(0, len(file_data), MAX_CHUNK_SIZE)]
    
    l=len(chunks)
    value_bytes = l.to_bytes(4, 'big')
    conn.sendall(value_bytes)
    
    for chunk in chunks:
        print(len(chunk))
        conn.sendall(chunk)    

    print("all chunk sent")         
    print("all data sent")
    print("all data sent")     
    conn.close()
         
while True:
    # Wait for a connection
    conn, addr = lb_socket.accept()
    # Create a new thread to handle the connection
    client_thread = threading.Thread(target=handle_client, args=(conn, addr))
    print("start")
    client_thread.start()