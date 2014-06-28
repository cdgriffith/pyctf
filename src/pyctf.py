#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import print_function
import requests
import json


class PyCTF():

    def __init__(self, host="localhost", port=47275,
                 ssl=True, verify_ssl=False):
        self.host = "{0}://{1}:{2}".format("https" if ssl else "http",
                                           host, port)
        self.auth_token = None
        self.verify = verify_ssl
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
                raise Exception("Forbidden area")
            else:
                raise Exception(req.text)
        try:
            return req.json()
        except ValueError:
            raise Exception("Server did not return json: {0}".format(req.text))

    def _check_auth(self):
        if not self.auth_token:
            raise Exception("Authenticate with .auth(username, password))")

    def auth(self, user, password):
        url = "{0}/login".format(self.host)
        data = dict(user=user, password=password)
        try:
            resp = self._request(url, data)
        except Exception as err:
            if "Forbidden" in str(err):
                raise Exception("Incorrect password")
            else:
                raise err
        else:
            self.auth_token = resp['auth_token']

    def questions(self):
        url = "{0}/questions".format(self.host)
        return self._request(url)

    def question(self, question_number):
        url = "{0}/question/{1}".format(self.host, question_number)
        resp = self._request(url)
        self.tokens[question_number] = resp.pop('token')
        return resp

    def answer(self, question_number, answer):
        self._check_auth()
        url = "{0}/answer/{1}".format(self.host, question_number)
        data = dict(auth_token=self.auth_token,
                    token=self.tokens[question_number],
                    answer=answer)
        return self._request(url, data=data)

    def score(self):
        self._check_auth()
        url = "{0}/score".format(self.host)
        data = dict(auth_token=self.auth_token)
        return self._request(url, data=data)

    def change_password(self, old_password, new_password):
        self._check_auth()
        url = "{0}/user/change_password".format(self.host)
        data = dict(auth_token=self.auth_token,
                    old_password=old_password, password=new_password)
        return self._request(url, data=data)

    def admin_add_user(self, user, password):
        self._check_auth()
        url = "{0}/user/add".format(self.host)
        data = dict(auth_token=self.auth_token,
                    user=user, password=password)
        return self._request(url, data=data)

    def admin_remove_user(self, user):
        self._check_auth()
        url = "{0}/user/remove".format(self.host)
        data = dict(auth_token=self.auth_token, user=user)
        return self._request(url, data=data)