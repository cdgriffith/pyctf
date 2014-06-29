#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import unittest
import pyctf


class PyCTFClass(pyctf.PyCTF):

    test_data = dict()

    def _request(self, url, data=None, method="get"):
        self.test_data.update(dict(url=url, data=data, method=method))
        if url.endswith("/login"):
            return {"auth_token": "1"}

class TestPyCTF(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.pyctf = PyCTFClass()

    def test_default_settings(self):
        assert self.pyctf.host == "https://localhost:47275"

    def test_auth(self):
        self.pyctf.auth("user", "password")
        assert self.pyctf.test_data['url'].endswith("/login")
        assert self.pyctf.test_data['data']