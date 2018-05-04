Create new document
===================

.. code-block:: bash

        fx doc src dest

`src` is directory contains source files of documents.

.. code-block:: text

        src
         |
         |-index.rst
         |-chapter-2.rst
         |-chapter-1.rst
         |-...
         |

`index.rst` is root file document, follow reStructureText format.

`dest` is destination directory will be store results.

.. code-block:: text

        dest
         |
         |-index.html
         |-pdf/index.pdf
         |-...
         |

`index.html` is file to start with document. `pdf/index.pdf` is PDF document.

.. table:: Shortcuts keys

        =============== ======================================================
        Key             Description
        =============== ======================================================
        ESC             Change to NORMAL mode
        BACKQUOTE       Change to SEARCH mode
        n               Go to next section
        p               Go to previous section
        t               Go to table of contents
        =============== ======================================================
