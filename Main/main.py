#### Xử lỹ lỗi import module
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'StockFiltering'))
sys.path.append(os.path.join(current_dir, 'Algorithm'))

# ####### Nhập các thư viện và module
import pandas as pd
from StockFiltering import stock_filter_past as stfp
from Class.portfolioClass import Portfolio
from Algorithm import calculation as cal
from Algorithm import alphas as alp


trading_year = 2020
###### Lấy danh sách signals của 5 mã cổ phiếu
ticker_list = stfp.get_5_ticker(year=trading_year-1)['ticker'].to_list()
# ticker_list = pd.read_csv('five_ticker_2018.csv')['ticker'].to_list()
# print('Chon ra 5 co phieu thanh cong!', ticker_list)

###### Thiết lập phần trăm danh mục dựa trên weight
df_percentage = pd.DataFrame({
    'ticker': ticker_list,
    # 'percentage': [0.3513, 0.05, 0.353, 0.1957, 0.05]
    'percentage': [0.279945, 0.05, 0.05, 0.570055, 0.05]
    # 'percentage': [0.05, 0.062, 0.7628, 0.0752, 0.05]
})

###### Khởi tạo portfolio
my_portfolio = Portfolio(starting_cash=1000000000, ticker_list=ticker_list, df_percentage=df_percentage)
print('############### Initial Portfolio ###############')
my_portfolio.show_porfolio()

###### Tạo dataframe tín hiệu
signal_df = pd.DataFrame(columns=['index', 'time', 'open', 'high', 'low', 'close', 'volume', 'ticker',
                                  'on-balance_volume', 'OBV_label', 'close_t_minus_1', 'bar_type', 'para',
                                  'label_spread', 'close_bar_label', 'signal'])

for ticker in ticker_list:
    data = cal.DataProcessor.load_data(ticker=ticker, year=trading_year)
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

    signal_df = pd.concat([signal_df, data], ignore_index=True)
signal_df.sort_values(by='time')

print('Danh sách tín hiệu dài ', len(signal_df))

####### Thực hiện xét tín hiệu để giao dịch
date_performances_df = pd.DataFrame(columns=['date', 'performance']);
for date, group in signal_df.groupby('time'):
    print(f'**time {date}')
    for index, row in group.iterrows():
        my_portfolio.validate_transaction(signal_row=row)
    date_performance = my_portfolio.cal_performance()
    date_performances_df.loc[len(date_performances_df)] = [date, date_performance]
    print('**')
    
print(date_performances_df.sample(20))


print('============== After trading =================')
my_portfolio.show_porfolio()
print('=========== Extra information ==============')
total_cash = my_portfolio.calculate_holding_stock_values() + my_portfolio.cash_prop + my_portfolio.get_pending_money()
print('*Total revenue: ', total_cash)
portfolio_performance, per_per_tick = my_portfolio.portfolio_performance()
print('Total performance', portfolio_performance*100, '%')
print('List performance per ticker')
print(per_per_tick)