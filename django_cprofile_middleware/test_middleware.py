import unittest
from unittest import mock

from django.conf import settings
from django import http
from django import test
from django import views
from django.test import client

from django_cprofile_middleware import middleware

settings.configure()


class MiddlewareTest(unittest.TestCase):

    class SampleView(views.View):

        def get(self, request):
            return http.HttpResponse()

    def setUp(self):
        self.view = MiddlewareTest.SampleView()
        self.middleware = middleware.ProfilerMiddleware(None)
        self.request = client.RequestFactory().get('/sample/?prof')
        self.default_response = http.HttpResponse('default response')
        self.override_settings = {'DEBUG': True}
        self.profile_content = '<pre>'.encode('utf-8')

    def test_profile(self):
        with test.override_settings(**self.override_settings):
            response = self.middleware.process_view(
                self.request, self.view.get, (), {})
        self.assertTrue(response.content.startswith(self.profile_content))
        self.assertIn('function calls'.encode('utf-8'), response.content)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

    def test_download_profile(self):
        request = client.RequestFactory().get('/sample/?prof&download')
        with test.override_settings(**self.override_settings):
            response = self.middleware.process_view(
                request, self.view.get, (), {})
        self.assertEqual(response['Content-Type'], 'application/octet-stream')

    def test_get_param_required(self):
        request = client.RequestFactory().get('/sample/')
        with test.override_settings(**self.override_settings):
            response = self.middleware.process_view(
                request, self.view.get, (), {})
        self.assertIsNone(response)

    def test_debug_required(self):
        request = client.RequestFactory().get('/sample/?prof')
        self.override_settings['DEBUG'] = False
        with test.override_settings(**self.override_settings):
            response = self.middleware.process_view(
                request, self.view, (), {})
        self.assertIsNone(response)
