import datetime
import pytz
import schedule
import time
import ntplib
from pandas.tseries.offsets import BDay


# 将日期调整到最近的工作日
def adjust_date_to_weekday(date):
    # 如果提供的日期是周末，将其调整为最近的工作日
    if date.weekday() > 4:  # 0 = Monday, 1=Tuesday, 2=Wednesday...
        return date - BDay(1)  # subtract one business day
    return date


def get_network_time():
    # 创建一个 NTPClient 对象
    client = ntplib.NTPClient()

    # 获取网络时间（UTC）
    response = client.request("pool.ntp.org")

    timestamp = response.tx_time
    network_time = datetime.datetime.fromtimestamp(timestamp)

    # 获取本地时区
    local_timezone = pytz.timezone("Asia/Shanghai")  # 例如 'Asia/Shanghai'
    # 从时区上获得的本地时间理论上与网络时间一致，可能存在一些网络延迟,但影响不大
    local_time = network_time.astimezone(local_timezone)

    # print(local_time.hour)
    # print(network_time.hour)
    return local_time


def get_local_time():
    local_time = datetime.datetime.now()
    return local_time
