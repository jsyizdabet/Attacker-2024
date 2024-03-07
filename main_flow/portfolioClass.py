import pandas as pd
import numpy as np
from datetime import datetime, date

class Portfolio:
    '''
        Khởi tạo portfolio
    '''
    def __init__(self, starting_cash, ticker_list, df_percentage):
        self.cash = starting_cash
        self.ticker_list = ticker_list
        self.stock_df = self.create_stock_df(ticker_list=ticker_list)
        self.transaction_list = self.create_transaction_list()
        self.update_percentage(df_percentage=df_percentage)
        self.init_buy_power();

    def create_stock_df(self, ticker_list):
        ticker_list_len = len(ticker_list) 
        data = {
            'ticker': ticker_list,
            'percentage': [0.0]*ticker_list_len,
            'weight': [0.0]*ticker_list_len,
            'buy_power': [0]*ticker_list_len,
            'holding': [False]*ticker_list_len,
            'quantity': [0]*ticker_list_len
        }
        stock_df = pd.DataFrame(data)
        return stock_df
    
    def update_percentage(self, df_percentage):
        self.stock_df['percentage'] = df_percentage['percentage'].values
        
    
    def create_transaction_list(self):
        data = {
            'time': [],
            'ticker': [],
            'price': [],
            'quantity': [],
            'action': []
        }      
        transaction_list = pd.DataFrame(data)
        return transaction_list
    
    def init_buy_power(self):
        for index, it in self.stock_df.iterrows():
            ticker_percentage = self.stock_df.loc[index]['percentage']
            new_buy_power = self.cash*ticker_percentage
            # print(new_buy_power)
            self.stock_df.at[index, 'buy_power'] = new_buy_power
    '''
        Kết thúc khởi tạo portfolio
    '''
    
    '''
        ************
        Utility functions
    '''
    def add_transaction(self, time: str, ticker: str, price: int, quantity: int, action: str):
        new_transaction = {
            'time': time,
            'ticker': ticker,
            'price': price,
            'quantity': quantity,
            'action': action,
        }
        # Phương thức append
        self.transaction_list = self.transaction_list._append(new_transaction, ignore_index=True)
        
    def update_buy_power(self):
        print('***Update buy power for each ticker ')
        print('Current cash: ', self.cash)
        for index, it in self.stock_df.iterrows():
            if not it['holding']:
                ticker_percentage = self.stock_df.loc[index]['percentage']
                new_buy_power = self.cash*ticker_percentage
                self.stock_df.at[index, 'buy_power'] = new_buy_power
        
    def validate_buy(self, signal_row):
        signal = signal_row['signal']
        ticker = signal_row['ticker']
        
        # Kiểm tra cổ phiếu đã được mua hay chưa
        index_of_ticker = self.stock_df[self.stock_df['ticker'] == ticker].index[0]
        if self.stock_df.at[index_of_ticker, 'holding']:
            print(f'Co phieu dang nam giu {ticker}, khong the mua')
            return # Thoát hàm
        
        # Lọc transaction theo ticker và theo action 'sell'
        transList = self.transaction_list
        ticker_trans = transList[(transList['ticker'] == ticker) & (transList['action'] == 'Sell')]
        ticker_trans.sort_values(by='time', inplace=True)
        
        # print(ticker_trans)
        # return
        
        # Kiểm tra luật T+2
        signal_date = signal_row['time']
        if not ticker_trans.empty:
            last_transaction_date = ticker_trans.iloc[-1]['time']
            date_format = '%Y-%m-%d'
            date_difference = (signal_date - last_transaction_date).days
            # print('difference days: ', date_difference)
            if date_difference < 2:
                print(f'Khong mua do tien ban lan truoc chua ve {ticker}')
                return
            
        stock_price = signal_row['close']
        tickers_buy_power = self.stock_df.at[index_of_ticker, 'buy_power']
        n_of_stocksCanBought = np.floor(tickers_buy_power/stock_price)
        
        # them dieu kien neu can
        
        # Ghi lai lich su mua
        self.add_transaction(time=signal_date, ticker=ticker, price=stock_price, quantity=n_of_stocksCanBought, action=signal)
        
        self.stock_df.at[index_of_ticker, 'quantity'] = n_of_stocksCanBought
        self.stock_df.at[index_of_ticker, 'holding'] = True
        self.cash -= n_of_stocksCanBought*stock_price
        
        # There no need to update buy power when a ticker is bought
        # self.update_buy_power()
            
    def validate_sell(self, signal_row):
        signal = signal_row['signal']
        ticker = signal_row['ticker']
        
        # Kiểm tra cổ phiếu đã được mua hay chưa
        index_of_ticker = self.stock_df[self.stock_df['ticker'] == ticker].index[0]
        if not self.stock_df.at[index_of_ticker, 'holding']:
        # [self.stock_df['ticker'] == ticker]].index, 'holding']:
            print(f'Khong nam giu co phieu nay {ticker}, khong the ban')
            return # Thoát hàm
        
        # Lọc transaction theo ticker và theo action 'buy'
        transList = self.transaction_list
        ticker_trans = transList[(transList['ticker'] == ticker) & (transList['action'] == 'Buy')]
        ticker_trans.sort_values(by='time', inplace=True)
        
        # Kiểm tra luật T+2
        signal_date = signal_row['time']
        if not ticker_trans.empty:
            last_transaction_date = ticker_trans.iloc[-1]['time']
            # print('date1 ', signal_date)
            # print('date2 ', last_transaction_date)
            date_difference = (signal_date - last_transaction_date).days
            if (date_difference < 2):
                print(f'Khong ban do co phieu mua chua nhan duoc {ticker}')
                return
                
        stock_price = signal_row['close']
        # Ghi lich su ban
        n_of_stock_toSell = self.stock_df.at[index_of_ticker, 'quantity']
        # quantity = self.ticker_list.at[[self.ticker_list['ticker'] == ticker].index, 'quantity']
        self.add_transaction(time=signal_date, ticker=ticker, price=stock_price, quantity=n_of_stock_toSell, action=signal)
        
        # update portfolio
        self.stock_df.at[index_of_ticker, 'quantity'] = 0 # Ban het
        self.stock_df.at[index_of_ticker, 'holding'] = False 
        self.cash += n_of_stock_toSell*stock_price
        self.update_buy_power()
        
    def validate_transaction(self, signal_row):
        signal = signal_row['signal']
        if (signal == 'Buy'):
            self.validate_buy(signal_row=signal_row)
        if (signal == 'Sell'):
            self.validate_sell(signal_row=signal_row) 
    
    def show_porfolio(self):
        print('==============PORTFOLIO================')
        print('*Money: ', self.cash)
        print('*Stocks\n', self.stock_df)
        self.show_transaction_history()
        print('=======================================')
        
    def show_transaction_history(self):
        print('*Transaction history\n', self.transaction_list)
        
    def testList(self):
        transList = self.transaction_list
        result = transList[transList['ticker'] == 'aaa']
        print(result)
        
    # Getter cho thuộc tính
    @property
    def portfolio_stock_df(self):
        return self.stock_df
    
    @property
    def cash_prop(self):
        return self.cash
    
    '''
        ************
        End Utility functions
    '''
        
'''
    Kết thúc định nghĩa class Portfolio
'''


