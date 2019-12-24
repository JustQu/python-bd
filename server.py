import socket
import sys
import time
import pickle
import whirlpool

import MySQLdb as mariadb

import sock_communication as sc

from uuid import uuid4

from  sql_errno import error

#подключение к mysql
mariadb_connection = mariadb.connect(user='dmelessa',
                                    password='ahegao',
                                    database='test3')
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
        elif record[3] == whirlpool.new(str.encode(kwargs['password'])):
            response['auth_token'] = str(uuid4())
            response['group'] = record[2]
            response['status'] = 'success'
            cursor.execute(f'''
                UPDATE `user_passwd`
                SET `auth_tok` = '{response['auth_token']}'
                WHERE user_id =  '{record[0]}';
                ''')

    return response


def register(**kwargs):
    response = {}
    response['status'] ='fail'

    if 'login' not in kwargs or 'password' not in kwargs:
        return response
    if len(kwargs['login']) < 2 or len(kwargs['login']) > 20 or len(kwargs['password']) < 6:
        return response

    try:
        cursor.execute('''
            INSERT INTO `users`(`login`, `group`)
            SELECT '%(login)s', 'user';
        ''' % {'login': kwargs['login']
        })
    except Exception as e:
        print('Ошибка в добавлении нового пользователя')
        print('Логин: ', kwargs['login'])
        if e.args[0] == error['Duplicate_entry']:
            print("Пользователь с таким именем уже существует.")
        else:
            print(str(e))
        return response
    
    try:
        cursor.execute('''
            INSERT INTO `user_passwd`(`user_id`, `user_passwd`)
            SELECT id, '%(hash)s'
            FROM `users`
            WHERE login = '%(login)s';
        ''' % {'login': kwargs['login'],
               'hash': whirlpool.new(str.encode(kwargs['password'])).hexdigest()
        })
    except Exception as e:
        cursor.execute('''
        DELETE FROM `users`
        WHERE `login` = '%(login)s'
        ''' % {'login': kwargs['login']})
        mariadb_connection.commit()
        print('Ошибка в добавлении при добавлении пароля нового пользователя')
        print('Логин: ', kwargs['login'])
        print(str(e))
        return response
    
    mariadb_connection.commit()
    response['status'] = 'success'
    return response
    

#insert information about game into sql
def add_game(**kwargs):
    '''game_name developer release rating description publishers platforms '''

    cursor.execute('''
        INSERT IGNORE INTO `developers`(`developer_name`)
            SELECT
            '%(developer)s';
    ''' % {'developer': kwargs['developer']
    })

    cursor.execute('''
        INSERT IGNORE INTO `games`(`game_name`, `release_date`, `rating`, `description`)
            SELECT '%(name)s'
            ,'%(release)s'
            ,'%(rating)s'
            ,'%(description)s';
    ''' % {'name': kwargs['game_name'],
          'release': kwargs['release_date'],
          'rating': kwargs['rating'],
          'description': kwargs['description']
    })
    
    for genre in kwargs['genres']:
        cursor.execute('''
            INSERT INTO `game_genre`(`game_id`, `genre_id`)
            SELECT `game_id`, `genre_id` FROM `games`, `genres`
            WHERE `game_name` = '%(name)s'
            AND `genre_name` = '%(genre)s';
        ''' % {'name': kwargs['game_name'],
              'genre': genre})

    for publisher in kwargs['publishers']:
        cursor.execute('''
            INSERT IGNORE INTO `publishers`(`publisher_name`)
                SELECT
                '%(publisher)s';
        ''' % {'publisher': publisher})

        cursor.execute('''
            INSERT INTO `game_publisher`(`game_id`, `publisher_id`)
            SELECT `game_id`, `publisher_id` FROM `games`, `publishers`
            WHERE `game_name` = '%(name)s'
            AND `publisher_name` = '%(publisher)s';
        ''' % {'name': kwargs['game_name'],
              'publisher': publisher})


    cursor.execute('''
        INSERT INTO `game_developer`(`game_id`, `developer_id`)
        SELECT `game_id`, `developer_id` FROM `games`, `developers`
        WHERE `game_name` = '%(name)s'
        AND `developer_name` = '%(developer)s';
    ''' % {'name': kwargs['game_name'],
          'developer': kwargs['developer']})

    for platform in kwargs['platforms']:
        cursor.execute('''
            INSERT INTO `game_platform`(`game_id`, `platform_id`)
            SELECT `game_id`, `platform_id` FROM `games`, `platforms`
            WHERE `game_name` = '%(name)s'
            AND `platform_name` = '%(platform)s';
        ''' % {'name': kwargs['game_name'],
              'platform': platform})

    mariadb_connection.commit()
    # for image in kwargs['images']:
    #     cursor.execute('''
    #         INSERT INTO `pictures`(`game_id`, `source`)
    #     ''')
    ...


def search(**kwargs):
    #default game_list
    query = '''
        SELECT DISTINCT `game_name`, `release_date`, `rating`
        FROM `games`
        JOIN `game_genre` USING(`game_id`) JOIN `genres` USING(`genre_id`)
        JOIN `game_platform` USING(`game_id`) JOIN `platforms` USING(`platform_id`)
        JOIN `game_publisher` USING(`game_id`) JOIN `publishers` USING(`publisher_id`)
        JOIN `game_developer` USING(`game_id`) JOIN `developers` USING(`developer_id`)
    '''
    if 'game_name' in  kwargs:
        query += '''WHERE game_name LIKE '%%%(game_name)s%%' ''' % {'game_name': kwargs['game_name']}
    else:
        query += '''WHERE game_name LIKE '%%%%' '''

    if 'genre_name' in  kwargs:
        query += ''' AND genre_name = '%(genre_name)s'
        ''' % {'genre_name': kwargs['genre_name']}

    if 'developer_name' in  kwargs:
        query += ''' AND developer_name='%(developer_name)s'
        ''' % {'developer_name': kwargs['developer_name']}

    if 'year' in  kwargs:
        query += ''' AND YEAR(release_date)='%(year)s'
        ''' % {'year': kwargs['year']}

    if 'platform_name' in  kwargs:
        query += ''' AND platform_name='%(platform)s'
        ''' % {'platform': kwargs['platform_name']}

    query += ''' ORDER BY `rating` DESC;'''

    print(query)

    cursor.execute(query)
    result = cursor.fetchall()
    for row in result:
        print(row)
    return result


def get_game_info():
    pass


Exec_request = {
    "login": log_in,
    'register': register,
    'add_game': add_game,
    'search': search,
    'get_game_info': get_game_info
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
    args = {}
    # add_game(game_name='The Last of Us',
    #           developer='Naughty Dog',
    #           release_date='2013-06-14',
    #           rating='95', 
    #           description='Twenty years after a pandemic radically transformed known civilization, infected humans run amuck and survivors kill one another for sustenance and weapons - literally whatever they can get their hands on. Joel, a salty survivor, is hired to smuggle a fourteen-year-old girl, Ellie, out of a rough military quarantine, but what begins as a simple job quickly turns into a brutal journey across the country',
    #           publishers=['SCEI'],
    #           platforms=['PS3'],
    #           genres=['action', 'rpg'])

    # add_game(game_name='Grand Theft Auto V',
    #           developer='Rockstar North',
    #           release_date='2014-11-18',
    #           rating='97', 
    #           description="Grand Theft Auto 5 melds storytelling and gameplay in unique ways as players repeatedly jump in and out of the lives of the game''s three protagonists, playing all sides of the game''s interwoven story.",
    #           publishers=['Rockstar Games'],
    #           platforms=['PS3', 'PC', 'XBOX one', 'PS4', 'PS3', 'XBOX 360'],
    #           genres=['action', 'adventure'])

    # add_game(game_name='Half-Life 2',
    #           developer='Valve Software',
    #           release_date='2004-11-16',
    #           rating='96', 
    #           description=" By taking the suspense, challenge and visceral charge of the original, and adding startling new realism and responsiveness, Half-Life 2 opens the door to a world where the player''s presence affects everything around him, from the physical environment to the behaviors -- even the emotions -- of both friends and enemies. The player again picks up the crowbar of research scientist Gordon Freeman, who finds himself on an alien-infested Earth being picked to the bone, its resources depleted, its populace dwindling. Freeman is thrust into the unenviable role of rescuing the world from the wrong he unleashed back at Black Mesa. And a lot of people -- people he cares about -- are counting on him.",
    #           publishers=['VU Games'],
    #           platforms=['PC'],
    #           genres=['action', 'shooter'])

    # register(login='admin',
    #          password='strong')
    # log_in(login='admin',
    #       password='strong')

    search(year=2004, game_name='half', developer_name='Valve Software', platform_name='P')
    #run_server(port=8000)