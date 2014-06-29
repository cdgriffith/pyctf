#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webtest import TestApp
import unittest
import pyctf_server as ps


class TestPyCTFServer(unittest.TestCase):

    def setUpClass(cls):
        cls.app = TestApp(ps.app)

    def setUp(self):
        self.app.reset()

    def test_login(self):
        self.app.post("/login", {"user": "user", "password": "user"})


if __name__ == '__main__':
    unittest.main()