#!/usr/bin/env python

import os
from os import path
from os.path import dirname

from flask import Flask, send_from_directory


if 'FX_DOC_DEST' in os.environ:
    dest_dir = os.environ['FX_DOC_DEST']
else:
    dest_dir = '.'

app = Flask('Elmetrix Scraper Documentation')

@app.route('/')
def index():
    return send_from_directory(dest_dir, 'index.html')


@app.route('/<path:file_path>', methods=['GET'])
def static_file(file_path):
    return send_from_directory(dest_dir, file_path)
