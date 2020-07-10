from datetime import datetime
import pymysql
from flask import g
from flask import request, jsonify, Flask
from flask_httpauth import HTTPBasicAuth
from callhome.server import conn, curr, log
from callhome.shared import version

# Initialize the app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    """Verify the password"""
    if verify_pwd(username, password):
        g.username = username
        return True
    else:
        return False


@app.errorhandler(404)
def page_not_found(err):
    log(level='error',
        msg=f"error:404,r_ip:{request.remote_addr},method:{request.method},path:{request.path},err:{err}")
    return jsonify({"ok": False,
                    "error": "Page or route not found",
                    "error_code": 404}), 404


@app.errorhandler(500)
def server_error(err):
    log(level='error',
        msg=f"error:500,r_ip:{request.remote_addr},method:{request.method},path:{request.path},err:{err}")
    return jsonify({"ok": False,
                    "error": "Something went wrong, contact the system admin",
                    "error_code": 500}), 500


@app.route('/', defaults={'path': ''})
@app.route('/', methods=['GET'])
def info():
    return jsonify({
        "name": version.PROG_NAME,
        "version": version.VERSION,
        "hostname": version.HOSTNAME,
        "ip": request.remote_addr,
    }), 200


@app.route('/show/current_ip', methods=['GET'])
def curr_ip():
    return jsonify({'ip': request.remote_addr})


@app.route('/show/settings/<username>', methods=['GET'])
@auth.login_required
def req_settings(username):
    sql = f"""
          SELECT *
            FROM `clients`
           WHERE `username` = '{username}'
    """

    curr.execute(sql)
    user_data = curr.fetchall()

    if len(user_data) == 1:
        curr.close()
        conn.close()
        return jsonify({
            "ok": True,
            "result": [{"id": user_data[0]['id'],
                        "username": user_data[0]['username'],
                        "config_ip": user_data[0]['host_ip'],
                        'current_ip': request.remote_addr,
                        "description": user_data[0]['host_description'],
                        "location": user_data[0]['location'],
                        "preshared": user_data[0]['preshared'],
                        "last_change": user_data[0]['last_change']}]
        }), 200
    else:
        return error(1000)


@app.route('/update/settings/<username>/ip/<ip>', methods=['POST'])
@auth.login_required
def upd_settings(username, ip):
    if g.username != username:
        return error(1006)

    try:
        ip_val = ip.split('.')
        if len(ip_val) != 4:
            raise ValueError
        else:
            for i in ip_val:
                int(i)
    except ValueError:
        return error(1007)

    sql = f"""
          SELECT *
            FROM `clients`
           WHERE `username` = '{username}'
    """

    curr.execute(sql)
    user_data = curr.fetchall()

    if len(user_data) == 1:
        sql = """
            UPDATE `clients` SET `host_ip` = %s, `last_change` = %s WHERE `id` = %s
        """
        try:
            change_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            affected_rows = curr.execute(sql, (ip, change_time, user_data[0]['id']))
            if affected_rows != 0:
                conn.commit()
                curr.close()
                conn.close()
                return jsonify({
                    "id": user_data[0]['id'],
                    "description": user_data[0]['host_description'],
                    "old_ip": user_data[0]['host_ip'],
                    "new_ip": ip,
                    "receive_time": change_time,
                    "changed": True
                }), 200
            else:
                return error(1008)
        except pymysql.ProgrammingError as ex:
            return server_error(ex)
    else:
        return error(1000)
