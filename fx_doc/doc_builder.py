import subprocess
import yaml
import os
import shutil
import json
from os import path
from pkg_resources import resource_filename

import htmlmin
import pathlib
import csscompressor
import jsmin
from pathlib import Path
from PIL import Image

conf_dir = resource_filename(__name__, 'sphinx_theme')


class build_config():
    def __init__(self, name, version, license, author):
        self.name = name
        self.version = version
        self.license = license
        self.author = author


class build_spec():
    def __init__(self, src_dir, dest_dir, name, version, license, author,
                 force):
        self.src_dir = src_dir
        self.dest_dir = dest_dir
        self.name = name
        self.version = version
        self.license = license
        self.author = author
        self.force = force


def read_packge_config_file(config_file):
    f = open(config_file, 'r')
    raw_config = yaml.load(f.read())
    f.close()
    return build_config(
            raw_config['name'], raw_config['version'], raw_config['license'],
            raw_config['author']
    )


def mk_build_spec(src_dir, dest_dir, force):
    config_file = path.join(src_dir, 'index.yaml')
    config = read_packge_config_file(config_file)
    return build_spec(
        src_dir, dest_dir,
        config.name, config.version, config.license, config.author,
        force
    )


def build_html_from_rst(spec, pdf_file, text_file):
    pdf_file_name = None
    if pdf_file is not None:
        pdf_file_name = Path(pdf_file).name

    text_file_name = None
    if text_file is not None:
        text_file_name = Path(text_file).name

    cmd = [
            'sphinx-build', '-b', 'html',
            '-c', str(conf_dir),
            '-D', 'project={}'.format(spec.name),
            '-D', 'version={}'.format(spec.version),

            '-A', 'license={}'.format(spec.license),
            '-A', 'author={}'.format(spec.author),
            '-A', 'pdf_file_name={}'.format(pdf_file_name),
            '-A', 'pdf_file={}'.format(pdf_file),
            '-A', 'text_file_name={}'.format(text_file_name),
            '-A', 'text_file={}'.format(text_file),
            spec.src_dir, spec.dest_dir
    ]
    if spec.force:
        cmd.append('-a')
    print(' '.join(cmd))
    subprocess.call(cmd)


def build_html(spec, pdf_file, text_file):
    build_html_from_rst(spec, pdf_file, text_file)
    mk_progressive_web_app(spec)
    mk_favicon(spec)


def mk_progressive_web_app(spec):
    mk_manifest_file(spec)


def mk_launcher_icon_specs():
    sizes = [48, 96, 192, 512]
    icons = []
    for size in sizes:
        icons.append({
            'src': 'launcher-icons-{}.png'.format(size),
            'type': 'image/png',
            'sizes': '{}x{}'.format(size, size)
        })
    return icons


def mk_launcher_icons(spec):
    icons = mk_launcher_icon_specs()
    src_icon = os.path.join(spec.src_dir, 'logo.png')
    for icon in icons:
        dest_icon = pathlib.Path(spec.dest_dir) / icon['src']
        if not dest_icon.is_file():
            shutil.copyfile(src_icon, str(dest_icon))
    return icons


def mk_manifest_file(spec):
    icons = mk_launcher_icons(spec)
    data = {
            'background_color': 'white',
            'theme_color': 'black',
            'display': 'standalone',
            'name': spec.name,
            'short_name': spec.name,
            'icons': icons,
            'start_url': '/'
    }
    manifest_file = os.path.join(spec.dest_dir, 'manifest.json')
    f = open(manifest_file, 'w')
    json.dump(data, f)
    f.close()


def mk_favicon(spec):
    src_favicon = os.path.join(spec.src_dir, 'logo.png')
    dest_favicon = pathlib.Path(spec.dest_dir) / 'favicon.png'
    if not dest_favicon.is_file():
        shutil.copyfile(src_favicon, str(dest_favicon))


def build_pdf(spec):
    pdf_dest_dir = os.path.join(spec.dest_dir, 'pdf')
    latex_name = spec.name.replace(' ', '\_')
    project_name = spec.name.replace(' ', '_')
    pdf_file_name = '{}.pdf'.format(project_name)
    cmd = [
            'sphinx-build', '-b', 'latex',
            '-c', str(conf_dir),
            '-D', 'project={}'.format(latex_name),
            '-D', 'version={}'.format(spec.version),
            # '-D', 'latex_elements.release={}'.format(config['version']),
            spec.src_dir, pdf_dest_dir
    ]
    if spec.force:
        cmd.append('-a')
    subprocess.call(cmd)
    subprocess.call(['make', '-C', pdf_dest_dir])

    return os.path.join('pdf', pdf_file_name)


def build_text(spec):
    project_name = spec.name.replace(' ', '_')
    text_file_name = '{}.txt.tar.gz'.format(project_name)
    dest_dir = pathlib.Path(spec.dest_dir) / 'text'
    dest_file = dest_dir / text_file_name
    if not dest_dir.is_dir():
        dest_dir.mkdir(0o777, True)
    cmd = ['tar', '-zcf', str(dest_file),  spec.src_dir]
    subprocess.Popen(cmd)
    return os.path.join('text', text_file_name)


def build_doc(src, dest, dist=False, no_pdf=False, no_html=False,
              no_text=False, force=False):
    spec = mk_build_spec(src, dest, force)
    real_dest_dir = spec.dest_dir
    pdf_file = None
    text_file = None

    if dist:
        spec.dest_dir = os.path.join(real_dest_dir, '_tmp')
    if not no_pdf:
        pdf_file = build_pdf(spec)
    if not no_text:
        text_file = build_text(spec)
    if not no_html:
        build_html(spec, pdf_file, text_file)

    if dist:
        optimize_build_files(spec.dest_dir, real_dest_dir)


def compress_html(src, dest):
    f = open(str(src))
    d = f.read()
    f.close()
    c = htmlmin.minify(d, remove_comments=True, remove_empty_space=True)

    if not dest.parent.is_dir():
        dest.parent.mkdir(0o777, True)
    f = open(str(dest), 'w')
    f.write(c)
    f.close()
    print('minified html: {}'.format(dest))


def copy_file(src, dest):
    dest_dir = dest.parent
    if not dest_dir.is_dir():
        dest_dir.mkdir(0o777, True)
    shutil.copyfile(str(src), str(dest))


def compress_js(src, dest):
    f = open(str(src))
    d = f.read()
    f.close()

    if not dest.parent.is_dir():
        dest.parent.mkdir(0o777, True)
    c = jsmin.jsmin(d)
    f = open(str(dest), 'w')
    f.write(c)
    f.close()
    print('minified js: {}'.format(dest))


def compress_handle(src, dest):
    if src.suffix == '.html':
        compress_html(src, dest)
    elif src.suffix == '.css':
        compress_css(src, dest)
    elif src.suffix == '.js':
        compress_js(src, dest)
    else:
        copy_file(src, dest)


def compress_css(src, dest):
    f = open(str(src))
    d = f.read()
    f.close()

    if not dest.parent.is_dir():
        dest.parent.mkdir(0o777, True)

    c = csscompressor.compress(d)
    f = open(str(dest), 'w')
    f.write(c)
    f.close()
    print('minified css: {}'.format(dest))


image_extensions = ['.png', '.jpeg', '.jpg']


def optimize_image_file(src_file, dest_file):
    if not dest_file.parent.is_dir():
        dest_file.parent.mkdir()
    img = Image.open(src_file)
    width, height = img.size
    if width > 900:
        new_width = 900
        new_height = height * new_width / width
        img = img.resize((new_width, new_height), Image.LANCZOS)
    img.save(dest_file, quality=95)
    print('minified image: {}'.format(dest_file))


def optimize_image_files(src_dir, dest_dir):
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            src_file = Path(os.path.join(root, file))
            src_dir_rel = src_file.relative_to(src_dir)
            dest_file = Path(dest_dir) / src_dir_rel
            if src_file.suffix in image_extensions:
                optimize_image_file(src_file, dest_file)
            else:
                copy_file(src_file, dest_file)


def optimize_build_files(src_dir, dest_dir):
    image_src_dir = os.path.join(src_dir, '_images')

    for root, dirs, files in os.walk(src_dir):
        if root == image_src_dir:
            continue
        for file in files:
            src_file = pathlib.Path(os.path.join(root, file))
            src_dir_rel = src_file.relative_to(src_dir)
            dest_file = pathlib.Path(dest_dir) / src_dir_rel
            compress_handle(src_file, dest_file)

    image_dest_dir = os.path.join(dest_dir, '_images')
    optimize_image_files(image_src_dir, image_dest_dir)
