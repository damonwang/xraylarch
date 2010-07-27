import wx
import MPlot
from WxUtil import *
from VarSelPanel import VarSelPanel
from DataSheet import DataSheet

class Data2DSheet(DataSheet):

    def mkCtrls(self):
        '''creates the controls.

        put them into your own sizer and put that one object into self.sizer

        put a list of controls into self.ctrls

        put the control which picks the plotting destination into self.plotctrl
        
        '''

        self.ctrlsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.PrependF(item=self.ctrlsizer, flags=wx.SizerFlags())

        self.ctrls = dict( 
            Data=VarSelPanel(parent=self, var="Data", sizer=self.ctrlsizer,
                options=self.getDataNames(), defchoice=-1),
            Plot=VarSelPanel(parent=self, var="Plot", sizer=self.ctrlsizer,
                options=[], defchoicelabel="in"))

        self.plotctrl = self.ctrls["Plot"] 
        self.updatePlotCtrl()

        self.plotbtn = createButton(parent=self, label="Plot", 
            handler=self.onPlot, sizer=self.ctrlsizer)

    def mkPanelPlot(self):
        '''creates the initial panel plot, before user can choose anything.

        assign the plot into self.plotpanel
        add it into self.sizer
        '''
        print(" mkPanelPlot ")
        self.plotpanel = MPlot.ImagePanel(parent=self)
        self.plotpanel.SetMinSize((400,300))
        self.plotpanel.SetSize(self.plotpanel.GetMinSize())
        self.sizer.AddF(item=self.plotpanel, 
                flags=wx.SizerFlags(1).Expand().Center().Border())

    def mkNewFrame(self, name="New Frame"):
        rv = MPlot.ImageFrame(parent=self, name=name)
        self.plotframes.append(rv)
        rv.Bind(event=wx.EVT_CLOSE, handler=self.onPlotFrameClose)
        rv.Show()
        self.updatePlotCtrl()
        return rv

    
    def plot(self, dataSrc, dest):
        '''plots the named data to destination

        Args:
            dataSrc: name suitable for putting into getData
            dest: something with a plot or display method
        '''

        self.writeOut("Plotting %s" % dataSrc)
        data = self.getData(name=self.getPlotName())
        dest.display(data)
        dest.redraw()

    def getDataChoice(self):
        '''returns something that can be passed as dataSrc argument to plot'''

        return self.getCtrls("Data")

    def getPlotName(self, data=None):
        '''returns a string following this plot's naming convention.

        Args:
            (optional) data: given the name, formats it
            If none given, queries the controls

        Returns:
            "Plot %{data}s"
        '''

        if data is None:
            return "Plot %s" % self.getCtrls("Data")
        else:
            return "Plot %s" % data

    def getDataNames(self):
        raise NotImplementedError("getDataNames")

    def getData(self, name):
        raise NotImplementedError("getData")

