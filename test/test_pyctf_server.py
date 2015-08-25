#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webtest import TestApp
import unittest
import pyctf_server as ps
import os
import shutil

root = os.path.abspath(os.path.dirname(__file__))


def del333():
    try:
        del ps.questions['333']
    except KeyError:
        pass


class TestPyCTF(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        shutil.copy("test_match.json", "original.json")
        ps.prepare_server("test_match.json")

    @classmethod
    def tearDownClass(cls):
        os.rmdir(os.path.join(root, "media"))
        os.rmdir(os.path.join(root, "scripts"))
        os.unlink("test_match.json")
        shutil.move("original.json", "test_match.json")


class TestPyCTFServer(TestPyCTF):

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

    def test_add_user(self):
        ps.add_user("test_user", "test_password")
        assert "test_user" in ps.auth
        del ps.auth['test_user']

    def test_remove_user(self):
        ps.auth['another_test_user'] = dict()
        ps.remove_user('another_test_user')
        assert "another_test_user" not in ps.auth

    def test_add_simple_question(self):
        self.addCleanup(del333)
        incoming_data = dict(question_number=333, question="what is 1+1?",
                             answer=2, title="Example question")
        ps.add_question(incoming_data)
        assert "333" in ps.questions
        incoming_data.pop("question_number")
        assert len([x for x in incoming_data if
                    incoming_data[x] == ps.questions['333'][x]]) == 3

    def test_add_complex_question(self):
        self.addCleanup(del333)
        self.addCleanup(lambda: os.unlink(os.path.join(root,
                                                       "media", "test_file")))
        with open(os.path.join(root, "media", "test_file"), "w") as f:
            f.write("me is a test!")
        incoming_data = dict(question_number=333, question="add the data set",
                             answer=7, title="Example question",
                             points=4, data=[3, 4], media="test_file",
                             tags=["hello", 'there'], answer_type="integer",
                             time_limit=10)
        ps.add_question(incoming_data)
        assert "333" in ps.questions
        incoming_data.pop("question_number")
        assert ps.questions['333'] == incoming_data

    def test_remove_question(self):
        ps.questions["333"] = dict(question="what is 1+1?",
                                   answer=2, title="Example question")
        ps.delete_question(dict(question_number=333))
        assert "333" not in ps.questions


class TestPyCTFServerFailure(TestPyCTF):

    def test_add_question_without_number(self):
        incoming_data = dict(question="what is 1+1?",
                             answer=2, title="Example question")
        self.assertRaises(KeyError, ps.add_question, incoming_data)

    def test_add_question_without_answer(self):
        self.addCleanup(del333)
        incoming_data = dict(question_number=333,
                             question="what is 1+1?", title="Example question")
        self.assertRaises(ps.PyCTFError, ps.add_question, incoming_data)


class TestPyCTFServerFunctional(TestPyCTF):

    @classmethod
    def setUpClass(cls):
        shutil.copy("test_match.json", "original.json")
        ps.prepare_server("test_match.json")
        cls.app = TestApp(ps.app)

    def setUp(self):
        self.app.reset()

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