# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Page


class UserTests(TestCase):
    """
    tests for user actions
    """

    def test_create_user_account_failure(self):
        """
        test invalid input for password in user account creation
        """
        # missing field
        response = self.client.post(reverse('wikiserver:user-join'),
                                    data={'username':'uniquename',
                                          'password':''})
        self.assertEqual(response.status_code, 400)

        # short password
        response = self.client.post(reverse('wikiserver:user-join'),
                                    data={'username':'uniquename',
                                          'password':'aaa',
                                          'verifyPassword':'aaa'})
        self.assertEqual(response.status_code, 400)

        # password mismatch
        response = self.client.post(reverse('wikiserver:user-join'),
                                    data={'username':'uniquename',
                                          'password':'passwordz',
                                          'verifyPassword':'passwords'})
        self.assertEqual(response.status_code, 400)

        # blank username
        response = self.client.post(reverse('wikiserver:user-join'),
                                    data={'username':'',
                                          'password':'password',
                                          'verifyPassword':'password'})
        self.assertEqual(response.status_code, 400)

        # non-alpha-numeric username
        response = self.client.post(reverse('wikiserver:user-join'),
                                    data={'username':'yo!',
                                          'password':'password',
                                          'verifyPassword':'password'})
        self.assertEqual(response.status_code, 400)

        # taken username
        self.client.post(reverse('wikiserver:user-join'),
                         data={'username':'john',
                               'password':'password',
                               'verifyPassword':'password'})
        self.client.get(reverse('wikiserver:user-logout'))

        response = self.client.post(reverse('wikiserver:user-join'),
                                    data={'username':'john',
                                          'password':'password',
                                          'verifyPassword':'password'})
        self.assertEqual(response.status_code, 400)


    def test_create_user_account_success(self):
        """
        test valid input for user account creation
        """
        response = self.client.post(reverse('wikiserver:user-join'),
                                    data={'username':'uniquename',
                                          'password':'password',
                                          'verifyPassword':'password'})
        self.assertRedirects(response, reverse('wikiserver:index'))
        self.assertEqual(User.objects.filter(username='uniquename').count(), 1)


    def test_create_user_account_redirect_success(self):
        """
        when user is logged in, signup should redirect to index
        """
        self.client.post(reverse('wikiserver:user-join'),
                         data={'username':'uniquename',
                               'password':'password',
                               'verifyPassword':'password'})

        response = self.client.get(reverse('wikiserver:user-join'))
        self.assertRedirects(response, reverse('wikiserver:index'))


    def test_user_login_failure(self):
        """
        test invalid username
        """
        self.client.post(reverse('wikiserver:user-join'),
                         data={'username':'uniquename',
                               'password':'password',
                               'verifyPassword':'password'})
        self.client.get(reverse('wikiserver:user-logout'))

        # missing field
        response = self.client.post(reverse('wikiserver:user-login'),
                                    data={'password':'password'})
        self.assertEqual(response.status_code, 400)

        # wrong password
        response = self.client.post(reverse('wikiserver:user-login'),
                                    data={'username':'uniquename',
                                          'password':'wrongpassword'})
        self.assertEqual(response.status_code, 400)


    def test_user_login_success(self):
        """
        test valid user log in
        """
        self.client.post(reverse('wikiserver:user-join'),
                         data={'username':'uniquename',
                               'password':'password',
                               'verifyPassword':'password'})
        self.client.get(reverse('wikiserver:user-logout'))

        response = self.client.post(reverse('wikiserver:user-login'),
                                    data={'username':'uniquename',
                                          'password':'password'})
        self.assertRedirects(response, reverse('wikiserver:index'))


    def test_user_login_redirect_success(self):
        """
        when user is logged in, login should redirect to index
        """
        self.client.post(reverse('wikiserver:user-join'),
                         data={'username':'uniquename',
                               'password':'password',
                               'verifyPassword':'password'})

        response = self.client.get(reverse('wikiserver:user-login'))
        self.assertRedirects(response, reverse('wikiserver:index'))


class PageTests(TestCase):
    """
    tests for page actions
    """

    def test_page_creation_login_required(self):
        """
        test page creation failure when not logged in
        """
        response = self.client.post(reverse('wikiserver:page-create'),
                                    data={'title':'A Good Title',
                                          'content':'And even better content.'})
        self.assertRedirects(response, str(reverse('wikiserver:user-login')) + "?next=/wiki/page/create/")


    def test_page_creation_failure(self):
        """
        test invalid title
        """
        self.client.post(reverse('wikiserver:user-join'),
                         data={'username':'uniquename',
                               'password':'password',
                               'verifyPassword':'password'})

        # missing field
        response = self.client.post(reverse('wikiserver:page-create'),
                                    data={'content':'And even better content.'})
        self.assertEqual(response.status_code, 400)

        # blank title
        response = self.client.post(reverse('wikiserver:page-create'),
                                    data={'title':'',
                                          'content':'And even better content.'})
        self.assertEqual(response.status_code, 400)

        # blank content
        response = self.client.post(reverse('wikiserver:page-create'),
                                    data={'title':'A Great Title',
                                          'content':''})
        self.assertEqual(response.status_code, 400)


    def test_page_creation_success(self):
        """
        test valid page creation
        """
        self.client.post(reverse('wikiserver:user-join'),
                         data={'username':'uniquename',
                               'password':'password',
                               'verifyPassword':'password'})

        t = 'A Great Title'
        c = 'And even better content'
        response = self.client.post(reverse('wikiserver:page-create'),
                                    data={'title':t,
                                          'content':c})

        self.assertRedirects(response, reverse('wikiserver:page-view', args=(1,)))
        self.assertEquals(Page.objects.filter(id=1).count(), 1)

        pages = Page.objects.filter(title=t)
        response = self.client.get(reverse('wikiserver:page-view', args=(pages[0].id,)))
        self.assertEquals(response.status_code, 200)


    def test_page_view_failure(self):
        """
        test failed page view
        """
        # viewing a page that doesn't exist
        response = self.client.get(reverse('wikiserver:page-view', args=(123456,)))
        self.assertEquals(response.status_code, 404)


    def test_page_edit_login_required(self):
        """
        test page creation failure when not logged in
        """
        response = self.client.post(reverse('wikiserver:page-edit', args=(1,)),
                                    data={'title':'A Good Title',
                                          'content':'And even better content.'})
        self.assertRedirects(response, str(reverse('wikiserver:user-login')) + "?next=/wiki/page/1/edit/")


    def test_page_edit_failure(self):
        """
        test failed page edit
        """
        self.client.post(reverse('wikiserver:user-join'),
                         data={'username':'uniquename',
                               'password':'password',
                               'verifyPassword':'password'})

        t = 'A Great Title'
        c = 'And even better content'
        self.client.post(reverse('wikiserver:page-create'),
                         data={'title':t,
                               'content':c})

        pages = Page.objects.filter(title=t)
        pid = pages[0].id

        # can't leave title blank
        response = self.client.post(reverse('wikiserver:page-edit', args=(pid,)),
                                    data={'title':'',
                                          'content':c})
        self.assertEquals(response.status_code, 400)

        # can't leave content blank
        response = self.client.post(reverse('wikiserver:page-edit', args=(pid,)),
                                    data={'title':t,
                                          'content':''})
        self.assertEquals(response.status_code, 400)

        # page doesn't exist
        response = self.client.post(reverse('wikiserver:page-edit', args=(123456,)),
                                    data={'title':t,
                                          'content':''})
        self.assertEquals(response.status_code, 404)

        # only original author can edit their page
        self.client.get(reverse('wikiserver:user-logout'))
        self.client.post(reverse('wikiserver:user-join'),
                         data={'username':'otheruser',
                               'password':'password',
                               'verifyPassword':'password'})

        response = self.client.post(reverse('wikiserver:page-edit', args=(pid,)),
                                    data={'title':'A Brand New Title',
                                          'content':c})

        self.assertEquals(response.status_code, 403)


    def test_page_edit_success(self):
        """
        test successful page edit
        """
        self.client.post(reverse('wikiserver:user-join'),
                         data={'username':'uniquename',
                               'password':'password',
                               'verifyPassword':'password'})

        t = 'A Great Title'
        c = 'And even better content'
        self.client.post(reverse('wikiserver:page-create'),
                         data={'title':t,
                               'content':c})

        pages = Page.objects.filter(title=t)
        originalPage = pages[0]

        newT = 'A Brand New Title'
        response = self.client.post(reverse('wikiserver:page-edit', args=(originalPage.id,)),
                                    data={'title':newT,
                                          'content':c})

        pages = Page.objects.filter(title=newT)
        editedPage = pages[0]
        self.assertRedirects(response, reverse('wikiserver:page-view', args=(editedPage.id,)))


    def test_page_list_success(self):
        """
        test view page list success
        """
        self.client.post(reverse('wikiserver:user-join'),
                         data={'username':'uniquename',
                               'password':'password',
                               'verifyPassword':'password'})

        t = 'A Great Title'
        c = 'And even better content'
        self.client.post(reverse('wikiserver:page-create'),
                         data={'title':t,
                               'content':c})

        response = self.client.get(reverse('wikiserver:page-list', args=(1,)))
        self.assertEquals(response.status_code, 200)

        # chapter (list-page) number too high
        response = self.client.get(reverse('wikiserver:page-list', args=(100,)))
        self.assertRedirects(response, reverse('wikiserver:page-list', args=(1,)))

        # chapter (list-page) number too low
        response = self.client.get(reverse('wikiserver:page-list', args=(0,)))
        self.assertRedirects(response, reverse('wikiserver:page-list', args=(1,)))
