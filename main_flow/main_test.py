import stock_filter_past as stfp
import pandas as pd
from portfolioClass import Portfolio
import calculation as cal
import alphas as alp
import sys
sys.path.append('C:\\Users\\Dell\\Documents\\Python\\Attacker-2024\\')
from main_flow import action as act

#### Lấy danh sách signals của 5 mã cổ phiếu
ticker_list = stfp.read_df5_local()['ticker'].to_list()
# print(ticker_list)

df_percentage = pd.DataFrame({
    'ticker': ticker_list,
    'percentage': [0.1, 0.1, 0.3, 0.2, 0.3]
})

my_portfolio = Portfolio(starting_cash=1000000000, ticker_list=ticker_list, df_percentage=df_percentage)
print('############### Initial Portfolio ###############')
my_portfolio.show_porfolio()


signal_df = pd.DataFrame(columns=['index', 'time', 'open', 'high', 'low', 'close', 'volume', 'ticker',
                                  'on-balance_volume', 'OBV_label', 'close_t_minus_1', 'bar_type', 'para',
                                  'label_spread', 'close_bar_label', 'signal'])

for ticker in ticker_list:
    data = cal.DataProcessor.load_data(ticker)
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

    signal_df = pd.concat([signal_df, data], ignore_index=True)
print('len of signal_df', len(signal_df))

for index, it in signal_df.iterrows():
    # print(it['signal'])
    my_portfolio.validate_transaction(signal_row=it)


'''
data = cal.DataProcessor.load_data('PNJ')
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
signal_df = pd.concat([signal_df, data], ignore_index=True)
print(signal_df)


for index, it in signal_df.head(20).iterrows():
    # print(it['signal'])
    my_portfolio.validate_transaction(signal_row=it)
'''        
        

print('============== After trading =================')
my_portfolio.show_porfolio()
print('=========== Extra information ==============')
portfolio_stock_df = my_portfolio.portfolio_stock_df
print(portfolio_stock_df)
total_cash = my_portfolio.cash_prop
for index, it in portfolio_stock_df.iterrows():
    if it['holding']:
        ticker = it['ticker']
        signal_filter = signal_df[signal_df['ticker'] == ticker]
        last_row = signal_filter.tail(1)
        print(f'last price of ticker {ticker}: {last_row.at[last_row.index[0], 'close']}')
        total_cash += last_row.at[last_row.index[0], 'close']*it['quantity']
        
print('total cash: ', total_cash)
