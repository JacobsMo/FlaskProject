import logging

from flask import Flask, request, render_template

from app.database import init_database
from app.auth.views import registration, authentication
from config import ServerConfig


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
    return render_template('auth.html', content=context)


if __name__ == '__main__':
    init_database()
    app.run(host=ServerConfig.HOST,
            port=ServerConfig.PORT, debug=ServerConfig.DEBUG)