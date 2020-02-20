from flask import Flask
from flask import g
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash
import pymysql


# Initialize the app
app = Flask(__name__)
auth = HTTPBasicAuth()


def db_connect():
    conn = False
    dbhost = '127.0.0.1'
    dbuser = 'root'
    dbpasswd = '35RH389haufhwa'
    database = 'callhome'
    try:
        conn = pymysql.connect(host=dbhost, user=dbuser, passwd=dbpasswd, db=database)
    except pymysql.Error:
        raise SystemExit("MySQL Error, could not connect: {}".format(dbhost))
    if conn:
        return conn


def verify_pwd(username, password):
    conn = db_connect()
    curr = conn.cursor(pymysql.cursors.DictCursor)
    sql = """
          SELECT `username`, `password`
            FROM `clients`
           WHERE `username` = '{}'
    """.format(username)
    curr.execute(sql)
    user_data = curr.fetchall()

    if len(user_data) == 1:
        if check_password_hash(user_data[0]['password'], password):
            return True
    else:
        return False


@auth.verify_password
def verify_password(username, password):
    """Verify the password"""
    if verify_pwd(username, password):
        g.username = username
        return True
    else:
        return False


from callhome import api

