# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 11:22:19 2016

@author: daxinggao
"""

import wx

class frame(wx.Frame):
    def __init__(self,parent=None,id=-1):
        wx.Frame.__init__(self,parent,id,"I am title",size=(500,400))
        self.panel=wx.Panel(self,-1)
        button=wx.Button(self.panel,-1,"Exit",pos=(100,100),size=(100,100))
        self.Bind(wx.EVT_BUTTON,self.closebutton,button)
        tx=wx.StaticText(self.panel,-1,"Hello,python!",(40,30),(400,-1),style=wx.ALIGN_CENTER_HORIZONTAL)
        tx.SetForegroundColour("Green")
        tx.SetBackgroundColour("Blue")
        box=wx.MessageDialog(None,"Do you want cookie?","question",wx.YES_NO)
        box.ShowModal()
        box.Destroy()
        box2=wx.TextEntryDialog(None,"What's your name?","question","Daxing")
        box2.ShowModal()
        box2.Destroy()
        box3=wx.SingleChoiceDialog(None,"What's your name?","question",["Daxing","kiki","Gao"])
        box3.ShowModal()
        box3.Destroy()
        s=self.CreateStatusBar()
        menubar=wx.MenuBar()
        first=wx.Menu()
        second=wx.Menu()
        first.Append(wx.NewId(),"New","Create a file")
        first.Append(wx.NewId(),"Open","Open a file")
        second.Append(wx.NewId(),"Copy","copy a file")
        second.Append(wx.NewId(),"paste","paste a copy")
        menubar.Append(first,"file")
        menubar.Append(second,"edit")
        self.SetMenuBar(menubar)
        self.panel.Bind(wx.EVT_LEFT_UP,self.clickleft)
        button2=wx.Button(self.panel,-1,"Add text",pos=(300,100),size=(100,100))
        self.text1=wx.TextCtrl(self.panel,-1,"Hello",size=(200,60))
        self.Bind(wx.EVT_BUTTON,self.click2,button2)
        
        
    def closebutton(self,event):
        self.Close(True)
    def clickleft(self,event):
        posi=event.GetPosition()
        wx.StaticText(self.panel,label="I am new",pos=(posi.x,posi.y))
    def click2(self,event):
        self.text1.AppendText("\nok!")
        



if __name__=="__main__":
    app=wx.App()
    frame1=frame()
    frame1.Show()
    app.MainLoop()