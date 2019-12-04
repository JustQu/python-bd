import MySQLdb as mariadb
import datetime
from sql_errno import *

mariadb_connection = mariadb.connect(user="dmelessa", password='ahegao', database='test')
cursor = mariadb_connection.cursor()

def create_db():
    query = """
    CREATE TABLE IF NOT EXISTS `users` (
        `id` INT NOT NULL UNIQUE PRIMARY KEY AUTO_INCREMENT,
        `login` VARCHAR(20) NOT NULL UNIQUE,
        `group` ENUM('admin', 'editor', 'user') NOT NULL,
        `created_at` DATE NOT NULL
    );
    """
    cursor.execute(query)
    mariadb_connection.commit()

def create_user(login, passwd):
    now = datetime.datetime.now()
    query1 = """
    INSERT INTO `users`(`login`, `group`, `created_at`)
        VALUES
        ('%s', 'user', '%s');
    """ % (login, now.strftime("%Y-%m-%d"))

    try:
        cursor.execute(query1)
    except mariadb_connection.Error as e:
        if e.args[0] == error['Duplicate_entry']:
            print("Пользователь с таким именем уже существует.")
        else:
            print("smthng else")
    mariadb_connection.commit()

create_db()
create_user("test", "1")
mariadb_connection.close()