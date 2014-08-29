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
logger.setLevel(logging.DEBUG)

root = os.path.abspath(os.path.dirname(__file__))

questions, config, scores, custom_config = dict(), dict(), dict(), dict()
auth, auth_tokens, limits = dict(), dict(), dict()


app = bottle.Bottle()


class PyCTFError(Exception):
    pass


######################### User Management #####################################


@app.route("/login", method="post")
def rest_login():
    global auth_tokens
    incoming_data = bottle.request.json
    user = incoming_data['user']
    password = incoming_data['password']
    try:
        return {"auth_token": login(user, password),
                "timeout": config['auth_time_limit']}
    except Exception as err:
        logger.exception(str(err))
        bottle.redirect("/login", code=403)


def login(user, password):
    if user not in auth and config['anonymous_users']:
        auth[user] = dict(password=hash_pass(password), roles=['user'])
    elif user not in auth:
        raise PyCTFError("User does not exist")
    hashed = hash_pass(password)
    if hashed != auth[user]['password']:
        raise PyCTFError("Password is incorrect")

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


@app.route("/user/auth_refresh", method="post")
def rest_auth_refresh():
    check_auth(bottle.request.json['auth_token'])
    return {"refresh": True}


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
        raise PyCTFError("user '{0}' already exists".format(user))

    auth[user] = dict(password=hash_pass(password), roles=['user'])
    if admin:
        auth[user]['roles'].append("admin")
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


@app.route("/user/list")
def get_users():
    check_auth(bottle.request.json['auth_token'], role="admin")
    return {"data": [(x, True if 'admin' in auth[x]['roles'] else False)
                     for x in auth]}


############################## Challenges #####################################


@app.route("/questions")
def list_questions():
    return {k: {"title": v.get('title'), "tags": v.get('tags')}
            for k, v in questions.items()}


@app.route("/questions/list")
def list_questions():
    return {"data":
            [[k, v.get('title'), ", ".join(v.get('tags', []))]
             for k, v in questions.items()]}


@app.route("/question/<question_number>")
def rest_question(question_number):
    return get_question(question_number)


def get_question(question_number):
    data = questions[question_number]
    uid = uuid.uuid4().hex
    out = dict(time_limit=data['time_limit'], title=data['title'],
               token=uid, question="", data=None, media=None, answer_type=None)

    if "question_script" in data:
        data.update(run_process(data['question_script']))

    out['answer_type'] = data.get('answer_type', None)
    out['question'] = data['question']
    out['data'] = data.get('data', None)

    if "media" in data:
        out['media'] = "/media/{0}".format(data['media'])
    else:
        out['media'] = None

    limits[uid] = dict(start_time=time.time(),
                       data=out['data'],
                       time_limit=out['time_limit'],
                       storage=None if "storage" not in
                                       data else data['storage'])
    save_state()
    return out


@app.route("/question/add")
def rest_add_question():
    incoming_data = bottle.request.json
    check_auth(incoming_data.pop('auth_token'), role="admin")
    try:
        add_question(incoming_data)
    except (KeyError, ValueError, AssertionError):
        bottle.abort(400, "did not provide correct parameters")
    except PyCTFError as err:
        bottle.abort(400, str(err))

    return {}


def add_question(data):
    global questions

    question_number = int(data['question_number'])

    if question_number in questions:
        bottle.abort(400, "Question number already exists")

    out = process_common_question_fields(data, True)

    questions[str(question_number)] = out
    save_questions()


def process_common_question_fields(data, required=False):
    out = dict()

    # Required fields

    if "title" in data:
        out['title'] = data['title']
    elif required:
        raise PyCTFError("Title Required")
    if "time_limit" in data:
        out['time_limit'] = int(data['time_limit'])
    elif required:
        out['time_limit'] = 0
    if "points" in data:
        assert data['points'] >= 0
        out["points"] = int(data['points'])
    elif required:
        out['points'] = 1

    # Required one or other fields

    if "question" in data:
        out['question'] = data['question']
    elif "question_script" in data:
        out['question_script'] = data['question_script']
    elif required:
        raise PyCTFError("No question provided")

    if "answer" in data:
        out['answer'] = data['answer']
    elif "answer_script" in data:
        out['answer_script'] = data['answer_script']
    elif required:
        raise PyCTFError("No answer provided")

    # Optional fields

    if "answer_type" in data:
        assert [x for x in ("boolean", "integer", "string", "list",
                            "dictionary") if x == data['answer_type'].lower()]
        out['answer_type'] = data['answer_type'].lower()
    if "media" in data:
        if not os.path.exists(os.path.join(custom_config['abs_media'],
                                           data['media'])):
            raise PyCTFError("Media specified does not exist in media folder")
        out['media'] = data['media']
    if "data" in data:
        out['data'] = data['data']
    if "tags" in data:
        assert isinstance(data['tags'], list)
        out['tags'] = data['tags']

    try:
        json.dumps(out)
    except ValueError as err:
        raise PyCTFError("Some value entered was not JSON Serializable:"
                         " {0}".format(str(err)))

    return out


@app.route("/question/edit")
def rest_edit_question():
    incoming_data = bottle.request.json
    check_auth(incoming_data.pop('auth_token'), role="admin")
    try:
        edit_question(incoming_data)
    except (KeyError, ValueError, AssertionError):
        bottle.abort(400, "did not provide correct parameters")
    except PyCTFError as err:
        bottle.abort(400, str(err))
    return {}


def edit_question(data):
    global questions

    question_number = int(data['question_number'])

    if question_number not in questions:
        bottle.abort(400, "Question number already exists")

    out = process_common_question_fields(data)

    questions[str(question_number)].update(out)
    save_questions()


@app.route("/question/delete")
def rest_edit_question():
    incoming_data = bottle.request.json
    check_auth(incoming_data.pop('auth_token'), role="admin")
    try:
        delete_question(incoming_data)
    except KeyError:
        bottle.abort(400, "Question does not exist")
    except PyCTFError as err:
        bottle.abort(400, str(err))
    return {}


def delete_question(data):
    global questions

    question_number = str(int(data['question_number']))
    del questions[question_number]
    save_questions()


@app.route("/answer/<question_number>", method="post")
def rest_check_answer(question_number):
    incoming_data = bottle.request.json
    logger.debug("Incoming answer: {0}".format(incoming_data))
    user = check_auth(incoming_data['auth_token'])
    uid = incoming_data['token']
    answer = incoming_data['answer']
    try:
        correct, score = check_answer(answer, user, uid, question_number)
    except PyCTFError as err:
        return {"correct": False, "error": str(err)}
    out = {"correct": correct}
    if correct:
        out['score'] = score
    return out


def check_answer(answer, user, token, question_number):
    match_data = questions[question_number]
    if token not in limits:
        raise PyCTFError("non existent token")

    answer_data = limits.pop(token)

    if answer_data['time_limit']:
        time_spent = time.time() - answer_data['start_time']
        if time_spent >= answer_data['time_limit']:
            raise PyCTFError("time limit of {0} seconds exceeded."
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
            raise PyCTFError("Question not found")

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
    if user not in scores:
        return dict(score=0, completed=[])
    else:
        return dict(score=scores[user]['points'],
                    completed=scores[user]['completed'])


@app.route("/scoreboard")
def get_score():
    return {x: scores[x]['points'] for x in scores}


@app.route("/scoreboard/list")
def get_score():
    return {"data": sorted([[x, scores[x]['points']] for x in scores],
            key=lambda x: x[1])}


@app.route("/recover_token", method="post")
def recover_token():
    token = bottle.request.json['token']
    try:
        del limits[token]
    except KeyError:
        pass
    else:
        save_state()
    return {}


def run_process(command, stdin=None, timeout=15):
        p = Popen(command, shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE,
                  cwd=custom_config['abs_script'])

        stdin = None if not stdin else stdin.encode("utf-8")
        stdout, stderr = p.communicate(input=stdin, timeout=timeout)

        if stderr:
            raise PyCTFError(stderr.decode("utf-8"))

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

@app.route("/media/<filename:path>")
def media_file(filename):
    return bottle.static_file(filename=filename,
                              root=custom_config['abs_media'])


@app.route("/server_info")
def server_info():
    return {"welcome_message": config['welcome_message'],
            "anonymous_users": config['anonymous_users'],
            "encoding": config['encoding']}


def save_state():
    if config['save_state']:
        with open(config['save_file'], "w", encoding="utf-8") as f:
            json.dump(fp=f, obj=dict(tokens=limits, scores=scores), indent=4)


def save_auth():
    if config['save_auth']:
        with open(config['auth_file'], mode="w", encoding="utf-8") as f:
            json.dump(fp=f, obj=auth, indent=4)


def save_questions():
    with open(custom_config['match_file'], mode="w", encoding="utf-8") as f:
        json.dump(fp=f, obj=dict(server=config, questions=questions), indent=4)


def find_admins(users):
    return [user for user in users if 'admin' in users[user]['roles']]


def verify_directories_exist():
    if not os.path.exists(config['working_directory']):
        os.makedirs(config['working_directory'])

    abs_script_dir = os.path.abspath(os.path.join(config['working_directory'],
                                                  config['script_directory']))

    abs_media_dir = os.path.abspath(os.path.join(config['working_directory'],
                                                 config['media_directory']))

    if not os.path.exists(abs_script_dir):
        os.makedirs(abs_script_dir)

    if not os.path.exists(abs_media_dir):
        os.makedirs(abs_media_dir)

    return abs_script_dir, abs_media_dir


def prepare_server(match_file):
    global questions, config, limits, auth, scores, custom_config

    with open(match_file, encoding="utf-8") as f:
        content = json.load(f)

    questions = content['questions']
    config = content['server']

    script_dir, media_dir = verify_directories_exist()

    custom_config['abs_media'] = media_dir
    custom_config['abs_script'] = script_dir
    custom_config['match_file'] = match_file

    os.chdir(os.path.join(root, config['working_directory']))

    if os.path.exists(config['auth_file']):
        with open(config['auth_file'], encoding="utf-8") as f:
            auth = json.load(fp=f)

    if not find_admins(auth):
        add_user('admin', 'admin', admin=True)

    if config['save_state']:
        if os.path.exists(config['save_file']):
            try:
                with open(config['save_file'], encoding="utf-8") as f:
                    saved_state = json.load(fp=f)
            except (OSError, ValueError):
                logger.warning("Could not load data from previous save file")
            else:
                limits.update(saved_state.get('tokens', dict()))
                scores.update(saved_state.get('scores', dict()))


def enable_ssl(key, cert, host, port):
    from cherrypy.wsgiserver.ssl_builtin import BuiltinSSLAdapter
    from cherrypy.wsgiserver.wsgiserver3 import CherryPyWSGIServer

    class SSLServer(bottle.ServerAdapter):

        # noinspection PyMissingConstructor
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


def get_user_arguments():
    import argparse

    parser = argparse.ArgumentParser(description="PyCTF SERVER")
    parser.add_argument("-m", "--match", help="Path to JSON match file",
                        default=os.path.join(root, "../data/match.json"))

    return parser.parse_args()


if __name__ == '__main__':

    args = get_user_arguments()

    prepare_server(args.match)

    server = 'wsgiref' if not config.get('ssl') else enable_ssl(
        key=config['ssl_key'], cert=config['ssl_cert'],
        host=config['host'], port=config['port'])

    if config['website']:
        import pyctf_website
        pyctf_website.config = config
        app.merge(pyctf_website.app.routes)

    bottle.run(app, host=config['host'], port=config['port'], server=server)
