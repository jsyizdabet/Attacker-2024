# import libraries
import pandas as pd
import numpy as np
import vnstock as vn
import warnings
from Module import alphas as alp

class DataProcessor:
    def __init__(self, data):
        self.data = data
    
    #load_data
    def load_data(ticker, year):
        START = f"{year}-01-01"
        END = f"{year+1}-02-01"
        data = vn.stock_historical_data(ticker, START, END)    
        return data

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

    #Bar
    def compare_close_prices(row):
        t = row['close']
        t_minus_1 = row['close_t_minus_1']
        if t > t_minus_1:
            return 'up-bar'
        else:
            return 'down-bar'

    #lable spread
    def label_spread(a):
        if 0 < a < 0.3: return 'low'
        elif 0.3 <= a <= 0.7: return 'medium'
        else: return 'high'

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

    def get_signals_df(self, ticker_list, trading_year):
        signal_df = pd.DataFrame(columns=['index', 'time', 'open', 'high', 'low', 'close', 'volume', 'ticker',
                                    'on-balance_volume', 'OBV_label', 'close_t_minus_1', 'bar_type', 'para',
                                    'label_spread', 'close_bar_label', 'signal'])

        for ticker in ticker_list:
            data = self.load_data(ticker=ticker, year=trading_year)
            # data = data.set_index('time')
            #Tính trung bình 20 phiên gần nhất
            mean_20 = data['volume'].rolling(window=20).mean()

            #Tính on-balance volume\n",
            data['on-balance_volume'] = data['volume']/mean_20
            data['OBV_label'] = data['on-balance_volume'].apply(self.label_values)

            #Giá đóng cửa ngày t-1
            data['close_t_minus_1'] = data['close'].shift(1)
            data['bar_type'] = data.apply(self.compare_close_prices, axis=1)
            data['para'] =abs(data['close'] - data['open'])/(data['high'] - data['low'])
            data['label_spread'] = data['para'].apply(self.label_spread)
            data['close_bar_label'] = data.apply(self.label_close_bar, axis=1)
                
            #tính RSI
            data['delta'] = data['close'] - data['close'].shift(1)
            data['gains'] = data['delta'].where(data['delta'] > 0, 0)
            data['losses'] = -data['delta'].where(data['delta'] < 0, 0)
            data['avg_gain'] = data['gains'].rolling(window=14).mean()
            data['avg_loss'] = data['losses'].rolling(window=14).mean()
            data['rs'] = data['avg_gain'] / data['avg_loss']
            data['RSI'] = 1 - (1 / (1 + data['rs']))

            data['signal'] = data.apply(alp.Alphas.determine_signal, axis=1)
            # data = data[data['signal'] != 'Hold']
            data.reset_index(inplace=True)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=FutureWarning)
                signal_df = pd.concat([signal_df, data], ignore_index=True)
        signal_df.sort_values(by='time')
        return signal_df