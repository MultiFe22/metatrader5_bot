# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 11:42:32 2021

@author: Felipe
"""

import MetaTrader5 as mt5
import time

if not mt5.initialize():
    print("Fail to init")
    mt5.shutdown()
    
symbol = "USDJPY"
symbol_info = mt5.symbol_info(symbol)

if symbol_info is None:
    print(symbol, "Not found")
    mt5.shutdown()
    quit()

if not symbol_info.visible:
    print(symbol, "not visible")
    if not mt5.symbol_select(symbol,True):
        print("symbol_select({}}) failed, exit",symbol)
        mt5.shutdown()
        quit()
        
def open_trade(action, symbol, lot, sl, tp, deviation):
    
    if action == 'buy':
        trade_type = mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(symbol).ask
    
    elif action == 'sell':
        trade_type = mt5.ORDER_TYPE_SELL
        price = mt5.symbol_info_tick(symbol).bid
        tp *= -1
        sl *= -1
    
    point = mt5.symbol_info(symbol).point
    
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": trade_type,
        "price": price,
        "sl": price - sl * point,
        "tp": price + tp * point,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python request",
        "type_time": mt5.ORDER_TIME_GTC, 
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    
    result = mt5.order_send(request)
    return result, request

def close_trade(request, result, deviation):
    symbol = request['symbol']
    
    if request['type'] == mt5.ORDER_TYPE_BUY:
        trade_type = mt5.ORDER_TYPE_SELL
        price = mt5.symbol_info_tick(symbol).bid
    elif request['type'] == mt5.ORDER_TYPE_SELL:
        trade_type= mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(symbol).ask
    
    position_id = result.order
    lot = request['volume']
    
    close_request={
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": trade_type,
        "position": position_id,
        "price": price,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python request end",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    
    result = mt5.order_send(close_request)
    
    
result, request = open_trade('sell', 'USDJPY', 1.0, 100, 100, 20)
time.sleep(5)
close_trade(request, result, 10)
    
