import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
import stock_filter_past as stfp

stock_df = stfp.stock_filter_past()

result = stock_df.sort_values('roe').head(5)
print(result)

