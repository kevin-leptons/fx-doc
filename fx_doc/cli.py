#!/usr/bin/env python

import click

from .doc_builder import build_doc
from .doc_server import serve_doc


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
def clid_serve(dest, port):
    serve_doc(dest, port)
