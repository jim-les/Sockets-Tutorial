import socket
import os
import threading

os.system("clear")
intro = """  
#### WELCOME TO HST CHAT ####
1. LOGIN
2. SIGNUP
"""

class Client:
    def __init__(self, address, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip_address = address
        self.port = port

    def make_connections(self, intro):
        self.client_socket.connect((self.ip_address, self.port))
        print("Connected to the server.")
        self.authentication()
    
    def authentication(self):
        print(intro)
        choice = input("choice >> ")
        if choice == "1":
            self.send_login()
        
        elif choice == "2":
            self.register_user()
        
        else:
            print("Invalid Choice")
            os.system("clear")
            return self.authentication()

    def register_user(self):
        os.system("clear")
        print("####### Create an Account with HST #######")
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        registration_data = f"REGISTER:{username}:{password}"
        self.client_socket.send(registration_data.encode())
        response = self.client_socket.recv(1024).decode()
        print(response)

    def send_login(self):
        os.system("clear")
        print("######## Login into your HST Account #########" )
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        data = f"LOGIN:{username}:{password}"
        self.client_socket.send(data.encode())
        response = self.client_socket.recv(1024)
        print(response.decode())

    def send_message(self):
        while True:
            recipient = input("Enter recipient's username: ")
            message = input("Enter your message: ")
            data = f"{recipient}:{message}"
            self.client_socket.send(data.encode())

    def receive_messages(self):
        while True:
            data = self.client_socket.recv(1024)
            print(data.decode())

if __name__ == "__main__":
    port = 34567
    ip_address = "127.0.0.1"
    client = Client(ip_address, port)
    client.make_connections(intro)
    receive_thread = threading.Thread(target=client.receive_messages)
    send_thread = threading.Thread(target=client.send_message)
    receive_thread.start()
    send_thread.start()
