#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import bottle
import json

app = bottle.Bottle()

questions = dict()
config = dict()


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
    try:
        return questions[question_number]['question']
    except KeyError:
        return {"error": "question not found"}


@app.route("/answer/<question_number>", method="post")
def check_answer(question_number):
    data = bottle.request.json

    try:
        correct_answer = questions[question_number]['answer']
    except KeyError:
        return {"error": "question not found"}

    if data['answer'] == correct_answer:
        return {"correct": True}
    else:
        return {"correct": False}


if __name__ == '__main__':
    import sys
    prepare_server(sys.argv[1])
    bottle.run(app)
