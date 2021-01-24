sing
====

|pypi| |build| |Documentation Status| |Updates|

Ensure a single process is running. Using lockfile and process checking.

Why?
----

Sometime you want that a process runs at most once, for example a
scheduled cron job that should always finish before starting again. That
was my case.

Install
-------

.. code:: bash

   pip install sing

Examples
--------

Normally, at the beginning of the file, you may want to declare, that
you want to be the single instance:

.. code:: python

   from sing import single

   assert single()

That’s it, for most of the use case, you don’t need anything else. The
assert will fail if the lock is already taken.

This uses a pid lockfile, in a temporary folder to ensure this. More on
that in ``sing.py``

You may want to grant all the lock from the same process, in that case
you’ll need.

.. code:: python

   assert single(allow_all_from_this_process=True)

You may have different subsections, and you want to have different
locks, even if you’re on the same process, both of them will return
True:

.. code:: python

   single(flavor='first')
   single(flavor='second')

Finally, if a PID file is there, but the process died, you may want to
grant the lock. Use the ``ensure_process_running`` to check it.

Notes
-----

-  Free software: MIT license
-  Documentation: https://python-sing.readthedocs.io.

Credits
-------

This package was created with
`Cookiecutter <https://github.com/audreyr/cookiecutter>`__ and the
`audreyr/cookiecutter-pypackage <https://github.com/audreyr/cookiecutter-pypackage>`__
project template.

Lot of inspiration comes from
`pycontribs/tendo <https://github.com/pycontribs/tendo>`__ that serves
the same purpose. I needed PID file, and allow same process grants, so I
made this package.

.. |pypi| image:: https://img.shields.io/pypi/v/sing.svg
   :target: https://pypi.python.org/pypi/sing
.. |build| image:: https://img.shields.io/travis/dariosky/python-sing.svg
   :target: https://travis-ci.org/dariosky/python-sing
.. |Documentation Status| image:: https://readthedocs.org/projects/python-sing/badge/?version=latest
   :target: https://python-sing.readthedocs.io/en/latest/?badge=latest
.. |Updates| image:: https://pyup.io/repos/github/dariosky/python-sing/shield.svg
   :target: https://pyup.io/repos/github/dariosky/sing/
