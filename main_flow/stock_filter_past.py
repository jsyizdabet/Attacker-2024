# import các thư viện cần thiết
import vnstock as vnst
import pandas as pd
import os

def basic_filter(df):
    # Lọc theo một vài tiêu chí cơ bản
    df2 = df[(df['roe'] > 0.2) & (df['earningPerShare'] > 2500) & (df['epsChange'] > 0)]
    df2.reset_index(drop=True, inplace=True)
    return df2

def pe_largerThan_pe_avg(df):
    # Tạo dataframe chứa dữ liệu P/E trung bình theo ngành
    df_pe_byIndustry = df.groupby('industry').agg(
        avg_pe = ('priceToEarning', 'mean')
    )

    # Thêm giá trị trung bình P/E theo ngành cho cột 'pe_avg' của dataframe
    for index, co in df.iterrows():
        # 'co' is a tuple, so we can get the industry name like this
        industryName = co[11] #column index = 11
        # get the pe average value
        df.at[index, 'pe_avg'] =  df_pe_byIndustry.loc[industryName][0]

    result = df[df['priceToEarning'] > df['pe_avg']]
    return result

def volume_largerThan_100K(df):
    # ------ Khối lượng trung bình 20 phiên gần nhất của từng cổ phiếu: Volume trung bình > 100 ngàn

    # Tạo một df chứa ticker và trung bình Volume của 20 phiên gần nhất
    df_volume = pd.DataFrame(columns=['ticker','volume_average', 'numSession'])
    for index, co in df.iterrows():
        # Tính tổng volume của 20 phiên gần nhất
        stockHisData = vnst.stock_historical_data(symbol=co[0], start_date="2018-06-04", end_date="2018-07-01", resolution="1D", type="stock", beautify=True, decor=False, source='DNSE')        
        mean_volume =stockHisData['volume'].mean()
        df_volume.loc[len(df_volume)] = {'ticker' : co[0], 'volume_average': mean_volume , 'numSession': len(stockHisData) }

    # Thêm cột thông tin về trung bình Volume (volume_average) vào dataframe    
    df_merged = pd.merge(df, df_volume[['ticker', 'volume_average']], on='ticker', how='left')

    # Khối lượng giao dịch 20 phiên gần nhất > 100 ngàn
    df_result = df_merged[df_merged['volume_average'] > 100000]
    df_result.reset_index(drop=True, inplace=True)
    return df_result


def stock_filter_past():
    # ---- Chuẩn bị dataframe dữ liệu thô
    # Nhập dữ liệu từ file thông tin đã tải xuống của năm 2018
    # và loại bỏ các cột không cần thiết, các dòng trùng lặp (nếu có)
    # Lấy đường dẫn tuyệt đối của file
    current_directory = os.path.dirname(__file__)
    file_path = os.path.join(current_directory, 'data_Q3-2018-mergedIndustry.csv')
    df = pd.read_csv(file_path)
    df.drop('Unnamed: 0', axis=1, inplace=True)
    df.drop_duplicates(subset='ticker', keep='first', inplace=True)
    df_dropColumns = df[['ticker', 'quarter', 'year', 'priceToEarning', 'priceToBook', 'roe',
        'roa', 'earningPerShare', 'bookValuePerShare','epsChange','bookValuePerShareChange', 'industry', 'organName']]
    # Thêm cột giá trị P/E trung bình cho dataframe
    df_dropColumns['pe_avg'] = 0
    df_dropColumns.reset_index(drop=True, inplace=True)

    filter = pe_largerThan_pe_avg(df_dropColumns)
    filter = basic_filter(filter)
    result = volume_largerThan_100K(filter)
    return result

def read_df5_local():
    current_directory = os.path.dirname(__file__)
    file_path = os.path.join(current_directory, '5_tickers_local.csv')
    df = pd.read_csv(file_path).head(5)
    return df