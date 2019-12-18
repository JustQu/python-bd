import kivy
import sys
import pickle

from socket import socket, AF_INET, SOCK_STREAM

import sock_communication as sc

host = 'localhost'
port = 8000
addr = (host, port)

tcp_socket = socket(AF_INET, SOCK_STREAM)
tcp_socket.connect(addr)

request = {}
request['type'] = 'login'
request['login'] = 'dmelessa'

sc.send_msg(tcp_socket, request)
data = sc.recv_msg(tcp_socket)

#data = pickle.dumps(request)
#data_size = len(data)
#data = tcp_socket.send(data)

data = pickle.loads(data)

print(data)
#while True:
    #data = input('write to server: ')
    #data = str.encode(data)
    #try:
   #     a = tcp_socket.send(data)
   # except:
  #      print('pepa')
  #  print(a)
  #  if a == 0:
 #       exit()
  #  data = bytes.decode(data)
 #   print(tcp_socket.recv(1024))
    # print(data)
    # if data is not None:
    #     for row in data:
    #             print("id_genre: ", row[0])
    #             print("genre_name: ", row[1], "\n")
   # print(data)

tcp_socket.close()

def get_games_list():
    pass