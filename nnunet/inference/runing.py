import wx.xrc
import wx, os
import matplotlib
matplotlib.use('TkAgg')
import wx.xrc


class ControlPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, size=wx.Size(500, 100))

        topSizer = wx.FlexGridSizer(1, 1, 0, 0)
        topSizer.SetFlexibleDirection(wx.BOTH)
        topSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        sizer1 = wx.FlexGridSizer(0, 3, 0, 0)
        sizer1.SetFlexibleDirection(wx.BOTH)
        sizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.openfile = wx.Button(self, wx.ID_ANY, u"runing", wx.DefaultPosition, wx.DefaultSize, 0)
        sizer1.Add(self.openfile, 0, wx.ALL, 1)

        self.patientdir = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(200, -1), 0)
        sizer1.Add(self.patientdir, 0, wx.ALL, 1)

        self.openfile1 = wx.Button(self, wx.ID_ANY, u"show", wx.DefaultPosition, wx.DefaultSize, 0)
        sizer1.Add(self.openfile1, 0, wx.ALL, 1)
        topSizer.Add(sizer1, 1, wx.EXPAND, 1)

        self.openfile.Bind(wx.EVT_BUTTON, self.readpwd)
        self.openfile1.Bind(wx.EVT_BUTTON, self.preslic)
        self.SetSizer(topSizer)
        self.Layout()

    def readpwd(self, event):
        # FileDialog只能打开各类文件，而Dirdialog只能打开文件夹。
        os.system('python predict_simple.py')


    def preslic(self, event):
        os.system('python Show3D.py')

class Frame3D(wx.Frame):
    frms = {}

    def __init__(self, parent, title='Frame3D'):
        wx.Frame.__init__(self, parent,
                          id=wx.ID_ANY,
                          title=title,
                          pos=wx.DefaultPosition,
                          size=wx.Size(500, 100),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.viewer = ControlPanel(self)
        # 新建一个3D显示盒子
        sizer.Add(self.viewer, 1, wx.EXPAND, 1)

        # 显示盒子
        self.SetSizer(vbox)
        self.Layout()
        self.Centre(wx.BOTH)


if __name__ == '__main__':
    app = wx.App(False)
    frm = Frame3D(None, title='GLCanvas Sample')
    frm.Show()
    app.MainLoop()