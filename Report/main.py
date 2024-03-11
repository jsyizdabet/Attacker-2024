#### Xử lỹ lỗi import module
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'Module'))
sys.path.append(os.path.join(current_dir, 'Data'))

# ####### Nhập các thư viện và module
import pandas as pd
from Module.portfolioClass import Portfolio
from Module import stock_filter_past as stfp
from Module import calculation as cal , weight as wi
calUtil = cal.DataProcessor

for trading_year in range(2019, 2020):
    
    ###### Lấy danh sách signals của 5 mã cổ phiếu
    ticker_list = stfp.get_5_ticker(year=trading_year-1)['ticker'].to_list()

    ###### Thiết lập phần trăm danh mục dựa trên weight
    df_combined =  wi.get_combined_df(ticker_list, trading_year)
    weight_df = wi.cal_weight(df_combined, ticker_list)
    weight_df.head()
    
    ###### Khởi tạo portfolio
    my_portfolio = Portfolio(starting_cash=1000000000, ticker_list=ticker_list, df_percentage=weight_df)
    print("### Trading year: ", trading_year)
    print('Initial Portfolio')
    my_portfolio.show_porfolio()

    ###### Tạo dataframe tín hiệu ######
    signal_df = cal.DataProcessor.get_signals_df(self=calUtil, ticker_list=ticker_list, trading_year=trading_year)
    ##########

    ####### Thực hiện xét tín hiệu để giao dịch
    date_performances_df = pd.DataFrame(columns=['date', 'performance']);
    for date, group in signal_df.groupby('time'):
        # print(f'**time {date}')
        for index, row in group.iterrows():
            my_portfolio.validate_transaction(signal_row=row)
        date_performance = my_portfolio.daily_performance()
        date_performances_df.loc[len(date_performances_df)] = [date, date_performance]
        # print('**')
        
    date_performances_df.to_csv(f'Visualization_{trading_year}.csv', index=False)

    print('============== After trading ================')
    my_portfolio.show_porfolio()
    
    portfolio_performance, per_per_tick = my_portfolio.portfolio_performance()
    print('*Total performance', round(portfolio_performance*100, 2), '%')
    print('*List performance per ticker')
    print(per_per_tick)




