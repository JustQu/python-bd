import MySQLdb as mariadb
import datetime
from sql_errno import *

mariadb_connection = mariadb.connect(user="dmelessa", password='ahegao', database='video_games')
cursor = mariadb_connection.cursor()