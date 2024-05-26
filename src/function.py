import pandas as pd

# 读取Excel文件，跳过前两行，使用第三行作为列名
prices_path = '../Price.xlsx'
df = pd.read_excel(prices_path, skiprows=2)

# 设置第三列作为索引（站名）
df.set_index(df.columns[2], inplace=True)

# 将数据帧转换为嵌套字典
price_dict = df.to_dict()

routes_path = '../Routes.xlsx'
df = pd.read_excel(routes_path)
df.set_index(df.columns[0], inplace=True)
routes_dict = df.to_dict()


def get_price(in_station, out_station):
    try:
        price = price_dict[in_station][out_station]
        return price
    except KeyError:
        return None  # 或者处理错误


def get_route(start_station, end_station):
    try:
        route = routes_dict[end_station][start_station]
        return route
    except KeyError:
        return None  # 或者处理错误

