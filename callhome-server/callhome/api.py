from flask import request, jsonify
from callhome import app
from callhome import auth
from callhome import version


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
    return jsonify({"foo": "bar"}), 200

