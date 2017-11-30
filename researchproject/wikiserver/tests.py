# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.urls import reverse

from .models import UserAccount


class UserAccountTests(TestCase):

    def test_create_user_account_password_invalid(self):
        """
        test invalid form input for password
        """
        # no password
        response = self.client.post(reverse('wikiserver:createuseraccount'),data={'username':'uniquename'})
        self.assertEqual(response.status_code, 400)

        # blank password
        response = self.client.post(reverse('wikiserver:createuseraccount'),data={'username':'uniquename', 'password':''})
        self.assertEqual(response.status_code, 400)

    def test_create_user_account_username_invalid(self):
        """
        test invalid form input for username
        """

        # no username
        response = self.client.post(reverse('wikiserver:createuseraccount'),data={'password':'insecurepassword'})
        self.assertEqual(response.status_code, 400)

        # blank username
        response = self.client.post(reverse('wikiserver:createuseraccount'),data={'username':'', 'password':'insecurepassword'})
        self.assertEqual(response.status_code, 400)
