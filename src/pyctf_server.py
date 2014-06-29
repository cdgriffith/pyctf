#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import print_function
import bottle
import json
import uuid
import os
import time
from subprocess import Popen, PIPE
import logging
import hashlib

logger = logging.getLogger(__file__)

questions, config, scores = dict(), dict(), dict()
auth, auth_tokens, limits = dict(), dict(), dict()

app = bottle.Bottle()


@app.route("/")
def main_page():
    return {}

######################### User Management #####################################


@app.route("/login", method="post")
def rest_login():
    global auth_tokens
    incoming_data = bottle.request.json
    user = incoming_data['user']
    password = incoming_data['password']
    try:
        return {"auth_token": login(user, password)}
    except Exception:
        bottle.redirect("/login", code=403)


def login(user, password):
    if user not in auth and config['anonymous_users']:
        auth[user] = dict(password=hash_pass(password), roles=['user'])
    elif user not in auth:
        raise Exception()
    hashed = hash_pass(password)
    if hashed != auth[user]['password']:
        raise Exception()

    token = uuid.uuid4().hex
    timeout = time.time() + config['auth_time_limit']

    auth_tokens[token] = dict(timeout=timeout,
                              user=user, roles=auth[user]['roles'])
    return token


def hash_pass(password):
    return hashlib.sha256("{0}{1}".format(password, config['seed'])
                          .encode(config['encoding'])).hexdigest()


def check_auth(token, role="user"):
    if token not in auth_tokens:
        bottle.redirect("/login", code=403)

    if auth_tokens[token]['timeout'] > time.time():
        auth_tokens[token]['timeout'] = (time.time() +
                                         config['auth_time_limit'])
    else:
        bottle.redirect("/login", code=403)
    if role not in auth_tokens[token]['roles']:
        bottle.abort(403, "Not authorized to view this area")

    return auth_tokens[token]['user']


@app.route("/user/change_password", method="post")
def rest_change_password():
    global auth, auth_tokens
    incoming_data = bottle.request.json
    user = check_auth(incoming_data['auth_token'])
    password = incoming_data['password']
    old_password = incoming_data['old_password']
    return {"changed": change_password(user, password, old_password)}


def change_password(user, password, old_password):
    if not user in auth:
        return False
    hashed = hash_pass(old_password)
    if hashed != auth[user]['password']:
        return False

    hashed = hashlib.sha256("{0}{1}".format(password, config['seed'])
                            .encode(config['encoding'])).hexdigest()
    auth[user]['password'] = hashed

    token = uuid.uuid4().hex
    timeout = time.time() + config['auth_time_limit']

    auth_tokens[token] = dict(timeout=timeout,
                              user=user, roles=auth[user]['roles'])
    save_auth()
    return True


@app.route("/user/add", method="post")
def rest_add_user():
    incoming_data = bottle.request.json
    check_auth(incoming_data['auth_token'], role="admin")
    user = incoming_data['user']
    password = incoming_data['password']
    admin = incoming_data.get('admin', False)
    try:
        add_user(user, password, admin)
    except Exception as err:
        return {"error": str(err)}
    return {}


def add_user(user, password, admin=False):
    if user in auth:
        raise Exception("user '{0}' already exists".format(user))

    auth[user] = dict(password=hash_pass(password), roles=['user'])
    if admin:
        auth[user].append("admin")
    save_auth()


@app.route("/user/remove", method="post")
def rest_remove_user():
    incoming_data = bottle.request.json
    check_auth(incoming_data['auth_token'], role="admin")
    user = incoming_data['user']
    remove_user(user)
    return {}


def remove_user(user):
    if user not in auth:
        return {"error": "user '{0}' does not exists".format(user)}
    del auth[user]
    if user in scores:
        del scores[user]
        save_state()
    save_auth()


############################## Challenges #####################################


@app.route("/questions")
def list_questions():
    return {k: {"title": v.get('title'), "tags": v.get('tags')}
            for k, v in questions.items()}


@app.route("/question/<question_number>")
def rest_question(question_number):
    return get_question(question_number)


def get_question(question_number):
    match_data = questions[question_number]
    uid = uuid.uuid4().hex
    out = dict(time_limit=match_data['time_limit'],
               token=uid, question="", data=None)

    data = match_data if "question_script" not in match_data \
        else run_process(match_data['question_script'])

    out['question'] = data['question']
    out['data'] = data.get('data', None)

    limits[uid] = dict(start_time=time.time(),
                       data=out['data'],
                       time_limit=out['time_limit'],
                       storage=None if "storage" not in
                                       data else data['storage'])
    save_state()
    return out


@app.route("/answer/<question_number>", method="post")
def rest_check_answer(question_number):
    incoming_data = bottle.request.json
    user = check_auth(incoming_data['auth_token'])
    uid = incoming_data['token']
    answer = incoming_data['answer']
    correct, score = check_answer(answer, user, uid, question_number)
    out = {"correct": correct}
    if correct:
        out['score'] = score
    return out


def check_answer(answer, user, token, question_number):
    match_data = questions[question_number]
    if token not in limits:
        return {"error": "non existent token"}

    answer_data = limits.pop(token)

    if answer_data['time_limit']:
        time_spent = time.time() - answer_data['start_time']
        if time_spent >= answer_data['time_limit']:
            return dict(error="time limit of {0} seconds exceeded."
                              " Time spent: {1}".format(
                        answer_data['time_limit'], time_spent))

    correct = False

    if "answer_script" in match_data:
        process_data = run_process(match_data['answer_script'],
                                   stdin=json.dumps(
                                       dict(data=answer_data['data'],
                                            answer=answer,
                                            storage=answer_data['storage'])))
        correct = process_data['correct']
    else:
        try:
            correct_answer = questions[question_number]['answer']
        except KeyError:
            return {"error": "question not found"}

        if answer == correct_answer:
            correct = True

    if correct:
        score = update_score(user, question_number)
        return correct, score
    return correct, 0


@app.route("/score", method="post")
def get_score():
    auth_token = bottle.request.json['auth_token']
    user = check_auth(auth_token)
    return dict(score=scores[user]['points'])


@app.route("/recover_token", method="post")
def recover_token():
    token = bottle.request.json['token']
    del limits[token]
    save_state()
    return {}


def run_process(command, stdin=None, timeout=15):
        p = Popen(command, shell=True, stdout=PIPE,
                  stderr=PIPE, stdin=PIPE)

        stdin = None if not stdin else stdin.encode("utf-8")
        stdout, stderr = p.communicate(input=stdin, timeout=timeout)

        if stderr:
            raise Exception(stderr.decode("utf-8"))

        return json.loads(stdout.decode("utf-8"))


def update_score(user, question):
    global scores
    points = questions[question].get("points", 1)
    if user not in scores:
        scores[user] = dict(completed=[question], points=points)
    else:
        if question not in scores[user]['completed']:
            scores[user]['completed'].append(question)
            scores[user]['points'] += points
    return scores[user]['points']


################################# Server #####################################

def save_state():
    if config['save_state']:
        with open(config['save_file'], "w", encoding="utf-8") as f:
            json.dump(fp=f, obj=dict(tokens=limits, scores=scores), indent=4)


def save_auth():
    if config['save_auth']:
        with open(config['auth_file'], mode="w", encoding="utf-8") as f:
            json.dump(fp=f, obj=auth, indent=4)


def prepare_server(match_file):
    global questions, config, limits, auth, scores

    with open(match_file, encoding="utf-8") as f:
        content = json.load(f)

    questions = content['questions']
    config = content['server']

    root = os.path.abspath(os.path.dirname(__file__))
    os.chdir(os.path.join(root, config['working_directory']))

    if os.path.exists(config['auth_file']):
        with open(config['auth_file'], encoding="utf-8") as f:
            auth = json.load(fp=f)

    if config['save_state']:
        if os.path.exists(config['save_file']):
            try:
                with open(config['save_file'], encoding="utf-8") as f:
                    save_state = json.load(fp=f)
            except (OSError, ValueError):
                logger.warning("Could not load data from previous save file")
            else:
                limits.update(save_state.get('tokens', dict()))
                scores.update(save_state.get('scores', dict()))


def enable_ssl(key, cert, host, port):
    from cherrypy.wsgiserver.ssl_builtin import BuiltinSSLAdapter
    from cherrypy.wsgiserver.wsgiserver3 import CherryPyWSGIServer

    class SSLServer(bottle.ServerAdapter):

        def __init__(self, **options):
            self.host = host
            self.port = port
            self.options = options

        def run(self, handler):
            ssl_server = CherryPyWSGIServer((self.host, self.port), handler)
            ssl_server.ssl_adapter = BuiltinSSLAdapter(private_key=key,
                                                       certificate=cert)
            try:
                ssl_server.start()
            finally:
                ssl_server.stop()
    return SSLServer


if __name__ == '__main__':
    import sys
    json_file = "../data/match.json" if len(sys.argv) != 2 else sys.argv[1]
    prepare_server(json_file)

    server = 'wsgiref' if not config.get('ssl') else enable_ssl(
        key=config['ssl_key'], cert=config['ssl_cert'],
        host=config['host'], port=config['port'])

    bottle.run(app, host=config['host'], port=config['port'], server=server)


