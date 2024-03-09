import pandas as pd

def calculate_portfolio_performance(df):
    total_performance = 0
    df.sort_values(by='date', inplace=True)

    for ticker in df['ticker'].unique():
        df_ticker = df[df['ticker'] == ticker]
        # print(df_ticker)
        ticker_profit = 0

        for index, tran in df_ticker.iterrows():
            if tran['signal'] == 'sell':
                sell_price = tran['price']
                df_buys = df_ticker[df_ticker['signal'] == 'buy']
                df_buys['profit'] = ((sell_price - df_buys['price']) * df_ticker.at[index-1, 'quantity'])/100
                print(df_buys)
                ticker_profit = df_buys['profit'].sum()
                # print(df_buys['profit'].sum())

        total_performance += ticker_profit
    return total_performance

# Tạo DataFrame minh họa
data = {'date': ['2024-01-02', '2024-01-03', '2024-01-01', '2024-01-02', '2024-01-03'],
        'ticker': ['AAPL', 'AAPL', 'GOOGL', 'GOOGL', 'GOOGL'],
        'signal': ['buy', 'buy', 'sell', 'buy', 'sell', 'buy'],
        'price': [ 105, 98, 500, 510, 490],
        'quantity': [ 10, 20, 10, 10, 20]}

df_portfolio = pd.DataFrame(data)
print('input dataframe:', df_portfolio)

# test
total_performance = calculate_portfolio_performance(df_portfolio)

print(f'Hiệu suất tổng cộng của danh mục: {total_performance*100:.2f}%')