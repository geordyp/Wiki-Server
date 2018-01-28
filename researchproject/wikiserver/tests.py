# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User


class UserTests(TestCase):

    def test_create_user_account_password_failure(self):
        """
        test invalid input for password in user account creation
        """
        # no passwords
        response = self.client.post(reverse('wikiserver:signup'),data={'username':'uniquename'})
        self.assertEqual(response.status_code, 400)

        # no password
        response = self.client.post(reverse('wikiserver:signup'),data={'username':'uniquename', 'verify_password':''})
        self.assertEqual(response.status_code, 400)

        # no verify password
        response = self.client.post(reverse('wikiserver:signup'),data={'username':'uniquename', 'password':''})
        self.assertEqual(response.status_code, 400)

        # blank password and verify password
        response = self.client.post(reverse('wikiserver:signup'),data={'username':'uniquename', 'password':'', 'verify_password':''})
        self.assertEqual(response.status_code, 400)

        # short password
        response = self.client.post(reverse('wikiserver:signup'),data={'username':'uniquename', 'password':'aaa', 'verify_password':'aaa'})
        self.assertEqual(response.status_code, 400)

        # password mismatch
        response = self.client.post(reverse('wikiserver:signup'),data={'username':'uniquename', 'password':'passwordz', 'verify_password':'passwords'})
        self.assertEqual(response.status_code, 400)


    def test_create_user_account_username_failure(self):
        """
        test invalid input for username in user account creation
        """
        # no username
        response = self.client.post(reverse('wikiserver:signup'),data={'password':'password', 'verify_password':'password'})
        self.assertEqual(response.status_code, 400)

        # blank username
        response = self.client.post(reverse('wikiserver:signup'),data={'username':'', 'password':'password', 'verify_password':'password'})
        self.assertEqual(response.status_code, 400)

        # non-alpha-numeric username
        response = self.client.post(reverse('wikiserver:signup'),data={'username':'yo!', 'password':'password', 'verify_password':'password'})
        self.assertEqual(response.status_code, 400)

        # non-alpha-numeric username
        response = self.client.post(reverse('wikiserver:signup'),data={'username':'johnny-apple-seed', 'password':'password', 'verify_password':'password'})
        self.assertEqual(response.status_code, 400)

        # taken username
        self.client.post(reverse('wikiserver:signup'),data={'username':'john', 'password':'password', 'verify_password':'password'})
        response = self.client.post(reverse('wikiserver:signup'),data={'username':'john', 'password':'password', 'verify_password':'password'})
        self.assertEqual(response.status_code, 400)


    def test_create_user_account_success(self):
        """
        test valid input for user account creation
        """
        response = self.client.post(reverse('wikiserver:signup'),data={'username':'uniquename', 'password':'password', 'verify_password':'password'})
        self.assertRedirects(response, reverse('wikiserver:index'))
        self.assertEqual(User.objects.filter(username='uniquename').count(), 1)
