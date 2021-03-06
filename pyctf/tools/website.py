#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import bottle

############################## Website ########################################

app = bottle.Bottle()

root = os.path.abspath(os.path.dirname(__file__))

bottle.TEMPLATE_PATH.append(os.path.join(root, os.path.pardir, "website", "templates"))


config = dict()  # This will be populated when this module is imported


@app.route("/")
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


@app.route("/web/admin")
@bottle.view("admin")
def new_page():
    return {}


@app.route("/web/user")
@bottle.view("user")
def new_page():
    return {}


@app.route("/static/<filename:path>")
def static_file(filename):
    return bottle.static_file(filename=filename,
                              root=os.path.join(root, os.path.pardir, "website", "static"))


