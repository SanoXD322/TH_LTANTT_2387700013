import threading

class ConnectionManager:
    def __init__(self):
        self.clients = {}
        self.lock = threading.Lock()

    def add_client(self, client_sock, username, encryption_key):
        with self.lock:
            self.clients[client_sock] = {'username': username, 'encryption_key': encryption_key}

    def remove_client(self, client_sock):
        with self.lock:
            if client_sock in self.clients:
                del self.clients[client_sock]