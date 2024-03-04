import vnstock as vnst
import pandas as pd

def last_quaterRevenueGrowth(df):
    # Tăng trưởng doanh thu/ lợi nhuận so với quý trước và tăng trưởng EPS trong năm dương
    result = df[df['lastQuarterRevenueGrowth'] > 0]
    return result

def eps_growth1Year(df):
    # Lọc theo điều kiện tăng trưởng EPS trong năm dương
    result = df[df['epsGrowth1Year'] > 0]
    return result

def pe_smallerThan_PE_avg(df):
    # Lọc cổ phiếu theo điều các cổ phiếu có pe bé hơn mức pe trung bình ngành
    industry_pe_avg = df.groupby('industryName.en')['pe'].mean()
    df['Industry_PE_Avg'] = df['industryName.en'].map(industry_pe_avg)
    result  = df[df['pe'] <= df['Industry_PE_Avg']]
    return result

def meanHeath_largerThan_MHIndustry(df):
    # Lọc cổ phiếu theo điều kiện sức khỏe trung bình lớn hơn hoặc bằng sức khỏe trung bình ngành

    # Tạo ra một cột mới là trung bình ngành của businessModel và financialHealth
    df['mean_health_industry'] = df.groupby('industryName.en')[['businessModel', 'financialHealth']].transform('mean').mean(axis=1)
    df['mean_health'] = df[['businessModel', 'financialHealth']].mean(axis=1)

    result = df[df['mean_health'] >= df['mean_health_industry']]
    result.reset_index(drop=True, inplace=True)

    return result

def volume_largerThan_100K(df):
    # Lọc ra những cổ phiếu có mức volume trung bình của 20 phiên gần nhất lớn hơn 100000

    # Tạo ra một dataframe theo volume rỗng
    df_volume = pd.DataFrame(columns=['ticker','volume_average', 'numSession'])

    for index, co in df.iterrows():
        stockHisData = vnst.stock_historical_data(symbol=co[0], start_date="2024-01-23", end_date="2024-02-26", resolution="1D", type="stock", beautify=True, decor=False, source='DNSE')
        mean_volume = stockHisData['volume'].mean()
        df_volume.loc[len(df_volume)] = {'ticker' : co[0], 'volume_average': mean_volume , 'numSession': len(stockHisData) }

    df_merged = pd.merge(df, df_volume[['volume_average','ticker']], on='ticker', how='left')
    result = df_merged[df_merged['volume_average'] > 100000]
    result.reset_index(drop=True, inplace=True)
    return result

def dropColumns(df):
    #  Thêm một vài cột thông tin cho df và loại bỏ các cột không cần thiểt
    List = vnst.listing_companies()
    df_merged = pd.merge(df, List[['ticker', 'industry', 'organName']], on='ticker', how='left')

    # Dataframe cuối và các thuộc tính cần quan tâm
    Stocks_result = df_merged[['ticker', 'marketCap', 'roe', 'stockRating', 'businessModel','financialHealth', 'alpha','beta','pe', 'pb', 'evEbitda', 'revenueGrowth1Year','epsGrowth1Year','foreignVolumePercent','foreignBuySell20Session', 'eps', 'lastQuarterRevenueGrowth','industry', 'industryName.en','organName']]
    
    return Stocks_result

# Lọc những dòng nếu bị NAN thì sẽ tự động drop
def drop_nan_rows(df):
    nan_rows = df[df['stockRating'].isna() | df['businessModel'].isna() | df['volume_average'].isna()]
    df_cleaned = df.dropna(subset=['stockRating', 'businessModel', 'volume_average'])
    return df_cleaned

def sortingAndDrop_nan(df):
    # Dataframe cuối cùng là datafame được sắp xếp stockRating từ lớn đến nhỏ
    sorted_by_rating_stocks = df.sort_values(by='stockRating', ascending=False)
    dropped_nan_rows = drop_nan_rows(sorted_by_rating_stocks)
    dropped_nan_rows = dropped_nan_rows.set_index('ticker')
    # Dataframe cuối cùng
    return dropped_nan_rows

def stock_filter_now():
    # Tạo danh sách công ty thỏa mãn các tiêu chuẩn cơ bản sau:
    # Sàn giao dịch: HOSE, HXN, UPCOM
    # Vốn hóa thị trường: trên 100 tỷ
    # ROE trên 20%
    params = {
                "exchangeName": "HOSE,HNX,UPCOM",
                "marketCap": (100,99999999),
                "roe": (0.2, 99)
            }
    filter = vnst.stock_screening_insights (params, size=1700, drop_lang='vi')
    print('Filtered by cap > 100, ROE > 20%')
    filter = last_quaterRevenueGrowth(filter)
    print('Filtered by last growth revenue 1 year')
    filter = eps_growth1Year(filter)
    print('Filtered by eps growth 1 year')
    filter = dropColumns(filter)
    filter = pe_smallerThan_PE_avg(filter)
    print('Filtered by PE < industry PE average')
    filter = meanHeath_largerThan_MHIndustry(filter)
    print('Filtered by mean heath > industry mean heath')
    filter = volume_largerThan_100K(filter)
    print('Filtered by last 20 sessions volume > 100K')
    result = sortingAndDrop_nan(filter)

    print('Completed filter')
    return result