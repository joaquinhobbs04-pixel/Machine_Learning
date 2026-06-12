import wx

class Mywin(wx.Frame):
    def __init__(self, parent, title):
        super(Mywin, self).__init__(parent, title=title,size=(600, 400))
        panel1 = wx.Panel(self)
        #垂直盒子
        vbox = wx.BoxSizer(wx.VERTICAL)
        #水平盒子
        nmbox = wx.BoxSizer(wx.HORIZONTAL)
        #创建两个静态文本
        fn = wx.StaticText(panel1, -1, label="电影名称：")
        ln = wx.StaticText(panel1, -1,label="选择片源：")
        #创建两个输入框
        self.nm1 = wx.TextCtrl(panel1, -1,size = (200,20),style=wx.ALIGN_LEFT)
        #在水平盒子里添加上面三个
        nmbox.Add(fn, 0, wx.ALL| wx.EXPAND, 5)
        nmbox.Add(self.nm1, 0, wx.ALL|wx.EXPAND, 5)
        nmbox.Add(ln, 0,  wx.ALL|wx.EXPAND, 5)
        #创建下拉框
        self.languages = ['电影天堂', '80S电影网', '1905电影网', 'BT天堂', '龙部落','电影港','人人字幕组']
        self.choice =self.languages[0]
        self.combo = wx.ComboBox(panel1, choices=self.languages,value=self.languages[0])
        #在水平盒子添加下拉框
        nmbox.Add(self.combo, 1, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)


        #创建按钮
        self.find_Button = wx.Button(panel1, label="查询")
        self.Bind(wx.EVT_BUTTON, self.Onclick, self.find_Button)
        #在水平盒子里添加查询按钮
        nmbox.AddSpacer(20)
        nmbox.Add(self.find_Button, 0, wx.ALIGN_CENTER_HORIZONTAL)
        #在垂直盒子里添加水平盒子
        vbox.Add(nmbox, 0, wx.ALL | wx.CENTER, 5)

        multiLabel = wx.StaticText(panel1, -1, "查询结果：")
        vbox.Add(multiLabel, 0, wx.ALL | wx.EXPAND, 5)

        # 创建文本域
        self.multiText = wx.TextCtrl(panel1, -1,size=(200, 200), style=wx.TE_MULTILINE)  # 创建一个文本控件
        self.multiText.SetInsertionPoint(0)  # 设置插入点
        #  在垂直盒子里添加文本域
        vbox.Add(self.multiText, 1, wx.ALL | wx.EXPAND , 5)

        panel1.SetSizer(vbox)
        self.Show()

    def Onclick(self,event):
       print(self.choice)
       self.multiText.write(self.choice+"\n")
app = wx.App()
Mywin(None, '快搜')
app.MainLoop()