
import wx
import os

class FileFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="TXT Editor", size=(1000, 666))
        self.bkg = wx.Panel(self)
        

        self.openBtn = wx.Button(self.bkg, label='浏览')
        self.openBtn.Bind(wx.EVT_BUTTON, self.openFile)

        self.saveBtn = wx.Button(self.bkg, label='保存')
        self.saveBtn.Bind(wx.EVT_BUTTON, self.saveFile)

        self.filename = wx.TextCtrl(self.bkg, style=wx.TE_READONLY)
        self.contents = wx.TextCtrl(self.bkg, style=wx.TE_MULTILINE)

        self.hbox = wx.BoxSizer()
        self.hbox.Add(self.openBtn, proportion=0, flag=wx.LEFT | wx.ALL, border=5)
        self.hbox.Add(self.filename, proportion=1, flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=5)
        self.hbox.Add(self.saveBtn, proportion=0, flag=wx.LEFT | wx.ALL, border=5)

        self.bbox = wx.BoxSizer(wx.VERTICAL)
        self.bbox.Add(self.hbox, proportion=0, flag=wx.EXPAND | wx.ALL)
        self.bbox.Add(self.contents, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=5)
        self.bkg.SetSizer(self.bbox)
        # self.openFile(wx.EVT_BUTTON)


    def openFile(self, evt):
        dlg = wx.FileDialog(
            self,
            "Open",
            "",
            "",
            "All files (*.*)|*.*",
            wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        filepath = ''
        if dlg.ShowModal() == wx.ID_OK:
            filepath = dlg.GetPath()
        else:
            return
        filepath = "/Users/yifan/Desktop/SoftwareProject/myproject/1.txt"
        self.filename.SetValue(filepath)
        fopen = open(filepath)
        fcontent = fopen.read()
        self.contents.SetValue(fcontent)
        fopen.close()

    def saveFile(self, evt):

        fcontent = self.contents.GetValue()
        fopen = open(self.filename.GetValue(), 'w')
        fopen.write(fcontent)
        fopen.close()
        win = wx.Frame(None, title='TXT Editor')
        button = wx.Button(win, label='保存成功')
        win.Show()