# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.urls import reverse

from .models import UserAccount


class UserAccountTests(TestCase):

    def test_create_user_account_success(self):
        """
        test valid input for user account creation
        """
        response = self.client.post(reverse('wikiserver:createuseraccount'),data={'username':'uniquename', 'password':'insecurepassword'})
        self.assertEqual(response.status_code, 200)


    def test_create_user_account_password_failure(self):
        """
        test invalid input for password in user account creation
        """
        # no password
        response = self.client.post(reverse('wikiserver:createuseraccount'),data={'username':'uniquename'})
        self.assertEqual(response.status_code, 400)

        # blank password
        response = self.client.post(reverse('wikiserver:createuseraccount'),data={'username':'uniquename', 'password':''})
        self.assertEqual(response.status_code, 400)

        # short password
        response = self.client.post(reverse('wikiserver:createuseraccount'),data={'username':'uniquename', 'password':'aaa'})
        self.assertEqual(response.status_code, 400)


    def test_create_user_account_username_failure(self):
        """
        test invalid input for username in user account creation
        """
        # no username
        response = self.client.post(reverse('wikiserver:createuseraccount'),data={'password':'insecurepassword'})
        self.assertEqual(response.status_code, 400)

        # blank username
        response = self.client.post(reverse('wikiserver:createuseraccount'),data={'username':'', 'password':'insecurepassword'})
        self.assertEqual(response.status_code, 400)

        # non-alpha-numeric username
        response = self.client.post(reverse('wikiserver:createuseraccount'),data={'username':'yo!', 'password':'insecurepassword'})
        self.assertEqual(response.status_code, 400)

        # non-alpha-numeric username
        response = self.client.post(reverse('wikiserver:createuseraccount'),data={'username':'johnny-apple-seed', 'password':'insecurepassword'})
        self.assertEqual(response.status_code, 400)

        # taken username
        self.client.post(reverse('wikiserver:createuseraccount'),data={'username':'john', 'password':'insecurepassword'})
        response = self.client.post(reverse('wikiserver:createuseraccount'),data={'username':'john', 'password':'insecurepassword'})
        self.assertEqual(response.status_code, 400)
