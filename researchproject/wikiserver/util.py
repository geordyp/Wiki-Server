# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User

import hashlib
import random
import string


class CreateUserValidation():

    @staticmethod
    def isValidUsername(username):
        if len(username) < 1:
            return {'isValid':False, 'message':'Username is blank'}

        if not username.isalnum():
            return {'isValid':False, 'message':'Invalid username, please only use letters and numbers'}

        if User.objects.filter(username=username).count() > 0:
            return {'isValid':False, 'message':'This username is already taken'}

        return {'isValid':True, 'message':'valid username'}


    @staticmethod
    def isValidPassword(password):
        if len(password) == 0:
            return {'isValid':False, 'message':'Password is blank'}

        if len(password) < 4:
            return {'isValid':False, 'message':'Invalid password, please create a password with at least 4 characters'}

        return {'isValid':True, 'message':'valid username'}
