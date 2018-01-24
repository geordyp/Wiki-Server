# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.urls import reverse

from .models import UserAccount

from .util import UserAccountPWHash


class UserAccountTests(TestCase):

    def test_create_user_account_password_failure(self):
        """
        test invalid input for password in user account creation
        """
        # no password
        response = self.client.post(reverse('wikiserver:signup'),data={'username':'uniquename'})
        self.assertEqual(response.status_code, 400)

        # blank password
        response = self.client.post(reverse('wikiserver:signup'),data={'username':'uniquename', 'password':''})
        self.assertEqual(response.status_code, 400)

        # short password
        response = self.client.post(reverse('wikiserver:signup'),data={'username':'uniquename', 'password':'aaa'})
        self.assertEqual(response.status_code, 400)


    def test_create_user_account_username_failure(self):
        """
        test invalid input for username in user account creation
        """
        # no username
        response = self.client.post(reverse('wikiserver:signup'),data={'password':'insecurepassword'})
        self.assertEqual(response.status_code, 400)

        # blank username
        response = self.client.post(reverse('wikiserver:signup'),data={'username':'', 'password':'insecurepassword'})
        self.assertEqual(response.status_code, 400)

        # non-alpha-numeric username
        response = self.client.post(reverse('wikiserver:signup'),data={'username':'yo!', 'password':'insecurepassword'})
        self.assertEqual(response.status_code, 400)

        # non-alpha-numeric username
        response = self.client.post(reverse('wikiserver:signup'),data={'username':'johnny-apple-seed', 'password':'insecurepassword'})
        self.assertEqual(response.status_code, 400)

        # taken username
        self.client.post(reverse('wikiserver:signup'),data={'username':'john', 'password':'insecurepassword'})
        response = self.client.post(reverse('wikiserver:signup'),data={'username':'john', 'password':'insecurepassword'})
        self.assertEqual(response.status_code, 400)


    def test_create_user_account_success(self):
        """
        test valid input for user account creation
        """
        response = self.client.post(reverse('wikiserver:signup'),data={'username':'uniquename', 'password':'insecurepassword'})
        self.assertRedirects(response, reverse('wikiserver:index'))
        self.assertEqual(UserAccount.objects.filter(username='uniquename').count(), 1)


    def test_create_user_account_pwhash_success(self):
        """
        test the creation of a password hash
        """
        u = "uniquename"
        p = "insecurepassword"
        response = self.client.post(reverse('wikiserver:signup'),data={'username':u, 'password':p})
        user = UserAccount.objects.get(username=u)
        self.assertNotEqual(user.pw_hash, p)
        self.assertIn(",", user.pw_hash)
        self.assertEqual(len(user.pw_hash), 70)
