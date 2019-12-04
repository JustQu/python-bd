import http.server
import socketserver
import MySQLdb as mariadb
from socketserver import *
import socket

#подключение к mysql
mariadb_connection = mariadb.connect(user='dmelessa',
                                    password='ahegao',
                                    database='test')
cursor = mariadb_connection.cursor()

#данные сервера
host = 'localhost'
port = 8000
addr = (host, port)

def return_game_list():
    cursor.execute('SELECT * FROM `genres`')
    records = cursor.fetchall()
    return records
    for row in records:
        print("id_genre: ", row[0])
        print("genre_name: ", row[1], "\n")

class MyTCPHandler(StreamRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024)
        self.command = str.decode(self.data)
        print(self.command)
        if (self.command == 'genres'):
            game_list = return_game_list()
        print('client send: ' + str(self.data))
        self.request.sendall(game_list)

if __name__ == '__main__':
    server = TCPServer(addr, MyTCPHandler)
    server.serve_forever()