#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import print_function
import requests
import json


class PyCTF():
    """  Python client to connect to a PyCTF Server. """

    def __init__(self, host="localhost", port=47275,
                 ssl=True, verify_ssl=False):
        self.host = "{0}://{1}:{2}".format("https" if ssl else "http",
                                           host, port)
        self.auth_token = None
        self.verify = verify_ssl
        self.tokens = dict()
        self.media = dict()

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

    def _recover_token(self, question):
        """ Method to help remove old tokens from the server."""
        url = "{0}/recover_token".format(self.host)
        self._request(url, data=dict(token=self.tokens[question]))

    def auth(self, user, password):
        """ Login to the server."""
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
        """ List the question numbers and titles of the available questions."""
        url = "{0}/questions".format(self.host)
        return self._request(url)

    def question(self, question_number):
        """ Return a question and data for it from the server."""
        url = "{0}/question/{1}".format(self.host, question_number)
        resp = self._request(url)
        if question_number in self.tokens:
            self._recover_token(question_number)
        self.tokens[question_number] = resp.pop('token')
        if 'media' in resp:
            self.media[question_number] = resp['media']
        return resp

    def download_media(self, question_number):
        """ Return the contents of the media associated with the question."""
        if question_number not in self.media:
            resp = self.question(question_number)
            if not resp['media']:
                raise Exception("Question {0} does not have media"
                                .format(question_number))
        url = "{0}/media/{1}".format(self.host, self.media[question_number])
        req = requests.get(url, verify=self.verify)
        return req.content

    def answer(self, question_number, answer):
        """ Send an answer to a question back to the server. The answer
         MUST be JSON serializable."""
        self._check_auth()
        url = "{0}/answer/{1}".format(self.host, question_number)
        data = dict(auth_token=self.auth_token,
                    token=self.tokens[question_number],
                    answer=answer)
        return self._request(url, data=data)

    def score(self):
        """ View your score."""
        self._check_auth()
        url = "{0}/score".format(self.host)
        data = dict(auth_token=self.auth_token)
        return self._request(url, data=data)

    def scoreboard(self):
        """ See how you stack up against the competition."""
        return self._request("{0}/scoreboard".format(self.host))

    def change_password(self, old_password, new_password):
        """ Update your password to a new one."""
        self._check_auth()
        url = "{0}/user/change_password".format(self.host)
        data = dict(auth_token=self.auth_token,
                    old_password=old_password, password=new_password)
        return self._request(url, data=data)

    def admin_add_user(self, user, password):
        """ Add a user to the server."""
        self._check_auth()
        url = "{0}/user/add".format(self.host)
        data = dict(auth_token=self.auth_token,
                    user=user, password=password)
        return self._request(url, data=data)

    def admin_remove_user(self, user):
        """ Remove a user from the server. """
        self._check_auth()
        url = "{0}/user/remove".format(self.host)
        data = dict(auth_token=self.auth_token, user=user)
        return self._request(url, data=data)