import socket
import sys
import time
import pickle

import MySQLdb as mariadb

from uuid import uuid4

import sock_communication as sc

#подключение к mysql
mariadb_connection = mariadb.connect(user='dmelessa',
                                    password='ahegao',
                                    database='test2')
cursor = mariadb_connection.cursor()

#https://iximiuz.com/ru/posts/writing-python-web-server-part-2/#hybrid


def run_server(port=8000):
    serv_sock = create_serv_sock(port)
    cid = 0
    while True:
        client_sock = accept_client_conn(serv_sock, cid)
        serve_client(client_sock, cid)
        cid += 1


def serve_client(client_sock, cid):
    request = read_request(client_sock)
    if request is not None:
        response = handle_request(pickle.loads(request))
        write_response(client_sock, response, cid)
    else:
        print(f'Client #{cid} unexpectedly disconnected')


def create_serv_sock(serv_port):
    serv_sock = socket.socket(socket.AF_INET,
                              socket.SOCK_STREAM,
                              proto=0)
    serv_sock.bind(('', serv_port))
    serv_sock.listen()
    return serv_sock


def accept_client_conn(serv_sock, cid):
    client_sock, client_addr = serv_sock.accept()
    print(f'Client #{cid} connected {client_addr[0]}:{client_addr[1]}')
    return client_sock 


def read_request(client_sock, delimeter=b''):
    request = sc.recv_msg(client_sock)
    return request
    # try:
    #     while True:
    #         chunk = client_sock.recv(4)
    #         if not chunk:
    #             #клиент преждевременно отключился
    #             return None
            
    #         request += chunk
    #         if delimeter in request:
    #             request = request.rsplit(b'!', 1)[0]
    #             return request
    # except ConnectionResetError:
    #     #соединение было нежиданно разорванно
    #     return None
    # except:
    #     raise


def log_in(**kwargs):
    response = {}
    cursor.execute('''
        SELECT `users`.`id`
        ,      `users`.`login` as `login`
        ,      `users`.`group` as `group`
        ,      `user_passwd`.`user_passwd` as `password`
        ,      `user_passwd`.`auth_tok` as `token`
            FROM `users` INNER JOIN `user_passwd`
                ON `users`.`id` = `user_passwd`.`user_id`
                 WHERE `users`.`login` = %(login)s;
        ''', {'login': kwargs['login']
        })
    record = cursor.fetchall()

    response['status'] = 'fail'

    if record != ():
        record = record[0]
        if 'auth_token' in kwargs:
            if kwargs['auth_token'] == record[4]:
                response['status'] = 'success'
        elif record[3] == kwargs['password']:
            response['auth_token'] = str(uuid4())
            response['group'] = record[2]
            response['status'] = 'success'
            cursor.execute(f'''
                UPDATE `user_passwd`
                SET `auth_tok` = '{response['auth_token']}'
                WHERE user_id =  '{record[0]}';
                ''')

    return response


def register():
    pass


#insert information about game into sql
def add_game(**kwargs):
    
    cursor.execute('''
        INSERT IGNORE INTO `developers`(`developer_name`)
            VALUES
            %(developer)s
    ''', {'developer': kwargs['developer']
    })

    cursor.execute('''
        INSERT IGNORE INTO `games`(`game_name`, `release_date`, `rating`, `description`)
            SELECT %(name)s
            ,%(release)s
            ,%(rating)s
            ,%(description)s
    ''', {'name': kwargs['game_name'],
          'realease': kwargs['release_date'],
          'rating': kwargs['rating'],
          'description': kwargs['description']
    })
    
    for publisher in kwargs['publishers']:
        cursor.execute('''
            INSERT IGNORE INTO `publishers`(`publisher_name`)
                VALUES
                %(publisher)s
        ''', {'publisher': publisher})

        cursor.execute('''
            INSERT INTO `game_publisher`(`game_id`, `publisher_id`)
            SELECT `game_id`, `publisher_id` FROM `games`, `publishers`
            WHERE `game_name` = %(name)s
            AND `publisher_name` = %(publisher)s;  
        ''', {'name': kwargs['game_name'],
              'publisher': publisher})

    cursor.execute('''
        INSERT INTO `game_developer`(`game_id`, `developer_id`)
        SELECT `game_id`, `developer_id` FROM `games`, `developers`
        WHERE `game_name` = %(name)s
        AND `developer_name` = %(developer)s
    ''', {'name': kwargs['game_name'],
          'developer': kwargs['developer']})

    for platform in kwargs['platforms']:
        cursor.execute('''
            INSERT INTO `game_platform`(`game_id`, `platform_id`)
            SELECT `game_id`, `platform_id` FROM `games`, `platforms`
            WHERE `game_name` = %(name)s
            AND `platform_name` = %(platform)s
        ''', {'name': kwargs['game_name'],
              'platform': platform})

    # for image in kwargs['images']:
    #     cursor.execute('''
    #         INSERT INTO `pictures`(`game_id`, `source`)
    #     ''')
    ...


def get_games_list():
    pass


def get_game_info():
    pass


Exec_request = {
    "login": log_in
}


def handle_request(request):
    response = Exec_request.get(request['type'], lambda: 'Invalid')(**request)
    #Exec_request[request['type']](request)
   #time.sleep(5)
    return response


def write_response(client_sock, response, cid):
    #client_sock.sendall(pickle.dumps(response))
    sc.send_msg(client_sock, response)
    client_sock.close()
    print(f'Client #{cid} has been served')


if __name__ == '__main__':
    run_server(port=8000)