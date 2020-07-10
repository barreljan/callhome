import pymysql
from werkzeug.security import check_password_hash
from callhome import config

dbhost = config['DATABASE']['HOST']
dbuser = config['DATABASE']['USER']
dbpasswd = config['DATABASE']['PASS']
database = config['DATABASE']['DB']
try:
    conn = pymysql.connect(host=dbhost, user=dbuser, passwd=dbpasswd, db=database)
except pymysql.Error:
    raise SystemExit(f"MySQL Error, could not connect: {dbhost}")
if conn:
    curr = conn.cursor(pymysql.cursors.DictCursor)


def error(err_nr):
    log(level='error', msg=f"error:{err_nr},user:{g.username},r_ip:{request.remote_addr},path:{request.path}")
    if err_nr == 1009:
        return jsonify({"ok": False,
                        "error": "Invalid, illegal or wrong request or post",
                        "error_code": err_nr}), 200
    if err_nr == 1008:
        return jsonify({"ok": False,
                        "error": "IP Address already in system",
                        "error_code": err_nr}), 200
    if err_nr == 1007:
        return jsonify({"ok": False,
                        "error": "IP Address given not valid",
                        "error_code": err_nr}), 200
    if err_nr == 1006:
        # Not allowed to change settings of other parties
        return jsonify({"ok": False,
                        "error": "Invalid, illegal or wrong request or post",
                        "error_code": err_nr}), 200
    else:
        return jsonify({"ok": False,
                        "error": "Something went wrong, contact the system admin",
                        "error_code": err_nr}), 200


def log(level=None, msg=None):
    if not level or not msg:
        pass
    sql = f"""
          INSERT INTO `log`
          (`level`, `msg`)
          VALUES ('{level}', '{msg}')
    """
    affected_rows = curr.execute(sql)
    if affected_rows != 0:
        try:
            conn.commit()
            curr.close()
            conn.close()
        except pymysql.Error:
            return error(1000)


def verify_pwd(username, password):
    sql = f"""
          SELECT `username`, `password`
            FROM `clients`
           WHERE `username` = '{username}'
    """

    try:
        if curr:
            curr.execute(sql)
            user_data = curr.fetchall()
        else:
            raise pymysql.Error
    except pymysql.Error or pymysql.ProgrammingError:
        return error(1000)

    if len(user_data) == 1:
        if check_password_hash(user_data[0]['password'], password):
            return True
    else:
        return False
