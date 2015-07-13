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

@app.route("/new")
@bottle.view("new")
def new_page():
    return {}

@app.route("/static/<filename:path>")
def static_file(filename):
    return bottle.static_file(filename=filename,
                              root=os.path.join(root, "website", "static"))


