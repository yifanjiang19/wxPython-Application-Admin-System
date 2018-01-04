import wx
import sys, glob, random
import data
from file import FileFrame
class DemoFrame(wx.Frame):
    def __init__(self, session):
        wx.Frame.__init__(self, None, -1,
                          "Admin System",
                          size=(700,500))
        self.list = None
        self.editable = False
        self.TextID = wx.StaticText(self, label="ID：", pos=(10, 10), size=(80, 25))
        self.userid = wx.TextCtrl(self, pos=(50, 10), size=(50, 25))
        self.TextFrequency = wx.StaticText(self, label="频率：", pos=(120, 10), size=(80, 25))
        self.frequency = wx.TextCtrl(self, -1, "1", pos=(170, 10), size=(50, 25))
        self.TextBloodPre = wx.StaticText(self, label="血压上下限：", pos=(10, 50), size=(80, 25))
        self.blood_pressure_down = wx.TextCtrl(self, -1, "100", pos=(100, 50), size=(50, 25))
        self.temp1 = wx.StaticText(self, label=" ~ ", pos=(150, 50), size=(25, 25))
        self.blood_pressure_up = wx.TextCtrl(self, -1, "180", pos=(170, 50), size=(50, 25))
        
        self.TextBreath = wx.StaticText(self, label="呼吸上下限：", pos=(10, 80), size=(80, 25))
        self.breath_down = wx.TextCtrl(self, -1, "100", pos=(100, 80), size=(50, 25))
        self.temp2 = wx.StaticText(self, label=" ~ ", pos=(150, 80), size=(25, 25))
        self.breath_up = wx.TextCtrl(self, -1, "180", pos=(170, 80), size=(50, 25))

        self.TextTemper = wx.StaticText(self, label="体温上下限：", pos=(10, 110), size=(80, 25))
        self.temper_down = wx.TextCtrl(self, -1, "100", pos=(100, 110), size=(50, 25))
        self.temp3 = wx.StaticText(self, label=" ~ ", pos=(150, 110), size=(25, 25))
        self.temper_up = wx.TextCtrl(self, -1, "180", pos=(170, 110), size=(50, 25))
        
        self.sendButton = wx.Button(self, label='send', pos=(230, 10), size=(50, 25))
        self.sendButton.Bind(wx.EVT_BUTTON, session.change_frequency)

        self.openButton = wx.Button(self, label='打开日志', pos=(330, 10), size=(100, 25))
        self.openButton.Bind(wx.EVT_BUTTON, self.openfile)

        self.MakeMenu()
        self.MakeListCtrl()

    def openfile(self, evt):
        print(123)
        files = FileFrame()
        files.Show()

    def MakeListCtrl(self, otherflags=0):
        # if we already have a listctrl then get rid of it
        if self.list:
            self.list.Destroy()

        if self.editable:
            otherflags |= wx.LC_EDIT_LABELS
            
        # load some images into an image list
        il = wx.ImageList(16,16, True)
        for name in glob.glob("/Users/yifan/Desktop/SoftwareProject/myproject/Chapter/"+"smicon??.png"):
            bmp = wx.Bitmap(name, wx.BITMAP_TYPE_PNG)
            il_max = il.Add(bmp)

        # create the list control
        self.list = wx.ListCtrl(self, -1, pos=(0,150), size=(800,800), style=wx.LC_REPORT|otherflags)

        # assign the image list to it
        self.list.AssignImageList(il, wx.IMAGE_LIST_SMALL)

        # Add some columns
        for col, text in enumerate(data.columns):
            # print(col,text)
            self.list.InsertColumn(col, text)

        # add the rows
        # for row, item in enumerate(data.rows):
        #     index = self.list.InsertStringItem(666666666, item[0])
        #     for col, text in enumerate(item[1:]):
        #         # print(col,text)
        #         self.list.SetStringItem(index, col+1, text)

        #     # give each item a random image
        #     img = random.randint(0, il_max)
        #     self.list.SetItemImage(index, img, img)

        #     # set the data value for each item to be its position in
        #     # the data list
        #     self.list.SetItemData(index, row)
            
                
        # set the width of the columns in various ways
        self.list.SetColumnWidth(0, 120)
        self.list.SetColumnWidth(1, 120)
        self.list.SetColumnWidth(2, 120)
        self.list.SetColumnWidth(3, 120)
        self.list.SetColumnWidth(4, wx.LIST_AUTOSIZE_USEHEADER)

        # bind some interesting events
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.list)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected, self.list)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated, self.list)

        # in case we are recreating the list tickle the frame a bit so
        # it will redo the layout
        self.SendSizeEvent()
        

    def MakeMenu(self):
        mbar = wx.MenuBar()
        menu = wx.Menu()
        item = menu.Append(-1, "E&xit\tAlt-X")
        self.Bind(wx.EVT_MENU, self.OnExit, item)
        mbar.Append(menu, "&File")

        menu = wx.Menu()
        item = menu.Append(-1, "Sort ascending")
        self.Bind(wx.EVT_MENU, self.OnSortAscending, item)
        item = menu.Append(-1, "Sort descending")
        self.Bind(wx.EVT_MENU, self.OnSortDescending, item)
        item = menu.Append(-1, "Sort by submitter")
        self.Bind(wx.EVT_MENU, self.OnSortBySubmitter, item)

        menu.AppendSeparator()
        item = menu.Append(-1, "Show selected")
        self.Bind(wx.EVT_MENU, self.OnShowSelected, item)
        item = menu.Append(-1, "Select all")
        self.Bind(wx.EVT_MENU, self.OnSelectAll, item)
        item = menu.Append(-1, "Select none")
        self.Bind(wx.EVT_MENU, self.OnSelectNone, item)

        menu.AppendSeparator()
        item = menu.Append(-1, "Set item text colour")
        self.Bind(wx.EVT_MENU, self.OnSetTextColour, item)
        item = menu.Append(-1, "Set item background colour")
        self.Bind(wx.EVT_MENU, self.OnSetBGColour, item)

        menu.AppendSeparator()
        item = menu.Append(-1, "Enable item editing", kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnEnableEditing, item)
        item = menu.Append(-1, "Edit current item")
        self.Bind(wx.EVT_MENU, self.OnEditItem, item)
        mbar.Append(menu, "&Demo")

        self.SetMenuBar(mbar)


    def AddList(self, data):
        temp = []
        for i in range(10):
            try:
                temp.append(self.list.GetItem(i,0).Text)
            except:
                pass
        if data[0] in temp:
            index = temp.index(data[0])
        else:
            index = self.list.InsertItem(666666666, data[0])
            self.list.SetItem(index, 1, data[1])
        del temp
        for col, text in enumerate(data[3:]):
            # print(index,col,text)
            self.list.SetItem(index, col+2, text)
        if int(data[2]):
            color = (196, 20, 27, 255)
            self.list.SetItemTextColour(index, color)
        else:
            color = (0, 0, 0, 255)
            self.list.SetItemTextColour(index, color)



    def OnExit(self, evt):
        self.Close()


    def OnItemSelected(self, evt):
        item = evt.GetItem()
        print ("Item selected:", item.GetText())
        
    def OnItemDeselected(self, evt):
        item = evt.GetItem()
        print ("Item deselected:", item.GetText())

    def OnItemActivated(self, evt): 
        item = evt.GetItem()
        print ("Item activated:", item.GetText())

    def OnSortAscending(self, evt):
        # recreate the listctrl with a sort style
        self.MakeListCtrl(wx.LC_SORT_ASCENDING)
        
    def OnSortDescending(self, evt):
        # recreate the listctrl with a sort style
        self.MakeListCtrl(wx.LC_SORT_DESCENDING)

    def OnSortBySubmitter(self, evt):
        def compare_func(row1, row2):
            # compare the values in the 4th col of the data
            val1 = data.rows[row1][3]
            val2 = data.rows[row2][3]
            if val1 < val2: return -1
            if val1 > val2: return 1
            return 0

        self.list.SortItems(compare_func)
        


    def OnShowSelected(self, evt):
        print ("These items are selected:")
        index = self.list.GetFirstSelected()
        if index == -1:
            print ("\tNone")
            return
        while index != -1:
            item = self.list.GetItem(index)
            print ("\t%s" % item.GetText())
            index = self.list.GetNextSelected(index)
            
    def OnSelectAll(self, evt):
        for index in range(self.list.GetItemCount()):
            self.list.Select(index, True)
    
    def OnSelectNone(self, evt):
        index = self.list.GetFirstSelected()
        while index != -1:
            self.list.Select(index, False)
            index = self.list.GetNextSelected(index)

    
    def OnSetTextColour(self, evt):
        dlg = wx.ColourDialog(self)
        if dlg.ShowModal() == wx.ID_OK:
            colour = dlg.GetColourData().GetColour()
            index = self.list.GetFirstSelected()
            while index != -1:
                self.list.SetItemTextColour(index, colour)
                index = self.list.GetNextSelected(index)
        dlg.Destroy()

    def OnSetBGColour(self, evt):
        dlg = wx.ColourDialog(self)
        if dlg.ShowModal() == wx.ID_OK:
            colour = dlg.GetColourData().GetColour()
            index = self.list.GetFirstSelected()
            while index != -1:
                self.list.SetItemBackgroundColour(index, colour)
                index = self.list.GetNextSelected(index)
        dlg.Destroy()


    def OnEnableEditing(self, evt):
        self.editable = evt.IsChecked()
        self.MakeListCtrl()
        
    def OnEditItem(self, evt):
        index = self.list.GetFirstSelected()
        if index != -1:
            self.list.EditLabel(index)
            
    
class DemoApp(wx.App):
    def OnInit(self, frame):
        # frame = DemoFrame()
        self.SetTopWindow(frame)
        print ("Program output appears here...")
        frame.Show()
        return True

def demo_launch():
    frame = DemoFrame()
    app = DemoApp(frame=frame, redirect=True)
    print ("Program output appears here...")
    return app, frame

    

# app = DemoApp(redirect=True)
# app.MainLoop()
