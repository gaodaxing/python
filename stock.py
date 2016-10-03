# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 09:25:46 2016

@author: daxinggao
"""

import ystockquote
from pprint import pprint
import sys
from numpy import *
import matplotlib.pyplot as plt
import datetime

#print name,':', ystockquote.get_price(name)
#pprint(ystockquote.get_historical_prices('GOOG', '2013-01-03', '2013-01-08'
#))
#print ystockquote.get_historical_prices('GOOG', '2013-01-03', '2013-01-08')
#['2013-01-04']['Open']
#pprint(ystockquote.get_all(name))
#ystockquote.urlopen('http://www.google.com/finance/getprices?i=60&p=10d&f=d,o,h,l,c,v&df=cpct&q=IBM')
#print ystockquote.get_bid_realtime('GOOG')

class bcolors:
    Red = '\033[91m'
    Green = '\033[92m'
    Blue = '\033[94m'
    Cyan = '\033[96m'
    White = '\033[97m'
    Yellow = '\033[93m'
    Magenta = '\033[95m'
    Grey = '\033[90m'
    Black = '\033[90m'
    Bold = '\033[1m'
    Underline = '\033[4m'
    Default = '\033[99m'
    ENDC = '\033[0m'
    def disable(self):
        self.Red = ''
        self.Green = ''
        self.Blue = ''
        self.Cyan = ''
        self.White = ''
        self.Yellow = ''
        self.Magenta = ''
        self.Grey = ''
        self.Black = ''
        self.Bold = ''
        self.Underline = ''
        self.Default = ''
        self.ENDC = ''

def plot_price(name):
    f,axs = plt.subplots(4,1, figsize=(8,10))
    url = 'http://chartapi.finance.yahoo.com/instrument/1.0/'+name+'/chartdata;type=quote;range=1d/csv'
    req = ystockquote.Request(url)
    resp = ystockquote.urlopen(url)
    content = resp.read().split('\n')[:-1]
    for n in range(len(content)):
        if content[n].find('previous_close')==0:
            previous_close = float(content[n].replace('previous_close:',''))
        if content[n].find(':')==-1:
            break
    content = content[n:]
    timestamp,close,high,low,open1,volume = array([tmp.split(',') for tmp in content],dtype=float).T

    url = 'http://finance.yahoo.com/d/quotes.csv?s='+name+'&f=aba5b6'
    req = ystockquote.Request(url)
    resp = ystockquote.urlopen(url)
    content = resp.read().split('\n')[0].split(',')
    ask,bid,askSize,bidSize = content

# 1 day
    datime = [datetime.datetime.fromtimestamp(tmp) for tmp in timestamp]
    axs[0].plot(datime,open1)
    axs[0].plot([datime[0],datime[0]+datetime.timedelta(0,23400)],previous_close*ones(2),':')
    
    axs[0].grid('on')
    axs[0].set_xlim(datime[0],datime[0]+datetime.timedelta(0,23400))

# duo days
    for n,N in enumerate([30,365,1826]):
        datime = [datetime.datetime.now()+datetime.timedelta(days=i) for i in range(-N,1)]

        quote = ystockquote.get_historical_prices(name, datime[0].strftime('%Y-%m-%d'), datime[-1].strftime('%Y-%m-%d'))

        datime = sorted([datetime.datetime.strptime(tmp,'%Y-%m-%d') for tmp 
        in quote.keys()])
        quote = [quote[tmp]['Adj Close'] for tmp in sorted(quote)]
        axs[n+1].plot(datime,quote)
        axs[n+1].grid('on')
    for ax in axs:
        plt.setp( ax.xaxis.get_majorticklabels(), rotation=12)

    plt.subplots_adjust(left=0.06, bottom=0.05, right=0.95, top=0.98, wspace=0.05, hspace=0.3)

    f.canvas.set_window_title(name)

# bid
    axs[0].text(0.95, 0.95, 'bid: ' +bid+'x'+bidSize+'   '+'ask: '+ask+'x'+askSize,verticalalignment='top', horizontalalignment='right',transform=axs[0].transAxes, fontsize=15)

        
        
    axs[0].text(0.70, 0.80, str(close[-1]),
        verticalalignment='top', horizontalalignment='right', color='b',
        transform=axs[0].transAxes, fontsize=15)
    color = 'r'*int(close[-1]<previous_close)+'g'*int(close[-1]>previous_close)+'0.5'*int(close[-1]==previous_close)

    axs[0].text(0.95, 0.80, '%+-.2f'%(close[-1]-previous_close)+'  %+-.2f'%(
    float(close[-1]-previous_close)/float(previous_close)*100)+'%',
        verticalalignment='top', horizontalalignment='right', color=color,
        transform=axs[0].transAxes, fontsize=15)

# stuff
    all1 = ystockquote.get_all(name)
    print bcolors.Bold+name+' '+bcolors.Blue+str(close[-1])+bcolors.ENDC
    if float(all1['change'])>0:
        print bcolors.Green+all1['change']+' +'+'%.2f'%(float(close[-1]-
        previous_close)/float(all1['price'])*100)+'%'+bcolors.ENDC
    else:
        print bcolors.Red+all1['change']+' '+'%.2f'%(float(close[-1]-
        previous_close)/float(all1['price'])*100)+'%'+bcolors.ENDC
    print '---------------------'
#    pprint(all1)
    return close[-1]

if __name__=='__main__':
    print sys.argv
    if len(sys.argv)<=1:
        sys.argv = ['','spy','atvi','tsla','goog']
    print '---------------------'
    for name in sys.argv[1:]:
        close = plot_price(name)
    if len(sys.argv[0])>1:
        plt.show()
    