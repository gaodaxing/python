# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 10:36:36 2016

@author: daxinggao
"""
import sqlite3
import wx
from matplotlib.finance import fetch_historical_yahoo as fhis
import pandas as pd


class frame(wx.Frame):
    def __init__(self,parent=None,id=-1):
        wx.Frame.__init__(self,parent,id,"SQL",size=(1000,800))
        self.panel=wx.Panel(self)
        button1=wx.Button(self.panel,-1,"Create SQL",pos=(10,10),size=(100,50))
        self.Bind(wx.EVT_BUTTON,self.clickb1,button1)
        button2=wx.Button(self.panel,-1,"Exit",pos=(800,10),size=(100,50))
        self.Bind(wx.EVT_BUTTON,self.clickb2,button2)
        Tx1=wx.TextEntryDialog(None,"Enter the Stock symbol","Stock","SKX")
        if Tx1.ShowModal()==wx.ID_OK:
            self.stock=Tx1.GetValue()
        else: self.stock="SKX"
        button3=wx.Button(self.panel,-1,"Stock "+self.stock,pos=(300,10),size=(100,50))
        self.Bind(wx.EVT_BUTTON,self.clickb3,button3)
        self.start=wx.DatePickerCtrl(self.panel,-1,style=wx.DP_DROPDOWN,pos=(200,100))
        self.end=wx.DatePickerCtrl(self.panel,-1,style=wx.DP_DROPDOWN,pos=(300,100))
        print self.start.GetValue()
        
    def clickb1(self,event):
        conn=sqlite3.connect("file.db")
        cur=conn.cursor()
        cur.execute('''CREATE TABLE if not EXISTS SQL(id INT PRIMARY KEY NOT NULL,
        NAME TEXT,
        URL TEXT) ''')
        conn.commit()
        cur.close()
        conn.close()
        
    def clickb2(self,event):
        self.Destroy()
        
    def _wxdate2pydate(another,date):
        import datetime
        if date.IsValid():
            ymd=map(int,date.FormatISODate().split('-'))
            return datetime.date(*ymd)
        else:return None
    
    def clickb3(self,event):
        import matplotlib.pyplot as plt 
        
        start=self._wxdate2pydate(self.start.GetValue())
        end=self._wxdate2pydate(self.end.GetValue())
        stk=fhis(self.stock,start,end)
        list1=[]
        flag=0
        for line in stk:
            if flag==0:colnames=line.rstrip().split(",");flag=1
            else: list1.append(line.rstrip().split(","))
        df=pd.DataFrame(list1,columns=colnames)
        df['Date']=pd.to_datetime(df['Date'],format="%Y-%m-%d")
        df['Open']=pd.to_numeric(df['Open'])
        df['Close']=pd.to_numeric(df['Close'])
        df['High']=pd.to_numeric(df['High'])
        df['Low']=pd.to_numeric(df['Low'])
        df['Adj Close']=pd.to_numeric(df['Adj Close'])
        print df
        plt.plot(df['Date'],df['High'],"r-")
        plt.plot(df['Date'],df['Low'],"b-")
        plt.plot(df['Date'],df['Open'],"go")
        plt.plot(df['Date'],df['Close'],"yo")
        plt.show()
        
if __name__=="__main__":
    app=wx.App()
    frame1=frame()
    frame1.Show()
    app.MainLoop()
        
