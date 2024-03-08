#### Xử lỹ lỗi import module
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
os.path.join(current_dir, 'B')
sys.path.append(os.path.join(current_dir, 'Part_1_Stock_Filtering'))
sys.path.append(os.path.join(current_dir, 'Part_2_Algorithm'))

# ####### Nhập các thư viện và module
import pandas as pd
from Part_1_Stock_Filtering import stock_filter_past as stfp
from Class.portfolioClass import Portfolio
from Part_2_Algorithm import calculation as cal
from Part_2_Algorithm import alphas as alp



###### Lấy danh sách signals của 5 mã cổ phiếu
ticker_list = stfp.get_5_ticker()['ticker'].to_list()
print('Chon ra 5 co phieu thanh cong!', ticker_list)

###### Thiết lập phần trăm danh mục dựa trên weight
df_percentage = pd.DataFrame({
    'ticker': ticker_list,
    'percentage': [0.1, 0.1, 0.3, 0.2, 0.3]
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
    
print(date_performances_df)

'''
###### Code chạy trên mẫu dữ liệu nhỏ
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

# for index, it in signal_df:
#     # print(it['signal'])
#     my_portfolio.validate_transaction(signal_row=it)

for date, group in signal_df.groupby('time'):
    print(f'date {date} group')
    print(group)
    print('.......')
    
####### Kết thúc mẫu thử nhỏ
'''
        

print('============== After trading =================')
my_portfolio.show_porfolio()
print('=========== Extra information ==============')
total_cash = my_portfolio.calculate_holding_stock_values() + my_portfolio.cash_prop
print('*Total cash: ', total_cash)
