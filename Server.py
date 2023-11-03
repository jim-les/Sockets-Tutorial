import socket
import os
import threading

os.system("clear")

class Server:
    def __init__(self, addr, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print("[*] Server initialized")

        self.ip_address = '0.0.0.0'
        self.port = 34567

        self.server.bind((self.ip_address, self.port))
        print(f"[*] Server connected successfully on {self.ip_address}:{self.port}")
        self.server.listen(3)

        self.client_list = {}
        self.users = {}  # Store user credentials (username: password)

    def handle_client(self, client_socket):
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break

                data_str = data.decode()
                if data_str.startswith("REGISTER:"):
                    username, password = data_str.split(":")[1], data_str.split(":")[2]
                    if username not in self.users:
                        self.users[username] = password
                        client_socket.send(b"\nRegistration successful.")
                        for client in self.client_list:
                            client_socket.send(b"Users Online {self.users}")
                            
                    else:
                        client_socket.send(b"User already exists.")
                elif data_str.startswith("LOGIN:"):
                    username, password = data_str.split(":")[1], data_str.split(":")[2]
                    if username in self.users and self.users[username] == password:
                        client_socket.send(b"\nAuthentication successful.")
                        self.client_list[username] = client_socket
                        print(f"{username} connected.")
                        print(f"Users Online {self.users}")

                    else:
                        client_socket.send(b"\nAuthentication failed.")
                else:
                    recipient, message = data_str.split(":", 1)
                    if recipient in self.client_list:
                        recipient_socket = self.client_list[recipient]
                        recipient_socket.send(message.encode())
        except:
            pass

        client_socket.close()
        self.client_list = {k: v for k, v in self.client_list.items() if v != client_socket}
        print("Client disconnected.")

    def running(self):
        while True:
            client_socket, client_address = self.server.accept()
            print(f"[*] Received connection from {client_address}")
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

if __name__ == "__main__":
    port = 34567
    ip_address = "0.0.0.0"
    Server(ip_address, port).running()
