import logging
import datetime

from flask import Flask, request, render_template, make_response, jsonify
import jwt

from app.database import init_database
from app.auth.views import registration, authentication
from config import ServerConfig, JsonWebTokenConfig


logging.basicConfig(filename='loggs.log', level=logging.DEBUG)
logger = logging.getLogger(name=__name__)


app = Flask(__name__)


@app.route('/auth/registration', methods=['POST', 'GET'])
def registration_user():
    context = {
        'flag': False
    }
    if request.method == 'GET':
        return render_template('reg.html', content=context)

    registration_status = registration(request)
    context = {
        'flag': True,
        'status': registration_status[0].value
    }
    return render_template('reg.html', content=context)


@app.route('/auth/authentication', methods=['POST', 'GET'])
def authentication_user():
    context = {
        'flag': False
    }
    if request.method == 'GET':
        return render_template('auth.html', content=context)

    authentication_status = authentication(request)
    context = {
        'flag': True,
        'status': authentication_status[0].value
    }

    if authentication_status[0].value.get('status'):
        payload = {
            'name': authentication_status[1].get('name'),
            'email': authentication_status[1].get('email'),
            'exp': datetime.datetime.now() + datetime.timedelta(hours=24)
        }
        jwt_token = jwt.encode(payload, JsonWebTokenConfig.SECRET_KEY,
                               algorithm=JsonWebTokenConfig.ALGORITHM)
        return jsonify(token=jwt_token)

    return render_template('auth.html', content=context)


if __name__ == '__main__':
    init_database()
    app.run(host=ServerConfig.HOST,
            port=ServerConfig.PORT, debug=ServerConfig.DEBUG)