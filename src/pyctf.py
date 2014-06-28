#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import bottle
import json
import uuid
import os
import time
from subprocess import Popen, PIPE

questions = dict()
config = dict()
limits = dict()

app = bottle.Bottle()


def prepare_server(match_file):
    global questions, config
    with open(match_file) as f:
        content = json.load(f)
    questions = content['questions']
    config = content['server']
    root = os.path.abspath(os.path.dirname(__file__))
    os.chdir(os.path.join(root, config['working_directory']))


@app.route("/")
def main_page():
    return {}


@app.route("/question/<question_number>")
def get_question(question_number):
    match_data = questions[question_number]
    uid = uuid.uuid4().hex
    out = dict(time_limit=match_data['time_limit'], token=uid, question="", data=None)

    data = match_data if "question_script" not in match_data \
        else run_process(match_data['question_script'])

    out['question'] = data['question']
    out['data'] = data.get('data', None)

    limits[uid] = dict(start_time=time.time(),
                       data=out['data'],
                       time_limit=out['time_limit'],
                       storage=None if "storage" not in data else data['storage'])

    return out


@app.route("/answer/<question_number>", method="post")
def check_answer(question_number):
    match_data = questions[question_number]
    incoming_data = bottle.request.json

    uid = incoming_data['token']

    if uid not in limits:
        return {"error": "non existent token"}

    answer_dats = limits.pop(uid)

    if answer_dats['time_limit']:
        time_spent = time.time() - answer_dats['start_time']
        if time_spent >= answer_dats['time_limit']:
            return dict(error="time limit of {0} seconds exceeded."
                              " Time spent: {1}".format(answer_dats['time_limit'],
                                                        time_spent))

    if "answer_script" in match_data:
        process_data = run_process(match_data['answer_script'],
                                   stdin=json.dumps(dict(data=answer_dats['data'],
                                                         answer=incoming_data['answer'],
                                                         storage=answer_dats['storage'])))
        return process_data
    else:
        try:
            correct_answer = questions[question_number]['answer']
        except KeyError:
            return {"error": "question not found"}

        if incoming_data['answer'] == correct_answer:
            return {"correct": True}
        else:
            return {"correct": False}


def run_process(command, stdin=None, timeout=15):
        p = Popen(command, shell=True, stdout=PIPE,
                  stderr=PIPE, stdin=PIPE)

        stdout, stderr = p.communicate(input=None if not stdin else stdin.encode("utf-8"), timeout=timeout)

        if stderr:
            raise Exception(stderr.decode("utf-8"))

        return json.loads(stdout.decode("utf-8"))


if __name__ == '__main__':
    import sys
    json_file = "../data" if len(sys.argv) != 2 else sys.argv[1]
    prepare_server(json_file)

    if config.get('ssl'):
        from cherrypy.wsgiserver import CherryPyWSGIServer
        from cherrypy.wsgiserver.ssl_builtin import BuiltinSSLAdapter
        server = CherryPyWSGIServer((config['host'], config['port']), app)
        server.ssl_adapter = BuiltinSSLAdapter(config['ssl_cert'],
                                               config['ssl_key'], None)
        server.start()
    else:
        bottle.run(app, host=config['host'], port=config['port'])
