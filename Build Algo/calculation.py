
#import libraries
import pandas as pd
import numpy as np
import vnstock as vn

class DataProcessor:
    def __init__(self, data):
        self.data = data
    
    #load_data
    def load_data(ticker):
        START = "2019-01-01"
        END = "2024-02-01"
        data = vn.stock_historical_data(ticker, START, END)    
        return data
    
    #main 1
    data = load_data('VCB') 
    data = data.set_index('time')
    mean_20 = data['volume'].rolling(window=20).mean() #Tính trung bình 20 phiên gần nhất
    data['on-balance_volume'] = data['volume']/mean_20 #Tính on-balance volume
    
    #lable volume
    def label_values(a):
        if pd.isnull(a):
            return a
        elif a < 0.75:
            return 'low'
        elif 0.75 <= a <= 1.25:
            return 'medium'
        else:
            return 'high'
    
    #main 2
    data['OBV_label'] = data['on-balance_volume'].apply(label_values)

    #Bar
    def compare_close_prices(t, t_minus_1):
        if t > t_minus_1:
            return 'up-bar'  
        else:
            return 'down-bar'
    #main 3
    data['close_t_minus_1'] = data['close'].shift(1) #Giá đóng cửa ngày t-1
    data['bar_type'] = data.apply(lambda row: compare_close_prices(row['close'], row['close_t_minus_1']), axis=1)   
    data['para'] =abs(data['close'] - data['open'])/(data['high'] - data['low'])

    #lable spread
    def label_spread(a):
        if 0 < a < 0.3: return 'low'
        elif 0.3 <= a <= 0.7: return 'medium'
        else: return 'high'
    
    #main 4
    data['labe_spread'] = data['para'].apply(label_spread)

    #Close bar
    def label_close_bar(data):
        q1 = data['low'] + (data['high'] - data['low'])/3
        q2 = data['low'] + 2*((data['high'] - data['low'])/3)
        if data['close'] < q1:
            return 'bottom-third'
        elif q1 <= data['close'] <= q2:
            return 'middle-third'
        else:
            return 'top-third'
    
    #main 5
    data['close_bar_label'] = data.apply(label_close_bar, axis=1)