import socket
import threading

BUFFER = 1024
IP = "localhost"
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
nicknames = []
clients = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    while True:
        try:
            msg = conn.recv(BUFFER).decode("utf-8")
            if msg == "!count":
                conn.send(f"User count: {len(nicknames)}".encode())
            else:
                broadcast(msg.encode())
        except:
            print("bitti")
            index = clients.index(conn)
            clients.remove(conn)
            conn.close()
            nickname = nicknames[index]
            broadcast(f"{nickname} has left!".encode())
            nicknames.remove(nickname)
            break

def start():
    server.listen(15)
    while True:
        client, address = server.accept()

        print(f"Connected with {address}")
        nickname = client.recv(BUFFER).decode("utf-8")

        broadcast(f"{nickname} has joined!".encode())

        nicknames.append(nickname)
        clients.append(client)

        thread = threading.Thread(target=handle_client, args=(client, address))
        thread.start()

        print(f"[ACTIVE CONNECTİONS]{threading.active_count() - 1}")

print("[STARTING] server is starting...")
start()
server.close()