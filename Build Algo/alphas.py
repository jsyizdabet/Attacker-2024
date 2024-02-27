
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
data['bar_type'] = data.apply(lambda row: cal.DataProcessor.compare_close_prices(row['close'], row['close_t_minus_1']), axis=1)
data['para'] =abs(data['close'] - data['open'])/(data['high'] - data['low'])
data['labe_spread'] = data['para'].apply(cal.DataProcessor.label_spread)
data['close_bar_label'] = data.apply(cal.DataProcessor.label_close_bar, axis=1)

 # Weakness A
'''
- Down bar
- High volume
- Medium or low spread
- Closing in the middle-third or  bottom-third of the bar
'''
def is_weakness_a_signal(data):
    if (data['bar_type'] == 'down-bar') and \
        (data['OBV_label']=='high') and \
        ((data['labe_spread'] == 'low') or (data['labe_spread']=='medium')) and \
        ((data['close_bar_label'] == 'middle-third') or (data['close_bar_label']=='bottom-third')):
        return True
    else:
        return False

# No Demand
    '''
    '''
def is_nodemand_signal(data):
    if (data['bar_type'] == 'up-bar') and \
        ((data['OBV_label']=='high') or (data['OBV_label']=='low')) and \
        ((data['labe_spread'] == 'low') or (data['labe_spread']=='high')) and \
        ((data['close_bar_label'] == 'bottom-third') ):
        return True
    else:
        return False
    

# Up Trust
    '''
    - Up bar or down bar (This bar must update the local maximum and its maximum should not be redrawn)
    - Spread high
    - The closing should be in the lower third
    - Volume is high or very high
    '''

def is_up_trust_signal(data):
    if ((data['OBV_label']=='high') or (data['OBV_label']=='low')) and \
        (data['labe_spread'] == 'high') and \
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
        (data['labe_spread'] == 'high'):
        return True
    else:
        return False