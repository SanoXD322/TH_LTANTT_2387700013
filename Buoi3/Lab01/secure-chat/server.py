import socket, ssl, threading
from connection_manager import ConnectionManager
from room_manager import RoomManager
from message_encryption import MessageEncryption

HOST, PORT = '127.0.0.1', 8443
SERVER_CERT, SERVER_KEY = 'certs/server/server.crt', 'certs/server/server.key'
CA_CERT = 'certs/ca/ca.crt'

conn_mgr = ConnectionManager()
room_mgr = RoomManager()

def handle_client(conn, addr):
    print(f"[+] Client connected: {addr}")
    try:
        data = conn.recv(1024).decode()
        if ':' not in data: return
        
        username, key_hex = data.split(':')
        enc_key = bytes.fromhex(key_hex)
        conn_mgr.add_client(conn, username, enc_key)
        
        room_mgr.create_room('general')
        room_mgr.join_room('general', conn)
        me = MessageEncryption(enc_key)
        
        while True:
            enc_message = conn.recv(4096)
            if not enc_message: break
            try:
                msg = me.decrypt(enc_message)
                print(f"[{username}]: {msg}")
                out_msg = f"[{username}]: {msg}"
                
                with conn_mgr.lock:
                    for client_sock, info in conn_mgr.clients.items():
                        if client_sock != conn:
                            me_other = MessageEncryption(info['encryption_key'])
                            client_sock.send(me_other.encrypt(out_msg))
            except Exception:
                continue
    except Exception:
        pass
    finally:
        print(f"[-] Client disconnected: {addr}")
        conn_mgr.remove_client(conn)
        room_mgr.leave_room('general', conn)
        conn.close()

if __name__ == '__main__':
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=SERVER_CERT, keyfile=SERVER_KEY)
    context.load_verify_locations(cafile=CA_CERT)
    context.verify_mode = ssl.CERT_REQUIRED
    context.options = ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Server listening on {HOST}:{PORT}")
    
    while True:
        newsocket, fromaddr = server.accept()
        connstream = context.wrap_socket(newsocket, server_side=True)
        threading.Thread(target=handle_client, args=(connstream, fromaddr), daemon=True).start()