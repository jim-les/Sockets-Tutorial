from flask import Flask, render_template, request, jsonify
from Client import Client, Database
import threading

# Variables
ip_address = "127.0.0.1"
port = 34567

# database init
database = Database()

# socket init
client = Client(ip_address, port, database)
receive_thread = threading.Thread(target=client.receive_messages)
receive_thread.start()

# insert message into db
# database.insertMessage(client.receive_messages().decode())

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def home():
    context = {
        "messages": client.chat_messages,
        "database_messages": database.getAllMessages()
    }

    if request.method == "POST":
        message = request.form['message']
        client.client_socket.send(message.encode())
        
    return render_template("index.html", context=context)

if __name__ == "__main__":
    app.run(debug=True)
