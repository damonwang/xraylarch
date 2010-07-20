#!/usr/bin/env python

'''a clone of data viewer by Matt Newville, as a wxPython learning project by Damon Wang. 22 June 2010 '''

#------------------------------------------------------------------------------
# IMPORTS

from __future__ import print_function

import wx
import os
import sys
from multiprocessing import Process, Pipe

from App import App
from MainFrame import MainFrame

def main(pipe=None):
    '''starts graphical app, does not return until app closes'''

    app = App(redirect=False)
    if pipe is not None:
        pipe.send(app)
        pipe.close()
    app.MainLoop()

def start_main():
    '''DOES NOT WORK
    
    starts graphical app in separate process.

    Returns (app, process): 
        app: the wx.App object
        process: the multiprocessing.Process object, which caller should join()
    '''

    pipe, child_pipe = Pipe()
    p = Process(target=main, args=(child_pipe,))
    p.start()
    app = pipe.recv()

    return app, p

def newplot():
    '''if a wx App is already running, use this to get a MainFrame without
    firing up another App.

    Returns:
        a dataviewer.MainFrame.MainFrame instance
    '''

    mf = MainFrame(parent=None, id=-1, title='Data Viewer Clone')
    mf.Show()

    return mf
