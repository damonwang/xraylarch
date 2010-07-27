import sys 

import wx
import MPlot
from WxUtil import *
from VarSelPanel import VarSelPanel
from DataSheet import DataSheet

class Data1DSheet(DataSheet):

    def onOverPlot(self, event):
        '''adds a trace to the existing plot'''

        self.onPlot(event, overplot=True)

    def plot(self, dataSrc=None, dest=None, x=None, y=None, **kwargs):
        '''plots the named data to destination

        Args:
            dataSrc: dict { var : name }, name suitable for passing to getData
            dest: something with a plot method
        '''
    
        if dest is None:
            dest = self.plotpanel

        try:
            if x is None:
                x = self.getXData(name=dataSrc["X"])
            if y is None:
                y = self.getYData(name=dataSrc["Y"])
        except (TypeError, KeyError):
            print >> sys.stderr, "must either provide the data via x, y arguments, or else name the sources via dataSrc argument."

        if kwargs.get("overplot", False):
            try:
                dest.oplot(x, y)
            except AttributeError:
                self.plot(dataSrc, dest, overplot=False)
        else:
            dest.plot(x, y)

    def getDataChoice(self):
        '''returns something that can be passed as dataSrc argument to plot'''

        return self.getCtrls("X", "Y")

    def mkCtrls(self):
        '''creates the controls.

        put them into your own sizer and put that one object into self.sizer

        put a dict { var : ctrl } of controls into self.ctrls

        put the control which picks the plotting destination into self.plotctrl
        
        '''

        self.ctrlsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.PrependF(item=self.ctrlsizer, flags=wx.SizerFlags())

        self.ctrls = dict( 
            X=VarSelPanel(parent=self, var="X", sizer=self.ctrlsizer,
                options=self.getXDataNames(), defchoice=-1),
            Y=VarSelPanel(parent=self, var="Y", sizer=self.ctrlsizer,
                options=self.getYDataNames(), defchoice=-1),
            Plot=VarSelPanel(parent=self, var="Plot", sizer=self.ctrlsizer,
                options=[], defchoicelabel="in"))

        self.plotctrl = self.ctrls["Plot"] 
        self.updatePlotCtrl()

        self.plotbtn = createButton(parent=self, label="Plot", 
            handler=self.onPlot, sizer=self.ctrlsizer)
        self.oplotbtn = createButton(parent=self, label="Overplot",
            handler=self.onOverPlot, sizer=self.ctrlsizer)

    def mkPanelPlot(self):
        '''creates the initial panel plot, before user can choose anything.

        assign the plot into self.plotpanel
        add it into self.sizer
        '''

        self.plotpanel = MPlot.PlotPanel(parent=self)
        self.plotpanel.SetMinSize((400,300))
        self.plotpanel.SetSize(self.plotpanel.GetMinSize())
        self.sizer.AddF(item=self.plotpanel, 
                flags=wx.SizerFlags(1).Expand().Center().Border())

    def mkNewFrame(self, name="New Frame"):
        rv = MPlot.PlotFrame(parent=self, name=name)
        self.plotframes.append(rv)
        rv.Bind(event=wx.EVT_CLOSE, handler=self.onPlotFrameClose)
        rv.Show()
        self.updatePlotCtrl()
        return rv

    def getPlotName(self, x=None, y=None):
        '''returns a string following this plot's naming convention.

        Args:
            (optional) x, y: given the axes, formats them
            If none given, queries the controls
            Note that if just one axis is passed, it is ignored and the
            controls are queried anyway

        Returns:
            "Plot %{x}s v. %{y}s"
        '''
            
        if x is None or y is None:
            srcs = self.getDataChoice()
            x, y = srcs["X"], srcs["Y"]
        return "Plot %s v. %s" % (x, y)


    def getXData(self, name):
        raise NotImplementedError("getXData")
    def getXDataNames(self):
        raise NotImplementedError("getXDataNames")
    def getYData(self, name):
        raise NotImplementedError("getYData")
    def getXDataNames(self):
        raise NotImplementedError("getYDataNames")
