#!/usr/bin/python3
import socket
import os
import zipfile

os.chdir(os.path.dirname(os.path.realpath(__file__)))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET = IP, SOCK_STREAM = TCP
server.bind(('0.0.0.0', 8888))
server.listen()
print("Server listening...")

client_socket, client_adress = server.accept()
print(f"\033[32m[!] Client connected {client_adress}\033[m")

filename ='files.zip'

print(f"[RECV] Receiving the file size")
file_size_in_bytes = client_socket.recv(8)
file_size= int.from_bytes(file_size_in_bytes, 'big')
print("File size received:", file_size, " bytes")
client_socket.send("File size received.".encode("utf-8"))

print(f"[RECV] Receiving the file data.")
# Until we've received the expected amount of data, keep receiving
packet = b""  # Use bytes, not str, to accumulate
while len(packet) < file_size:
    if(file_size - len(packet)) > 1024:  # if remaining bytes are more than the defined chunk size
        buffer = client_socket.recv(1024)  # read SIZE bytes
    else:
        buffer = client_socket.recv(file_size - len(packet))  # read remaining number of bytes

    if not buffer:
        raise Exception("Incomplete file received")
    packet += buffer
with open(filename, 'wb') as f:
    f.write(packet)
os.system("ls")
os.system("ls ../data_received")
print("Received zip file")
print("Extracting files...")
with zipfile.ZipFile(filename, 'r') as zip_ref:
    zip_ref.extractall("../data_received")
print("Done")

os.remove(filename)

print("Execute Main now")
os.system("python3 ../annexes/code/main.py")

print("Image generated")

client_socket.send("OK".encode("utf-8"))

client_socket.close()
server.close()