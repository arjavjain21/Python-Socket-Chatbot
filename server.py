import threading
import socket

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = set()
clients_lock = threading.Lock()


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} Connected")

    try:
        connected = True
        while connected:
            msg = conn.recv(1024).decode(FORMAT)
            if not msg:
                break
            # if there was no msg, something went wrong at user's end, break
            # disconnecting that particular client from the server


            if msg == DISCONNECT_MESSAGE:
                connected = False
                
            # can disconnect the client

            print(f"[{addr}] {msg}")
            with clients_lock: # locking that particular thread
                for c in clients:
                    c.sendall(f"[{addr}] {msg}".encode(FORMAT))
                    # sending the string/msg to all the clients
    finally:
        with clients_lock:
            clients.remove(conn)
            # removes connection object
            
        conn.close()


def start():
    print('Server started. Waiting for connections')
    server.listen()
    while True:
        conn, addr = server.accept()
        # conn is a connection object (socket)
        # addr is the socket address string

        with clients_lock: 
        # to make sure only 1 thread is being modified at an instance
        # locks all other threads from modifying this particular datastructure
        
            clients.add(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

# thread is used handle simultaneous messaging/working of the clients on the same server. 
# one thread can wait for a particular client while others can wait for other clients
# no client gets blocked from sending a msg ie all operations take place

start()