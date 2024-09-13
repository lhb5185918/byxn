import requests
from datetime import datetime, timedelta
import yaml
import os
import sys
from dateutil.relativedelta import relativedelta


def get_token():
    url = "http://192.168.111.108:9994/oauth/password/unencrypted"
    data = {"userNo": "lhb", "pwd": "lhx7758521", "platForm": "app", "companyCode": "QDBYYYGF", "whId": 817929940341248,
            "warehouseId": 817929940341248, "haveWarehouse": 1, "clientId": "iowtb", "userLanguage": "zh-CN"}
    res = requests.post(url=url, json=data, headers={'Content-Type': 'application/json'})
    token = res.json()['obj']['token']
    headers = {'Content-Type': 'application/json', 'Authorization': token}
    return headers


def time_slp():
    # 获取今天的日期
    today = datetime.now().date()

    # 生成今天的零点时间
    midnight = datetime.combine(today, datetime.min.time())  # 今天的零点
    # 生成今天的 23:59:59 时间
    end_of_day = datetime.combine(today, datetime.max.time().replace(hour=23, minute=59, second=59, microsecond=0))

    # 格式化为字符串
    midnight_str = midnight.strftime('%Y-%m-%d %H:%M:%S')
    end_of_day_str = end_of_day.strftime('%Y-%m-%d %H:%M:%S')
    return {"start": midnight_str, "end": end_of_day_str}


def select_time():
    # 获取当前时间
    current_time = datetime.now()

    # 计算三个月前的时间
    three_months_ago = current_time - relativedelta(months=3)

    # 格式化为字符串
    current_time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
    three_months_ago_str = three_months_ago.strftime('%Y-%m-%d %H:%M:%S')

    return {"current_time": current_time_str, "three_months_ago": three_months_ago_str}

def read_yaml(file_path, key=None, value=None):
    with open(file_path, 'r', encoding="utf-8") as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
        if key is None:
            return data
        else:
            if value is None:
                return data[key]
            else:
                for item in data[key]:
                    if value is None:
                        return item
                    else:
                        return item[value]


def write_yaml(file_path, moudle_name, key, value):
    # 读取YAML文件
    with open(file_path, 'r', encoding="utf-8") as file:
        data = yaml.safe_load(file)

    # 遍历数据并修改指定的字段
    for item in data[moudle_name]:
        if key in item:
            item[key] = value

    # 将修改后的内容写回到YAML文件中
    with open(file_path, 'w', encoding="utf-8") as file:
        yaml.safe_dump(data, file, default_flow_style=False, allow_unicode=True)
    return data


def base_path(path):
    if getattr(sys, 'frozen', None):
        basedir = sys._MEIPASS
    else:
        basedir = os.path.dirname(__file__)
    return os.path.join(basedir, path)


