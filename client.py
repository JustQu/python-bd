import kivy
import sys
import pickle

from socket import socket, AF_INET, SOCK_STREAM

host = 'localhost'
port = 8000
addr = (host, port)

tcp_socket = socket(AF_INET, SOCK_STREAM)
tcp_socket.connect(addr)
while True:
    data = input('write to server: ')
    data = str.encode(data)
    tcp_socket.send(data)
    data = bytes.decode(data)
    data = pickle.loads(tcp_socket.recv(1024))
    for row in data:
            print("id_genre: ", row[0])
            print("genre_name: ", row[1], "\n")
    print(data)

tcp_socket.close()

def get_games_list():
    pass