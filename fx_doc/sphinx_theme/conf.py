import os
from os import path
from os.path import dirname, realpath

extensions = ['sphinx.ext.coverage', 'sphinx.ext.autodoc']
source_suffix = ['.rst']
master_doc = 'index'
project = u'libfx'
copyright = u'2018, libfx'
author = u'Kevin Leptons'
version = u'0.0.0'
release = u'0.0.0'
language = None
exclude_patterns = []
pygments_style = 'sphinx'
todo_include_todos = False
highlight_language = 'python'
theme_dir = dirname(__file__)


# HTML output
html_theme = 'sphinx_libfx_theme'
html_theme_path = [theme_dir]
html_last_updated_fmt = "%Y/%m/%d %H:%M"
html_logo = os.path.join(theme_dir, 'sphinx_libfx_theme/static/img/libfx.png')
html_additional_pages = {
    'info': 'info.html',
    'help': 'help.html',
    'downloads': 'downloads.html',
    'basic_mode_links': 'basic_mode_links.html',
    'basic_mode_toc': 'basic_mode_toc.html',
}


# PDF output
libfx_logo_path_rel = 'sphinx_libfx_theme/static/img/libfx.png'
libfx_logo_path = path.join(theme_dir, libfx_logo_path_rel)
latex_elements = {
    'sphinxsetup': r'''
        InnerLinkColor={HTML}{d00a74},
        OuterLinkColor={HTML}{d00a74},
        VerbatimColor={HTML}{ffffff},
        VerbatimBorderColor={HTML}{000000},
        VerbatimHighlightColor={HTML}{000000}
    ''',
    'papersize': 'a4paper',
    'pointsize': '10pt',
    'releasename': 'version',
    'fncychap': r'''
        \usepackage[Sony]{fncychap}
    ''',
    'preamble': r'''
        \usepackage{arev}
        \usepackage[T1]{fontenc}
        \usepackage{hyperref}
        \usepackage{tabu, tabulary}
        \usepackage{xcolor}
        \usepackage{sectsty}

        \chapterfont{\color[HTML]{000000}}
        \hypersetup{bookmarksnumbered,colorlinks=true, linkcolor=black}

        \ChNameVar{\Large}
        \ChNumVar{\Large}
        \ChTitleVar{\Huge}
        \ChNameUpperCase
    ''',
    'maketitle': r'''
        \makeatletter

        \begin{titlepage}
        \begin{center}

        \textbf{\Huge\@title}

        \textbf{version \version}

        \vfill{}

        \includegraphics[width=0.5\textwidth]{''' + libfx_logo_path + r'''}

        \textbf{\@date}

        \textbf{\Large\@author}


        \end{center}
        \end{titlepage}
    '''

    # Latex figure (float) alignment
    # 'figure_align': 'htbp',
}

# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'libfx_directive', u'libfx\_directive Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'libfx_directive', u'libfx\_directive Documentation',
     author, 'libfx_directive', 'One line description of project.',
     'Miscellaneous'),
]
