import wx
import matplotlib.cm 
class ImageConfig:
    def __init__(self):
        self.conf  = None
    def relabel(self):
        " re draw labels (title, x,y labels)"
        print 'relabel! '

class ImageGUIConfig(wx.Frame):
    def __init__(self,config=None,cmap=None,interp=None,**kw):
        self.conf  = config
    
        self.cmap   = cmap or matplotlib.cm.jet
        self.interp = interp or 'bilinear'
