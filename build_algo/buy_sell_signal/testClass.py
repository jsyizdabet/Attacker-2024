import pandas as pd

# Tạo DataFrame1 và DataFrame2 để minh họa
data1 = {'ticker': ['AAPL', 'GOOGL', 'MSFT'],
         'value1': [10, 20, 30]}
df1 = pd.DataFrame(data1)

data2 = {'ticker': ['GOOGL', 'AAPL', 'MSFT'],
         'value2': [100, 200, 300]}
df2 = pd.DataFrame(data2)

# Hiển thị DataFrame1 và DataFrame2 ban đầu
print("DataFrame1:")
print(df1)

print("\nDataFrame2:")
print(df2)

# Thay thế giá trị cột 'value1' trong DataFrame1 bằng giá trị của cột 'value2' trong DataFrame2
df1['value1'] = df2['value2']

# Hiển thị DataFrame1 sau khi thay đổi
print("\nDataFrame1 sau khi thay đổi:")
print(df1)