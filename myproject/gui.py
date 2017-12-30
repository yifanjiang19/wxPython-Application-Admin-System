import wx

class AdminFrame(wx.Frame):
    """
    admin window
    """
    def __init__(self, parent, id, title, size):
        wx.Frame.__init__(self, parent, id, title)
        self.SetSize(size)
        self.Center()
        
        panel = wx.Panel(self, -1)
        panel.Bind(wx.EVT_MOTION, self.OnMove) 
        wx.StaticText(panel, -1, "Pos:", pos=(10, 12))
        self.posCtrl = wx.TextCtrl(panel, -1, "", pos=(40, 10))
        self.testframe = wx.TextCtrl(self, pos=(5, 100), size=(200, 100), style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.Show()
    def OnMove(self, event):
        pos = event.GetPosition() 
        self.posCtrl.SetValue("%s, %s" % (pos.x, pos.y))

def launch():
    app = wx.App()
    admin = AdminFrame(None, -1, title="Login", size=(320, 250))  
    return app, admin   