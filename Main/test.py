#### Xử lỹ lỗi import module
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
sys.path.append(os.path.join(current_dir, 'StockFiltering'))
sys.path.append(os.path.join(current_dir, 'Algorithm'))

# ####### Nhập các thư viện và module
import pandas as pd
from StockFiltering import stock_filter_past as stfp
from Class.portfolioClass import Portfolio
from Algorithm import calculation as cal
from Algorithm import alphas as alp


trading_year = 2019
###### Lấy danh sách signals của 5 mã cổ phiếu
# ticker_list = stfp.get_5_ticker(year=trading_year-1)
ticker_list = pd.read_csv('five_ticker_2018.csv')['ticker'].to_list()
print(ticker_list)
