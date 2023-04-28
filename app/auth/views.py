from typing import Callable, TypeVar
import logging

from flask import request, render_template
from argon2 import PasswordHasher

from app.auth.schemas import UserModel


logger = logging.getLogger(name=__name__)


template = TypeVar('template')


def registration() -> template:
    '''TODO'''
    response = None
    if request.method == 'POST':
        if request.form['password1'] != request.form['password2']:
            raise ValueError(f'''Password\'s don\'t coincidence!''')

        user = {
            'username': request.form['name'],
            'email': request.form['email'],
            'password': request.form['password1'],
        }

        try:
            user_valid = UserModel(**user)
            try:
                pass
        except Exception as ex:
            raise ValueError(f'''Data don\'t pass the check.
                                Error: {ex}!''')
        else:
            logger.info('''User data will poss the check is success!''')

        return render_template('auth.html', response=response)