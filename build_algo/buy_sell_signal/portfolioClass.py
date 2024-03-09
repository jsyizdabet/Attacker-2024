import pandas as pd
import numpy as np
from datetime import datetime

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
            print(new_buy_power)
            self.stock_df.at[index, 'buy_power'] = new_buy_power
    '''
        Kết thúc khởi tạo portfolio
    '''
    
    '''
        ************
        Utility functions
    '''
    def add_transaction(self, ticker: str, price: int, quantity: int, action: str):
        new_transaction = {
            'time': '20-02-2024',
            'ticker': ticker,
            'price': price,
            'quantity': quantity,
            'action': action,
        }
        # Phương thức append
        self.transaction_list = self.transaction_list._append(new_transaction, ignore_index=True)
        
    def update_buy_power(self):
        for index, it in self.stock_df.iterrows():
            if not it['holding']:
                ticker_percentage = self.stock_df.loc[index]['percentage']
                new_buy_power = self.cash*ticker_percentage
                self.stock_df.loc[index]['buy_power'] = new_buy_power
        
    def validate_buy(self, signal_row):
        signal = signal_row['signal']
        ticker = signal_row['ticker']
        # Kiểm tra cổ phiếu đã được mua hay chưa
        if self.stock_df[ticker]['holding']:
            print(f'Co phieu dang nam giu {ticker}, khong the mua')
            return # Thoát hàm
        
        # Lọc transaction theo ticker và theo action 'sell'
        transList = self.transaction_list
        ticker_trans = transList[(transList['ticker'] == ticker) & (transList['action'] == 'sell')]
        ticker_trans.sort_values(by='time', inplace=True)
        
        # Kiểm tra luật T+2
        signal_date = signal_row['time']
        last_transaction_date = ticker_trans.iloc[-1]['time']
        date_format = '%Y-%m-%d'
        
        date1 = datetime.strptime(signal_date, date_format)
        date2 = datetime.strptime(last_transaction_date, date_format)
        date_difference = date2 - date1
        
        if date_difference >= 2:
            stock_price = signal_row['price']
            tickers_buy_power = self.ticker_list.at[[self.ticker_list['ticker'] == ticker].index, 'buy_power']
            n_of_stocksCanBought = tickers_buy_power/stock_price
            
            # them dieu kien neu can
            self.add_transaction(ticker=ticker, price=stock_price, quantity=n_of_stocksCanBought, action=signal)
            self.ticker_list.at[[self.ticker_list['ticker'] == ticker].index, 'quantity'] = n_of_stocksCanBought
            self.ticker_list.at[[self.ticker_list['ticker'] == ticker].index, 'holding'] = True 
            self.cash -= n_of_stocksCanBought*stock_price
            self.update_buy_power()
            
    def validate_sell(self, signal_row):
        signal = signal_row['signal']
        ticker = signal_row['ticker']
        # Kiểm tra cổ phiếu đã được mua hay chưa
        if not self.stock_df[ticker]['holding']:
            print(f'Khong nam giu co phieu nay {ticker}, khong the ban')
            return # Thoát hàm
        
        # Lọc transaction theo ticker và theo action 'buy'
        transList = self.transaction_list
        ticker_trans = transList[(transList['ticker'] == ticker) & (transList['action'] == 'buy')]
        ticker_trans.sort_values(by='time', inplace=True)
        
        # Kiểm tra luật T+2
        signal_date = signal_row['time']
        last_transaction_date = ticker_trans.iloc[-1]['time']
        date_format = '%Y-%m-%d'
        
        date1 = datetime.strptime(signal_date, date_format)
        date2 = datetime.strptime(last_transaction_date, date_format)
        date_difference = date2 - date1
        
        if date_difference >= 2:
            stock_price = signal_row['price']
            n_of_stock_toSell = self.ticker_list[[]]['']
            # them dieu kien neu can
            
            # Ghi lich su giao dich
            quantity = self.ticker_list.at[[self.ticker_list['ticker'] == ticker].index, 'quantity']
            self.add_transaction(ticker=ticker, price=stock_price, quantity=quantity, action=signal)
            
            # update portfolio
            self.ticker_list.at[[self.ticker_list['ticker'] == ticker].index, 'quantity'] = 0 # Ban het
            self.ticker_list.at[[self.ticker_list['ticker'] == ticker].index, 'holding'] = False 
            self.cash += quantity*stock_price
            self.update_buy_power()
        
    def validate_transaction(self, signal_row):
        signal = signal_row['signal']
        if (signal == 'buy'):
            self.validate_buy(signal_row=signal_row)
        if (signal == 'sell'):
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
    
    '''
        ************
        End Utility functions
    '''
        
'''
    Kết thúc định nghĩa class Portfolio
'''

df_percentage = pd.DataFrame({
    'ticker': ['AAA', 'BBB', 'CCC'],
    'percentage': [0.2, 0.2, 0.6]
})

my_portfolio = Portfolio(starting_cash=1000000000, ticker_list=np.array(['AAA', 'BBB', 'CCC']), df_percentage=df_percentage)
my_portfolio.add_transaction('AAA', 1000, 100, 'buy')
my_portfolio.add_transaction('AAA', 1001, 100, 'buy')
my_portfolio.add_transaction('BBB', 1000, 100, 'buy')
my_portfolio.add_transaction('CCC', 1000, 100, 'buy')

my_portfolio.show_porfolio()
