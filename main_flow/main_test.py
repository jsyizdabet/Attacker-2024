import stock_filter_past as stfp
import pandas as pd
from portfolioClass import Portfolio
import calculation as cal
import alphas as alp
import sys
sys.path.append('C:\\Users\\Dell\\Documents\\Python\\Attacker-2024\\')
from main_flow import action as act

ticker_list = stfp.read_df5_local()['ticker'].to_list()
# print(ticker_list)

df_percentage = pd.DataFrame({
    'ticker': ticker_list,
    'percentage': [0.1, 0.1, 0.3, 0.2, 0.3]
})
my_portfolio = Portfolio(starting_cash=1000000000, ticker_list=ticker_list, df_percentage=df_percentage)
my_portfolio.show_porfolio()

#### Lấy danh sách signals của 5 mã cổ phiếu
# signal_df = pd.DataFrame(columns=['index', 'time', 'open', 'high', 'low', 'close', 'volume', 'ticker',
#                                   'on-balance_volume', 'OBV_label', 'close_t_minus_1', 'bar_type', 'para',
#                                   'label_spread', 'close_bar_label', 'signal'])

# for ticker in ticker_list:
    
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

data['signal'] = data.apply(alp.Alphas.determine_signal, axis=1)
data = data[data['signal'] != 'Hold']
data.reset_index(inplace=True)



