nb-code-formatter
=================

code formatter for ipynb files.

this tool uses `Black <https://github.com/psf/black>`_ for formatting code and `isort <https://github.com/PyCQA/isort>`_ for sorting imports.

Quick Start
-----------

Install the package
^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    pip install nb-code-formatter

format code your ipynb file
^^^^^^^^^^^^^^^^^^^^^^^^^^^

overwrite existing notebook file

.. code-block:: bash

    nbcodefmt your_notebook.ipynb

write to new notebook file

.. code-block:: bash

    nbcodefmt your_notebook.ipynb new_notebook.ipynb
