# For handling clients
import socket
import sys
import os
import tkinter

# python library for GUI
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

# Initialize global variables
username = ""
password = ""

option = 0
filename = "" 
temp = ""

#creating socket
lb_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the TL.py
lb_socket.connect(('localhost', 30005))

# Function to validate credentials
def validate_credentials():
    global username, password, f
    
    un = username
    ps = password

    #sending to Uploads for validation
    lb_socket.send(un.encode())
    lb_socket.send(ps.encode())
    z = lb_socket.recv(1024).decode()
            
    if z == "i":
        messagebox.showinfo("Success", "Login successful!")
        return True
    else:
        messagebox.showerror("Error", "Incorrect username or password. Please try again.")
        root.destroy()
        return False

# Function to handle option selection
def handle_option():
    global option
    if option_var.get() == 1:
        option = 1
        file_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        
    elif option_var.get() == 2:
        option = 2
        file_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
    elif option_var.get() == 3:
        option = 3
        root.destroy()

# **Function to handle file selection**
def handle_file_selection():
    filename = filename_entry.get()
    root.destroy()
    messagebox.showinfo("File",filename)

# Function to handle submission
def submit():
    global username, password, option, filename
    username = username_entry.get()
    password = password_entry.get()
    
    if validate_credentials():
        login_frame.place_forget()  # Remove the login frame from the window
        option_frame.place(relx=0.5, rely=0.5, anchor=CENTER)  # Show the option frame

from tkinter import filedialog

# browsing files in system
def open_file_dialog():
    entry_var = tkinter.StringVar()
    entry = tkinter.Entry(root, textvariable=entry_var, width=40)
    entry.grid(row=0, column=0, padx=10, pady=10)
# Trying to restrict user
    print(option)
    if option ==1:
        file_path = filedialog.askopenfilename(title="Select a file")
    if option ==2:
        initial_dir = "C:/Users/shahz/OneDrive/Desktop/CN Project/uploaded/"
        file_path = filedialog.askopenfilename(title="Select a file", initialdir=initial_dir)
    entry_var.set(file_path)
    global filename, temp
    directory, temp = os.path.split(file_path)
    filename=file_path
    print(filename)
    root.destroy()
    messagebox.showinfo("File",filename)

#**GUI**
# Create main window
root = Tk()
root.title("File Transfer Application")

# Set background image
background_image = PhotoImage(file="Zoe.png")
background_label = Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create login frame
login_frame = Frame(root, bg="white", padx=50, pady=50)
login_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

# Create login widgets
username_label = Label(login_frame, text="Username:", bg="white", font=("Arial", 14))
username_label.grid(row=0, column=0, pady=10)
username_entry = Entry(login_frame, bg="#F0F0F0", font=("Arial", 14))
username_entry.grid(row=0, column=1, pady=10)

password_label = Label(login_frame, text="Password:", bg="white", font=("Arial", 14))
password_label.grid(row=1, column=0, pady=10)
password_entry = Entry(login_frame, show="*", bg="#F0F0F0", font=("Arial", 14))
password_entry.grid(row=1, column=1, pady=10)

login_button = Button(login_frame, text="Login", bg="#4CAF50", fg="white", font=("Arial", 14), command=submit)
login_button.grid(row=2, columnspan=2, pady=10)

# Create option frame
option_frame = Frame(root, bg="white", padx=50, pady=50)

option_label = Label(option_frame, text="Select an option:", bg="white", font=("Arial", 14))
option_label.grid(row=0, column=0, pady=10)

option_var = IntVar()
option1 = Radiobutton(option_frame, text="Upload a file", variable=option_var, value=1, bg="white", font=("Arial", 14), command=handle_option)
option1.grid(row=1, column=0, pady=5)
option2 = Radiobutton(option_frame, text="Download a file", variable=option_var, value=2, bg="white", font=("Arial", 14), command=handle_option)
option2.grid(row=2, column=0, pady=5)
option3 = Radiobutton(option_frame, text="Exit", variable=option_var, value=3, bg="white", font=("Arial", 14), command=handle_option)
option3.grid(row=3, column=0, pady=5)

# Create file frame
file_frame = Frame(root, bg="white", padx=50, pady=50)

file_label = Label(file_frame, text="Enter filename:", bg="white", font=("Arial", 14))
file_label.grid(row=0, column=0, pady=10)

filename_entry = Entry(file_frame, bg="#F0F0F0", font=("Arial", 14))
filename_entry.grid(row=0, column=1, pady=10)

file_button = Button(file_frame, text="Browse", bg="#4CAF50", fg="white", font=("Arial", 14), command=open_file_dialog)
file_button.grid(row=2, columnspan=2, pady=10)

root.mainloop()
#**GUI END**

# Define the maximum chunk size
MAX_CHUNK_SIZE = 1 * 1024 * 1024  # 1 MB

# **Transmission**
print(filename)
while True:
    if os.path.isfile(filename):
        print("ok")
    else:
        if option!=3 or option!=0:
            messagebox.showinfo("File","The file does not exist in the directory.")
        lb_socket.close()
        break
# Uploading
    c=option
    if c==1:
        terminating = "false"
        l=len(terminating)
        value_bytes = l.to_bytes(4, 'big')
        lb_socket.send(value_bytes)
        
        lb_socket.send(terminating.encode())    
        
        ff = filename
        print(ff)
# Open the file to send
        f1 = str(ff)
        
        with open(ff, 'rb') as f:
            file_data = f.read()

# Split the file into chunks
        chunks = [file_data[i:i+MAX_CHUNK_SIZE] for i in range(0, len(file_data), MAX_CHUNK_SIZE)]

# Create a socket object for the load balancer
        l=len(temp)
        value_bytes = l.to_bytes(4, 'big')
        lb_socket.send(value_bytes)
         
        lb_socket.send(temp.encode())
        
        l=len(chunks)
        value_bytes = l.to_bytes(4, 'big')
        lb_socket.send(value_bytes)
# Send each chunk to the load balancer
        for chunk in chunks:
        
            print("Size of chunk ",len(chunk))
            j = len(chunk)
            value_bytes = j.to_bytes(4, 'big')
            lb_socket.send(value_bytes)     
            lb_socket.send(chunk)
            
        print("all chunk sent")        

        print('got it')
        lb_socket.close()
        messagebox.showinfo("Success", "File successfully uploaded")
        break

    if c==3:
        lb_socket.close()
        sys.exit(1)
        messagebox.showinfo("Success", "successfully exiting")
        break

# Downloading
    if c==2:
        
        terminating = "true"
        l=len(terminating)
        value_bytes = l.to_bytes(4, 'big')
        lb_socket.send(value_bytes)
        
        lb_socket.send(terminating.encode())
        lb_socket.close()
        
        lb_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        lb_socket.connect(('localhost', 40002))
        
        ff = filename.encode()
        lb_socket.send(ff)
        ff = ff.decode()
        print('filename sent')
        
        chunks = []
        
        l = lb_socket.recv(4)  # Receive 4 bytes (integer is 4 bytes long)
        l = int.from_bytes(l, 'big')  # Convert bytes to integer
        
        i=0
        while i<l:
            data = lb_socket.recv(MAX_CHUNK_SIZE)
            print(len(data))
            i=i+1
            chunks.append(data)
    #  reassemble chunks
        file_data = b''.join(chunks)
        
    # Open a file in write mode
        filename = ff.replace("C:/","")
        ff = filename.replace("/","")
        filename = "Downloads/"+ff
        
        with open(filename, 'wb') as f:
            f.write(file_data)
        
        lb_socket.close()
        messagebox.showinfo("Success", "File successfully downloaded")
        break