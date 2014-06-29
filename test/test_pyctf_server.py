#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webtest import TestApp
import unittest
import pyctf_server as ps


class TestPyCTFServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ps.prepare_server("test_match.json")

    def test_login(self):
        assert ps.login("user", "user")

    def test_passhash(self):
        # Seed: "2Re68Ik12"
        assert ps.hash_pass("password") == ("68dd4ae05f0ba1f6e9099d562bb7fed4"
                                            "1f6d298784c13b296ab6692a0505a061")

    def test_question(self):
        resp = ps.get_question("1")
        for key in ("token", "time_limit", "question", "data"):
            assert key in resp, "{0} is not in {1}".format(key, resp)
        assert resp["time_limit"] == 10
        assert resp["question"] == "Test Question 1"
        assert resp['data'] is None

    def test_answer(self):
        resp = ps.get_question("1")
        correct, score = ps.check_answer("my_answer", "user",
                                         resp['token'], "1")
        assert correct
        assert score == 1

    def test_run_process(self):
        resp = ps.run_process("echo {\"key\": \"value\"}")
        assert resp['key'] == 'value'


class TestPyCTFServerFunctional(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ps.prepare_server("test_match.json")
        cls.app = TestApp(ps.app)

    def setUp(self):
        self.app.reset()
        pass

    def test_webapp_login(self):
        self.app.post_json("/login", {"user": "user", "password": "user"})

    def test_webapp_question(self):
        resp = self.app.get("/question/1").json
        for key in ("token", "time_limit", "question", "data"):
            assert key in resp, "{0} is not in {1}".format(key, resp)
        assert resp["time_limit"] == 10
        assert resp["question"] == "Test Question 1"
        assert resp['data'] is None

    def test_webapp_answer(self):
        auth = self.app.post_json("/login",
                                  {"user": "user", "password": "user"}).json
        resp = self.app.get("/question/1").json
        resp = self.app.post_json("/answer/1",
                                  {"token": resp['token'],
                                   "auth_token": auth['auth_token'],
                                   "answer": "my_answer"}).json
        assert resp['correct']
        assert resp['score'] == 1



if __name__ == '__main__':
    unittest.main()