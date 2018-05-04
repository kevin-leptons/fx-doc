#!/usr/bin/env python

import click
import sys
from os.path import dirname, realpath
from subprocess import Popen

from .doc_builder import build_doc


@click.group()
def cli():
    pass

@cli.command(name='build', help='Build RST document')
@click.argument('src')
@click.argument('dest')
@click.option('--dist', is_flag=True, default=False)
@click.option('--no-pdf', is_flag=True, default=False)
@click.option('--no-html', is_flag=True, default=False)
@click.option('--no-text', is_flag=True, default=False)
@click.option('--force', is_flag=True, default=False)
def cli_build(src, dest, no_pdf, no_html, no_text, force, dist):
    build_doc(src, dest, dist, no_pdf, no_html, no_text, force)


@cli.command(name='serve', help='Serve document on HTTP')
@click.argument('dest')
@click.option('--port', default=8080)
def cli_serve(dest, port):
    curent_dir = dirname(__file__)
    dest = realpath(dest)
    cmd = [
        'gunicorn', '-b', ':' + str(port), 
        '--chdir', curent_dir,
        '--env', 'FX_DOC_DEST={}'.format(dest),
        'doc_server:app'
    ]
    ret = Popen(cmd, cwd=dest).wait()
    sys.exit(ret)
