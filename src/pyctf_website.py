#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import bottle

############################## Website ########################################

app = bottle.Bottle()

root = os.path.abspath(os.path.dirname(__file__))

bottle.TEMPLATE_PATH.append(os.path.join(root, "website", "templates"))


config = dict()  # This will be populated when this module is imported


@app.route("/")
@bottle.view("main")
def main_page():
    return {}


@app.route("/web/home")
@bottle.view("home")
def new_page():
    return {}


@app.route("/web/questions")
@bottle.view("questions")
def new_page():
    return {}


@app.route("/web/scoreboard")
@bottle.view("scoreboard")
def new_page():
    return {}


@app.route("/web/login")
@bottle.view("login")
def new_page():
    return {}


@app.route("/static/<filename:path>")
def static_file(filename):
    return bottle.static_file(filename=filename,
                              root=os.path.join(root, "website", "static"))


