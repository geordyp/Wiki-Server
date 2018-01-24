# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .models import UserAccount

import hashlib
import random

class UserAccountValidation():

    @staticmethod
    def isValidUsername(username):
        validation = {'isValid':True, 'message':'valid username'}

        if len(username) < 1:
            validation['isValid'] = False
            validation['message'] = 'Username is blank'

        if not username.isalnum():
            validation['isValid'] = False
            validation['message'] = 'Invalid username, please only use letters and numbers'

        if UserAccount.objects.filter(username = username).count() > 0:
            validation['isValid'] = False
            validation['message'] = 'This username is already taken'

        return validation

    @staticmethod
    def isValidPassword(password):
        validation = {'isValid':True, 'message':'valid username'}

        if len(password) < 4:
            validation['isValid'] = False
            validation['message'] = 'Invalid password, please create a password with at least 4 characters'

        return validation


class UserAccountPWHash():
    @staticmethod
    def make_pw_hash(name, pw, salt=None):
        if not salt:
            salt = make_salt()
        h = hashlib.sha256(name + pw + salt).hexdigest()
        return "%s,%s" % (h, salt)

    @staticmethod
    def make_salt(length=5):
        return "".join(random.choice(string.letters) for x in xrange(length))
