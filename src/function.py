import pandas as pd

# 读取Excel文件，跳过前两行，使用第三行作为列名
file_path = '../Price.xlsx'
df = pd.read_excel(file_path, skiprows=2)

# 设置第三列作为索引（站名）
df.set_index(df.columns[2], inplace=True)


# 将数据帧转换为嵌套字典
price_dict = df.to_dict()

def get_price(in_station, out_station):
    try:
        price = price_dict[in_station][out_station]
        return price
    except KeyError:
        return None  # 或者处理错误

