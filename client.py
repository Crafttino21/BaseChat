import socket
import threading
import base64
from colorama import Fore

banner = '''
██████╗  █████╗ ███████╗███████╗ ██████╗██╗  ██╗ █████╗ ████████╗    
██╔══██╗██╔══██╗██╔════╝██╔════╝██╔════╝██║  ██║██╔══██╗╚══██╔══╝    
██████╔╝███████║███████╗█████╗  ██║     ███████║███████║   ██║       
██╔══██╗██╔══██║╚════██║██╔══╝  ██║     ██╔══██║██╔══██║   ██║       
██████╔╝██║  ██║███████║███████╗╚██████╗██║  ██║██║  ██║   ██║       
╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝       
     Soft-Encrypted P2P Chat Client | By WeepingAngel
     GitHub: https://github.com/Crafttino21
     
    * DISCLAIMER: This is a Hobby Project. Base64 Encrypteion dosnt Replace a good E2EE  *
    You are Using the client Version!
'''

def send_message(client_socket, client_nickname):
    while True:
        message = input("Nachricht eingeben: ")
        if message.lower() == "exit":
            break

        # Base64-Kodierung der Nachricht
        encoded_message = base64.b64encode(message.encode('utf-8'))

        client_socket.sendall(encoded_message)
        print(f"{client_nickname} ({client_socket.getsockname()}): {message}")

        # Antwort des Servers empfangen
        response = client_socket.recv(1024)
        decoded_response = base64.b64decode(response).decode('utf-8')
        print("Empfangene Antwort:", decoded_response)

def main():
    print(Fore.LIGHTMAGENTA_EX + banner)
    host = input("[Server IP] > ")
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Nickname eingeben
    nickname = input("Nickname eingeben: ")
    client_socket.sendall(nickname.encode('utf-8'))

    # Server-Nickname empfangen
    server_nickname = client_socket.recv(1024).decode('utf-8')
    print(f"Verbunden mit Server {server_nickname} ({host}:{port})")

    # Thread starten, um Nachrichten zu senden
    send_thread = threading.Thread(target=send_message, args=(client_socket, nickname))
    send_thread.start()

if __name__ == "__main__":
    main()
