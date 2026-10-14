import threading
import socket
#import select
import time

class Server:
    def __init__(self, server, port = 4444):
        self.server = server #socket.gethostbyname(server)
        self.port = port
        self.addr = (self.server, self.port)
        self.format = "utf-8"
        self.disconnect_message = "!disconnect"
        self.client_list = []
        self.client_id_list = []
        self.unread_messages = []
        self.new_message = False
        
    def Start_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.addr)    
        print("Listening for new connections")
        threading.Thread(target = self.New_connections, args=()).start()  
        #_thread.start_new_thread(self.New_connections)
        
    def Remove_client(self, conn_id):
        print(f"{conn_id} was disconnected from the server")
        self.client_list.pop(self.client_id_list.index(conn_id))
        self.client_id_list.remove(conn_id)        
    
    def Client_thread(self, conn, conn_id):
        while True:
            try:
                message = conn.recv(2048).decode(self.format)
                if message:
                    print(f"received message from {conn_id}: {message}")
                    self.unread_messages.append((conn_id,message))
                    self.new_message = True
                else:
                    print(f"something went wrong while trying to receive a message")
                    self.Remove_client(conn_id)
                    break
            except ConnectionResetError as error:
                print(f"something went wrong while trying to receive a message: {error}")
                self.Remove_client(conn_id)
                break
            except Exception as error:
                print(f"Global exception!!! (TOO BAD!): {error}")
                self.Remove_client(conn_id)
                break

    def New_connections(self):
        self.server.listen()
        while True:
            conn, addr = self.server.accept()            
            conn_id = conn.recv(2048).decode(self.format)
            client_ip = addr[0]
            print(f"{client_ip} connected as: {conn_id}")
            current_time = time.strftime("%H:%M:%S", time.localtime())
            conn.send(f"Connected to the Server at: {current_time}".encode(self.format))
            self.client_list.append(conn)
            self.client_id_list.append(conn_id)
            threading.Thread(target = self.Client_thread, args = (conn, conn_id)).start()
            #_thread.start_new_thread(self.Client_thread, (conn, conn_id))
            
    def Send_to_all(self, message):
        for client in self.client_list:
            client.send(message.encode(self.format))
        

if __name__ == '__main__':
    Server1 = Server("127.0.0.1", 4444)
    Server1.Start_server()


