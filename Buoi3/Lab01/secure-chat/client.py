import socket, ssl, threading, os, binascii
from message_encryption import MessageEncryption

SERVER_HOST, SERVER_PORT = '127.0.0.1', 8443
CA_CERT = 'certs/ca/ca.crt'
CLIENT_CERT, CLIENT_KEY = 'certs/client/client.crt', 'certs/client/client.key'

def receive_messages(ssl_sock, me):
    while True:
        try:
            enc_data = ssl_sock.recv(4096)
            if not enc_data: break
            print(me.decrypt(enc_data))
        except Exception:
            pass

if __name__ == '__main__':
    username = input("Username: ").strip()
    aes_key = os.urandom(32)
    me = MessageEncryption(aes_key)
    
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=CA_CERT)
    context.load_cert_chain(certfile=CLIENT_CERT, keyfile=CLIENT_KEY)
    context.verify_mode = ssl.CERT_REQUIRED
    context.check_hostname = False
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_sock = context.wrap_socket(sock, server_hostname=SERVER_HOST)
    ssl_sock.connect((SERVER_HOST, SERVER_PORT))
    
    ssl_sock.send(f"{username}:{binascii.hexlify(aes_key).decode()}".encode())
    threading.Thread(target=receive_messages, args=(ssl_sock, me), daemon=True).start()
    
    print("Type messages (type 'exit' to quit):")
    while True:
        msg = input()
        if msg.lower() == 'exit': break
        ssl_sock.send(me.encrypt(msg))
        
    ssl_sock.close()