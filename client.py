import socket
import os
import threading

os.system("clear")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("[*] Welcome to Lestons server")
ip_address = "127.0.0.1"
port = 34567

client_socket.connect((ip_address, port))
print("[*] Connection to the server was successful")

name = input("Enter username: ")

def receive_messages():
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        print(data.decode())

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

while True:
    message = input(f"{name}: ")
    client_socket.send(message.encode())
