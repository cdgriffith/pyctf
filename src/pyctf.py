#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import bottle
import json
import uuid
import time
from subprocess import Popen, PIPE

app = bottle.Bottle()

questions = dict()
config = dict()
limits = dict()


def prepare_server(match_file):
    global questions, config
    with open(match_file) as f:
        content = json.load(f)
    questions = content['questions']
    config = content['server']

@app.route("/")
def main_page():
    return {}


@app.route("/question/<question_number>")
def get_question(question_number):
    match_data = questions[question_number]
    uid = uuid.uuid4().hex
    out = dict(time_limit=0, uuid=uid, question="", data=None)

    if "question_script" in match_data:
        process_data = run_process(match_data['question_script'])

        out.update(process_data)
    else:
        out['question'] = match_data['question']
        out['time_limit'] = match_data.get('time_limit', None)
        out['data'] = match_data.get('data', None)

    limits[uid] = dict(start_time=time.time(),
                       data=out['data'],
                       time_limit=out['time_limit'])

    return out

@app.route("/answer/<question_number>", method="post")
def check_answer(question_number):
    match_data = questions[question_number]
    incoming_data = bottle.request.json

    uid = incoming_data['uid']

    if uid not in limits:
        return {"error": "non existent uid"}

    if limits['time_limit']:
        time_spent = time.time() - limits[uid]['start_time']
        if time_spent >= limits['time_limit']:
            return dict(error="time limit of {0} seconds exceeded."
                              " Time spent: {1}".format(limits['time_limit'],
                                                        time_spent))

    if "answer_script" in match_data:
        process_data = run_process(match_data['answer_script'],
                                   input=dict(data=limits['data'],
                                              answer=incoming_data['data']))
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


def run_process(command, timeout=15, input=None):
        p = Popen(command, shell=True, stdout=PIPE,
                  stderr=PIPE, stdin=PIPE)

        stdout, stderr = p.communicate(input=input, timeout=timeout)

        if stderr:
            raise Exception(stderr)

        return json.loads(stdout)



if __name__ == '__main__':
    import sys
    prepare_server(sys.argv[1])
    bottle.run(app, host=config['host'], port=config['port'])
