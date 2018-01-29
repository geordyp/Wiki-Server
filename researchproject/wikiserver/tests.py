# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User


class UserTests(TestCase):
    """
    tests for user actions
    """

    def test_create_user_account_password_failure(self):
        """
        test invalid input for password in user account creation
        """
        # no passwords
        response = self.client.post(reverse('wikiserver:user-signup'),
                                    data={'username':'uniquename'})
        self.assertEqual(response.status_code, 400)

        # no password
        response = self.client.post(reverse('wikiserver:user-signup'),
                                    data={'username':'uniquename',
                                          'verifyPassword':''})
        self.assertEqual(response.status_code, 400)

        # no verify password
        response = self.client.post(reverse('wikiserver:user-signup'),
                                    data={'username':'uniquename',
                                          'password':''})
        self.assertEqual(response.status_code, 400)

        # blank password and verify password
        response = self.client.post(reverse('wikiserver:user-signup'),
                                    data={'username':'uniquename',
                                          'password':'',
                                          'verifyPassword':''})
        self.assertEqual(response.status_code, 400)

        # short password
        response = self.client.post(reverse('wikiserver:user-signup'),
                                    data={'username':'uniquename',
                                          'password':'aaa',
                                          'verifyPassword':'aaa'})
        self.assertEqual(response.status_code, 400)

        # password mismatch
        response = self.client.post(reverse('wikiserver:user-signup'),
                                    data={'username':'uniquename',
                                          'password':'passwordz',
                                          'verifyPassword':'passwords'})
        self.assertEqual(response.status_code, 400)


    def test_create_user_account_username_failure(self):
        """
        test invalid input for username in user account creation
        """
        # no username
        response = self.client.post(reverse('wikiserver:user-signup'),
                                    data={'password':'password',
                                          'verifyPassword':'password'})
        self.assertEqual(response.status_code, 400)

        # blank username
        response = self.client.post(reverse('wikiserver:user-signup'),
                                    data={'username':'',
                                          'password':'password',
                                          'verifyPassword':'password'})
        self.assertEqual(response.status_code, 400)

        # non-alpha-numeric username
        response = self.client.post(reverse('wikiserver:user-signup'),
                                    data={'username':'yo!',
                                          'password':'password',
                                          'verifyPassword':'password'})
        self.assertEqual(response.status_code, 400)

        # non-alpha-numeric username
        response = self.client.post(reverse('wikiserver:user-signup'),
                                    data={'username':'johnny-apple-seed',
                                          'password':'password',
                                          'verifyPassword':'password'})
        self.assertEqual(response.status_code, 400)

        # taken username
        self.client.post(reverse('wikiserver:user-signup'),
                         data={'username':'john',
                               'password':'password',
                               'verifyPassword':'password'})
        response = self.client.post(reverse('wikiserver:user-signup'),
                                    data={'username':'john',
                                          'password':'password',
                                          'verifyPassword':'password'})
        self.assertEqual(response.status_code, 400)


    def test_create_user_account_success(self):
        """
        test valid input for user account creation
        """
        response = self.client.post(reverse('wikiserver:user-signup'),
                                    data={'username':'uniquename',
                                          'password':'password',
                                          'verifyPassword':'password'})
        self.assertRedirects(response, reverse('wikiserver:index'))
        self.assertEqual(User.objects.filter(username='uniquename').count(), 1)


    def test_create_user_account_redirect_success(self):
        """
        when user is logged in, signup should redirect to index
        """
        self.client.post(reverse('wikiserver:user-signup'),
                         data={'username':'uniquename',
                               'password':'password',
                               'verifyPassword':'password'})

        response = self.client.get(reverse('wikiserver:user-signup'))
        self.assertRedirects(response, reverse('wikiserver:index'))


    def test_user_login_failure(self):
        """
        test invalid user log in
        """
        self.client.post(reverse('wikiserver:user-signup'),
                         data={'username':'uniquename',
                               'password':'password',
                               'verifyPassword':'password'})
        self.client.get(reverse('wikiserver:user-logout'))

        # wrong password
        response = self.client.post(reverse('wikiserver:user-login'),
                                    data={'username':'uniquename',
                                          'password':'wrongpassword'})
        self.assertEqual(response.status_code, 400)


    def test_user_login_success(self):
        """
        test valid user log in
        """
        self.client.post(reverse('wikiserver:user-signup'),
                         data={'username':'uniquename',
                               'password':'password',
                               'verifyPassword':'password'})
        self.client.get(reverse('wikiserver:user-logout'))

        # wrong password
        response = self.client.post(reverse('wikiserver:user-login'),
                                    data={'username':'uniquename',
                                          'password':'password'})
        self.assertRedirects(response, reverse('wikiserver:index'))


    def test_user_login_redirect_success(self):
        """
        when user is logged in, login should redirect to index
        """
        self.client.post(reverse('wikiserver:user-signup'),
                         data={'username':'uniquename',
                               'password':'password',
                               'verifyPassword':'password'})

        response = self.client.get(reverse('wikiserver:user-login'))
        self.assertRedirects(response, reverse('wikiserver:index'))
