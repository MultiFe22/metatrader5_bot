# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
from datetime import datetime
import time

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import MetaTrader5 as mt5

if not mt5.initialize():
    print("fail do init")
    mt5.shutdown()
    
stocks = mt5.symbols_get()

def get_data(stock,timeframe, n=5):
    val = mt5.copy_rates_from_pos(stock, timeframe, 0 , 5)
    val = pd.DataFrame(val)
    val['time'] = pd.to_datetime(val['time'], unit= 's')
    val.set_index('time', inplace=True)
    return val

#print(get_data('USDJPY', mt5.TIMEFRAME_M1))

#plt.style.use('fivethirtyeight')
fig, ax = plt.subplots()
graph1, = ax.plot([],[], label = 'USDJPY')
ax.set_title('Classes')
ax.set_xlabel('time')
ax.set_ylabel('price')
w = 0
correction = 0
x = []
y = []
def animate(i):
    global w
    global correction
    global x,y
    
    data = mt5.symbol_info_tick('USDJPY')

    x.append(float (data[0]))
    if  w == 0:
        correction = x[len(x)-1]
        w += 1
    x[len(x)-1] -= correction
    print(x[len(x)-1])
    y.append(float(data[1]))
    print(y[len(x)-1])
    graph1.set_data(x,y)
    
    """ xlim_low, xlim_high = ax.get_xlim()
    ylim_low, ylim_high = ax.get_ylim()
    
    ax.set_xlim(xlim_low, (xlim_high + 5))
    
    ax.set_ylim((ylim_low - 5), (xlim_high + 5)) """
    
    

ani = FuncAnimation(fig, animate, interval = 200)

ax.legend()
plt.tight_layout()
plt.show()