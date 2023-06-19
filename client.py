import socket
import threading

BUFFER = 1024
server_ip = "localhost"
server_port = 9090

nickname = input("Nickname: ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((server_ip, server_port))

client_socket.send(nickname.encode())

def send_message():
    while True:
        message = f"{nickname}: {input()}"
        client_socket.send(message.encode())

def receive_message():
    try:
        while True:
            message = client_socket.recv(BUFFER).decode("utf-8")
            print(message)

    except Exception as e:
        print("Error:", str(e))

    finally:
        client_socket.close()

receive_thread = threading.Thread(target=receive_message)
send_thread = threading.Thread(target=send_message)

receive_thread.start()
send_thread.start()