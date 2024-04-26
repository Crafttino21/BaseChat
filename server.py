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

    You are Using the Server Version!
'''

def receive_messages(client_socket, client_address, client_nickname):
    while True:
        try:
            encrypted_data = client_socket.recv(1024)
            if not encrypted_data:
                break

            # Base64-Decodierung der empfangenen Nachricht
            decoded_data = base64.b64decode(encrypted_data).decode('utf-8')

            print(f"{client_nickname} ({client_address}): {decoded_data}")

            # Antwort des Servers
            response = input("Antwort eingeben: ")
            encoded_response = base64.b64encode(response.encode('utf-8'))

            client_socket.sendall(encoded_response)
            print("Antwort gesendet:", response)
        except ConnectionResetError:
            print(f"Die Verbindung mit {client_address} wurde geschlossen.")
            break

def main():
    print(Fore.LIGHTCYAN_EX + banner)
    host = 'localhost'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server läuft auf {host}:{port}")

    # Nickname für den Server eingeben
    server_nickname = input("Server-Nickname eingeben: ")

    while True:
        client_socket, client_addr = server_socket.accept()
        print(f"Verbindung hergestellt mit {client_addr}")

        # Nickname vom Client empfangen
        client_nickname = client_socket.recv(1024).decode('utf-8')
        print(f"{client_nickname} ist dem Chat beigetreten.")

        # Server-Nickname an den Client senden
        client_socket.sendall(server_nickname.encode('utf-8'))

        # Thread starten, um Nachrichten zu empfangen
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket, client_addr, client_nickname))
        receive_thread.start()

if __name__ == "__main__":
    main()
