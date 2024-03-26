import socket
import threading
from concurrent.futures import ThreadPoolExecutor


class Thread(threading.Thread):
    def __init__(self, client_socket, client_name, server):
        threading.Thread.__init__(self)
        self.on = True
        self.client_socket = client_socket
        self.client_name = client_name
        self.server = server

    def run(self):
        while self.on:
            text = self.client_socket.recv(1024).decode("utf-8")
            if text == "exit":
                self.on = False
            self.server.send_all(" %s:%s" % (self.client_name, text))
        self.client_socket.close()


class Server:
    def __init__(self):
        self.isOn = False
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.bind(('127.0.0.1', 8999))
        self.socket_server.listen(5)
        self.all_client_dic = {}
        self.Thread_pool = ThreadPoolExecutor(max_workers=5)

    def start_server(self):
        print('start server')
        if not self.isOn:
            self.isOn = True
            main_thread = threading.Thread(target=self.recv_main_thread)
            main_thread.start()

    def recv_main_thread(self):
        while self.isOn:
            client_socket, client_address = self.socket_server.accept()
            client_name = client_socket.recv(1024).decode("utf-8")
            print(client_name)
            client_thread = Thread(client_socket, client_name, self)
            self.all_client_dic[client_name] = client_thread
            self.Thread_pool.submit(client_thread.run)
            self.send_all("【服务器通知】欢迎%s进入聊天室" % client_name)

    def send_all(self, msg):
        print(msg + "\n")
        for client_thread in self.all_client_dic.values():
            if client_thread.on:
                client_thread.client_socket.send(msg.encode("utf-8"))


server = Server()
server.start_server()

# Keep the main thread running
while True:
    pass
