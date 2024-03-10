# import stock_filter
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
from Algorithm import weight as wi



###### Lấy danh sách signals của 5 mã cổ phiếu
ticker_list = stfp.get_5_ticker(year=2020)['ticker'].to_list()
print('Chon ra 5 co phieu thanh cong!', ticker_list)

# list_stock = ['MWG', 'VCG', 'BMP', 'VCS', 'GIL']
df_combined =  wi.get_combined_df(ticker_list, 2020)
weight_df = wi.cal_weight(df_combined, ticker_list)
weight_df.head()
print(weight_df)
# list_stock = ['SSI','HPG','VND','GAS','FPT']
# df_combined =  wi.get_combined_df(list_stock=ticker_list, trading_year=2020)
# weight_df = wi.cal_weight(df_combined, ticker_list)
# weight_df.head()
# print(weight_df)