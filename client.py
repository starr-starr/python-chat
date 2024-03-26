from socket import *
import threading


class Client:
    def __init__(self):
        # 实例属性
        self.name = "star"
        self.isConnected = False
        self.client_socket = None

    def connect_server(self):
        if not self.isConnected:
            self.isConnected = True
            self.client_socket = socket()
            self.client_socket.connect(('127.0.0.1', 8999))
            self.client_socket.send(self.name.encode('utf8'))

            main_thread = threading.Thread(target=self.recv_data)
            main_thread.daemon = True
            main_thread.start()

            self.send()
    def recv_data(self):
        while self.isConnected:
            text = self.client_socket.recv(1024).decode('utf8')
            print(text + "\n")

    def send(self):
        while self.isConnected:
            text = input()
            if text != '':
                self.client_socket.send(text.encode('utf-8'))
            # elif text == 'exit':
            #     self.client_socket.send('exit'.encode('utf-8'))
            #     self.isConnected = False


client = Client()
client.connect_server()
