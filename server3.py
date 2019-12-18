import http.server
import socketserver
import MySQLdb as mariadb
from socketserver import StreamRequestHandler, TCPServer

import socket
import sys
import time
import pickle
import time

#подключение к mysql
mariadb_connection = mariadb.connect(user='dmelessa',
                                    password='ahegao',
                                    database='test2')
cursor = mariadb_connection.cursor()

#данные сервера
host = 'localhost'
port = 8000
addr = (host, port)

def return_game_list():
    cursor.execute('SELECT * FROM `genres`')
    records = cursor.fetchall()
    return records
    # for row in records:
    #     print("id_genre: ", row[0])
    #     print("genre_name: ", row[1], "\n")

class MyTCPHandler(StreamRequestHandler):

    def handle(self):
        game_list = None
        #get data from client
        self.data = self.request.recv(1024)
        #decode data
        self.command = bytes.decode(self.data)
        if (self.command == 'genres'):
            print('recieved command $genres$')
            game_list = return_game_list()
            print(game_list)
        #send response to client
        #time.sleep(5)
        #if game_list is None:
        #    self.request.sendall(pickle.dumps(self.data))
        self.request.sendall(pickle.dumps(game_list))

if __name__ == '__main__':
    server = TCPServer(addr, MyTCPHandler)
    server.serve_forever()