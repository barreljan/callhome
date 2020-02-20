from flask import request, jsonify
from flask import g
from callhome import app, auth, db_connect
from callhome import version
import pymysql


@app.route('/', defaults={'path': ''})
@app.route('/', methods=['GET'])
def info():
    return jsonify({
        "name": version.PROG_NAME,
        "version": version.VERSION,
        "hostname": version.HOSTNAME,
        "ip": request.remote_addr
    }), 200


@app.route('/settings')
@app.route('/settings', methods=['GET'])
@auth.login_required
def req_settings():
    conn = db_connect()
    curr = conn.cursor(pymysql.cursors.DictCursor)

    sql = """
          SELECT *
            FROM `clients`
           WHERE `username` = '{}'
    """.format(g.username)
    curr.execute(sql)
    user_data = curr.fetchall()

    if len(user_data) == 1:
        return jsonify({
            "id": user_data[0]['id'],
            "username": g.username,
            "ip": user_data[0]['host_ip'],
            "description": user_data[0]['host_description'],
            "location": user_data[0]['location'],
            "preshared": user_data[0]['preshared'],
            "last_change": user_data[0]['last_change']
        }), 200
    else:
        return jsonify({"Error": "Something went wrong"}), 500

