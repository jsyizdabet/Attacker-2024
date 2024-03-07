import pandas as pd

# Tạo một DataFrame mẫu
data = {'A': [1, 2, 3],
        'B': ['a', 'b', 'c'],
        'C': [0.1, 0.2, 0.3]}

df = pd.DataFrame(data)

# Lấy dòng cuối cùng của DataFrame
last_row = df.tail(1)

# Truy cập giá trị của một cell trong dòng cuối cùng bằng tên cột
cell_value = last_row.at[last_row.index[0], 'B']  # Lấy giá trị ở dòng cuối cùng, cột 'B'

print("Giá trị của cell trong dòng cuối cùng:")
print(cell_value)
