import pandas as pd
import numpy as np
import vnstock as vn
import calculation as cal
import alphas as alp

# import sys
# sys.path.append('D:\DATA ANALYSIS\COMPETITION\ATTACKER\ATTACKER\Attacker-2024\Build Algo\Portfolio Balancing Algo')
# from Portfolio Balancing Algo import action as act

# import sys
# sys.path.append('C:\\Users\\Dell\\Documents\\Python\\Attacker-2024\\build_algo')
# from portfolio_balancing import action as act

data = cal.DataProcessor.load_data('VCB')
# data = data.set_index('time')
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
print('hhh',data)

#tính RSI
data['delta'] = data['close'] - data['close'].shift(1)
data['gains'] = data['delta'].where(data['delta'] > 0, 0)
data['losses'] = -data['delta'].where(data['delta'] < 0, 0)
data['avg_gain'] = data['gains'].rolling(window=14).mean()
data['avg_loss'] = data['losses'].rolling(window=14).mean()
data['rs'] = data['avg_gain'] / data['avg_loss']
data['RSI'] = 1 - (1 / (1 + data['rs']))
print('---',data)

data['signal'] = data.apply(alp.Alphas.determine_signal, axis=1)
# data = data[data['signal'] != 'Hold']
# data.reset_index(inplace=True)
signal_counts = data['signal'].value_counts()

print(data.columns)
print(data)
# bat dau trade

print("Số lượng 'Sell':", signal_counts.get('Sell', 0))
print("Số lượng 'Buy':", signal_counts.get('Buy', 0))
print("Số lượng 'Hold':", signal_counts.get('Hold', 0))

# portfolio_return = act.calculate_portfolio_return(data)
# print("Portfolio return:", portfolio_return)