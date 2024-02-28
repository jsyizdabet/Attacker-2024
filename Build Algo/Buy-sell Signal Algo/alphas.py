
import pandas as pd
import numpy as np
import vnstock as vn
import calculation as cal
 
data = cal.DataProcessor.load_data('VCB')
data = data.set_index('time')
#Tính trung bình 20 phiên gần nhất
mean_20 = data['volume'].rolling(window=20).mean()

#Tính on-balance volume\n",
data['on-balance_volume'] = data['volume']/mean_20
data['OBV_label'] = data['on-balance_volume'].apply(cal.DataProcessor.label_values)

#Giá đóng cửa ngày t-1
data['close_t_minus_1'] = data['close'].shift(1)
data['bar_type'] = data.apply(cal.DataProcessor.compare_close_prices, axis=1)
data['para'] =abs(data['close'] - data['open'])/(data['high'] - data['low'])
data['label_spread'] = data['para'].apply(cal.DataProcessor.label_spread)
data['close_bar_label'] = data.apply(cal.DataProcessor.label_close_bar, axis=1)

# Pattern of Weakness

 # Weakness A
'''
- down bar
- high volume
- medium or low spread
- close: middle-third or bottom-third
'''
def is_weakness_a_signal(data):
    if (data['bar_type'] == 'down-bar') and \
        (data['OBV_label']=='high') and \
        ((data['label_spread'] == 'low') or (data['label_spread']=='medium')) and \
        ((data['close_bar_label'] == 'middle-third') or (data['close_bar_label']=='bottom-third')):
        return True
    else:
        return False

# No Demand - Weakness B
    '''
    - up bar
    - volume: low or high
    - spread: low
    - close: bottom-third and middle-third
    '''
def is_no_demand_signal(data):
    if (data['bar_type'] == 'up-bar') and \
        ((data['OBV_label']=='high') or (data['OBV_label']=='low')) and \
        (data['label_spread'] == 'low') and \
        ((data['close_bar_label'] == 'bottom-third') or data['close_bar_label'] == 'middle-third'):
        return True
    else:
        return False
    

# Up-trust - Pseudo Up-trust
    '''
    - up bar or down bar 
    - high spread
    - close: bottom-third
    - high or low volume
    '''

def is_up_trust_signal(data):
    if ((data['OBV_label']=='high') or (data['OBV_label']=='low')) and \
        (data['label_spread'] == 'high') and \
        ((data['close_bar_label'] == 'bottom-third') ):
        return True
    else:
        return False

# Stop volume
    '''
    - up bar
    - high spread
    - high volume 
    '''
def is_stop_volume_signal(data):
    if (data['bar_type']=='up-bar') and \
        (data['OBV_label']=='high') and \
        (data['label_spread'] == 'high'):
        return True
    else:
        return False
    
# Power pattern

# Power A
    '''
    - up bar
    - medium spread
    - medium or high volume
    - close: top-third
    '''
def is_power_A_signal(data):
    if (data['bar_type'] == 'up-bar') and \
        (data['label_spread'] == 'medium') and \
        ((data['OBV_label']=='medium') or (data['OBV_label'] == 'low')) and \
        (data['close_bar_label'] == 'top-third'):
        return True
    else:
        return False
    
# Power B - Lack of order
    '''
    - down bar 
    - low spread 
    - low or high volume
    - close: top-third or bottom-third
    '''
def is_power_B_signal(data):
    if (data['bar_type'] == 'down-bar') and \
        (data['label_spread'] == 'low') and \
        ((data['OBV_label']=='low') or (data['OBV_label'] == 'high')) and \
        ((data['close_bar_label'] == 'top-third') or (data['close_bar_label'] == 'bottom-third')):
        return True
    else:
        return False

# Reverse Up-Trust - Pseudo Up-trust
    '''
    - up bar or down bar 
    - high spread
    - close: bottom-third
    - high and low volume
    '''
def is_reverse_up_trust_signal(data):
    if ((data['bar_type'] == 'down-bar') or (data['bar_type']) == 'up-bar') and \
        (data['label_spread'] == 'high') and \
        ((data['OBV_label']=='low') or (data['OBV_label'] == 'high')) and \
        (data['close_bar_label'] == 'bottom-third'):
        return True
    else:
        return False
    
# Stopped Volume
    '''
    - down bar
    - low spread
    - close: middle-third
    - high volume
    '''
def is_stopped_volume_signal(data):
    if (data['bar_type'] == 'down-bar') and \
        (data['label_spread'] == 'low') and \
        (data['OBV_label'] == 'high') and \
        (data['close_bar_label'] == 'middle-third'):
        return True
    else:
        return False
