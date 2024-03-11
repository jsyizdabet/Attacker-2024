from Module import stock_filter_past as stfp

a = 2019
result = stfp.subtract_weekdays(f'{a}-07-01', 20)
print(result)