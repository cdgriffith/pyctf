#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import requests
import json

class PyCTF():

    def __init__(self, host="https://localhost:47275", verify_ssl=False):
        self.auth_token = None
        self.verify = verify_ssl
        self.host = host.rstrip("/")
        self.tokens = dict()

    def _request(self, url, data=None, method="get"):
        if method.lower() == "post" or data:
            req = requests.post(url,
                                data=json.dumps(data),
                                headers={'Content-type': 'application/json',
                                         'Accept': 'text/plain'},
                                verify=self.verify)
        elif method.lower() == "get":
            req = requests.get(url, verify=self.verify)
        else:
            raise Exception("Wrong method")
        if req.status_code != 200:
            if req.status_code == 403:
                raise Exception("Not yet authenticated, please use .auth")
            else:
                raise Exception(req.text)
        return req.json()

    def auth(self, user, password):
        url = "{0}/login".format(self.host)
        data = dict(user=user, password=password)
        resp = self._request(url, data)
        self.auth_token = resp['auth_token']

    def questions(self):
        url = "{0}/questions".format(self.host)
        return self._request(url)

    def question(self, question_number):
        url = "{0}/question/{1}".format(self.host, question_number)
        resp = self._request(url)
        self.tokens[question_number] = resp['token']
        return resp

    def answer(self, question_number, answer):
        if not self.auth_token:
            raise Exception("Authenticate with .auth(username, password))")
        url = "{0}/answer/{1}".format(self.host, question_number)
        data = dict(auth_token=self.auth_token,
                    token=self.tokens[question_number],
                    answer=answer)
        return self._request(url, data=data)

    def score(self):
        if not self.auth_token:
            raise Exception("Authenticate with .auth(username, password))")
        url = "{0}/score".format(self.host)
        data = dict(auth_token=self.auth_token)
        return self._request(url, data=data)