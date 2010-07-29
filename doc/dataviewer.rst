==================
    Dataviewer
==================

This document freely mixes implemented and planned features. It's closer to a
roadmap than an actual help page at the moment. 

------------------
    How to use
------------------

1. Make sure PYTHONPATH includes the larch modules directory::

       PYTHONPATH=...;P:\xraylarch\larch\modules;...

2. import the module::

       import dataviewer

3. create a new MainFrame using func:`dataviewer.start`::

       mf = dataviewer.start(r"P:\dataviewer\test\diamond_line.002")

   Note that the ``r"`` is necessary on Windows to prevent the directory
   separator from being misinterpreted as an escape.

   If no arguments are provided, a blank MainFrame opens. 

   Each DataSheet becomes an attribute of the MainFrame instance, e.g.::

        mf.diamond_line_002

   The attribute name is the filename, with underscores substituted in to make
   it a legal Python identifier. This tends to result in long attribute names,
   but fortunately there will be tab-completion.

4. 
