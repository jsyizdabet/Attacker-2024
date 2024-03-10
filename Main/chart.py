#### Xử lỹ lỗi import module
import plotly.graph_objects as go
import streamlit as st
from datetime import date
import vnstock as vn

import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'Part_1_Stock_Filtering'))
sys.path.append(os.path.join(current_dir, 'Part_2_Algorithm'))

# ####### Nhập các thư viện và module
import pandas as pd
from StockFiltering import stock_filter_past as stfp
from Class.portfolioClass import Portfolio
from Algorithm import calculation as cal
from Algorithm import alphas as alp

#-------------------------------

st.subheader('Buy and sell signal chart')

stocks = ('MWG','VCG','BMP','VCS','GIL')
selected_stock = st.selectbox('Select stock', stocks)
data = cal.DataProcessor.load_data(selected_stock)
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
# data.reset_index(inplace=True)
signal_counts = data['signal'].value_counts()

# print(data.columns)
# # bat dau trade

# print("Số lượng 'Sell':", signal_counts.get('Sell', 0))
# print("Số lượng 'Buy':", signal_counts.get('Buy', 0))
# print("Số lượng 'Hold':", signal_counts.get('Hold', 0))



#------------
import pandas as pd
from datetime import date
import plotly.graph_objects as go
import streamlit as st

def plot_buy_sell_signal(data, selected_stock):
    fig = go.Figure()

    # Vẽ biểu đồ dựa trên tín hiệu mua bán
    buy_signals = data[data['signal'] == 'Buy']
    sell_signals = data[data['signal'] == 'Sell']

    # Hiển thị nút lọc
    col1, col2 = st.columns([0.4, 0.5])
    with col1:
        start_date = st.date_input("Start", min_value=date(2018, 7, 1), max_value=date.today(), key="start_date", value=date(2018, 7, 1))
    with col2:
        end_date = st.date_input("End", min_value=date(2018, 7, 1), max_value=date.today(), key="end_date")

    # Lọc dữ liệu
    filtered_buy_signals = buy_signals[(buy_signals['time'] >= start_date) & (buy_signals['time'] <= end_date)]
    filtered_sell_signals = sell_signals[(sell_signals['time'] >= start_date) & (sell_signals['time'] <= end_date)]

    # Tạo DataFrame mới
    signal_counts = data['signal'].value_counts()

    signal_data = {'Buy': [len(filtered_buy_signals)], 'Sell': [len(filtered_sell_signals)], 'Hold': [signal_counts.get('Hold', 0)]}
    signal_df = pd.DataFrame(signal_data)

    # Vẽ biểu đồ
    fig.add_trace(go.Scatter(x=data['time'], y=data['close'], mode='lines', name='Closing Price'))
    fig.add_trace(go.Scatter(x=filtered_buy_signals['time'], y=filtered_buy_signals['close'], mode='markers', name='Buy', marker=dict(color='green', symbol='triangle-up')))
    fig.add_trace(go.Scatter(x=filtered_sell_signals['time'], y=filtered_sell_signals['close'], mode='markers', name='Sell', marker=dict(color='red', symbol='triangle-down')))

    # Cấu hình biểu đồ
    fig.update_layout(title=f'Buy and sell signal of {selected_stock}', xaxis_title='Time', yaxis_title='Closing Price')
    
    # Cập nhật khoảng thời gian trên trục x của biểu đồ
    fig.update_layout(xaxis_range=[start_date, end_date])
    st.write(signal_df)

    return fig
filtered_fig = plot_buy_sell_signal(data, selected_stock)
st.plotly_chart(filtered_fig, use_container_width=True)

#----------------------------------------------
vnindex = vn.stock_historical_data("VNINDEX", "2018-07-01", "2024-02-01", type="index")
vnindex['performance_vnindex'] = 100 * (vnindex['close'] - vnindex['close'].iloc[0]) / (vnindex['close'].iloc[0])
vnindex1 = vnindex[['time', 'performance_vnindex']]
vnindex1['time'] = pd.to_datetime(vnindex1['time'])

date_performances_df = date_performances_df.rename({'date':'time'})
date_performances_df['time'] = pd.to_datetime(date_performances_df['time'])

merge_port_vnindex = pd.merge(date_performances_df, vnindex1, on='time', how="inner")

st.write(merge_port_vnindex)
