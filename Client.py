import socket
import threading
#import select

class Client:
    def __init__(self, server, port = 4444):
        self.server = server
        self.port = port
        self.addr =(server, port)
        self.format = "utf-8"
        self.new_message = None

    def Connect(self, name):
        self.name = name
        print(f"Connecting to: {self.server}")
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(self.addr)
        self.s.send(name.encode(self.format))
        print(self.s.recv(2048).decode(self.format))
        threading.Thread(target = self.Incoming, args = ()).start()
        
    def Incoming(self):
        print("Starting recv thread:")
        while True:
            try:
                message = self.s.recv(2048).decode(self.format)
                if message:
                    self.new_message.append(message)
                    print(f"Message from server: {message}")
            except Exception as error:
                
                print(f"Global exception!!! (TOO BAD!): {error}")
                print("Connection lost, trying to reconnect")
                self.Connect(self.name)
                
    def Send(self, message):
        print(f"Sending: {message}")
        self.s.send(message.encode(self.format))
        
if __name__ == '__main__':
        
    Client1 = Client('127.0.0.1', 4444)
    Client1.Connect("Lule")

    while True:
        Client1.Send(input())