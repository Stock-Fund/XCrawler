import src.data_processor as data_processor
import src.html as html
from algorithm.stock import Stock
from datetime import datetime, time
import pandas as pd
import asyncio


check = False


def getStockTimeData(date_part, time_part, name, enginstr, timename):
    # 某只股票所有的第三方数据
    stockCustomData = data_processor.GetAllDataFromTable(name, enginstr)
    # 某只股票分时数据
    stockTimeData = data_processor.GetDatasFromSql2(
        timename,
        {"id": "日期", "value": date_part},
        {"id": "时间", "value": time_part},
        enginstr,
    )

    if stockTimeData is None:
        print(f"{timename} table is not exist")
        return None
    elif stockCustomData is None:
        print(f"{name} table is not exist")
        return None
    else:
        # stockData = {"Close":stockCustomData[4],"Open":stockCustomData[1],"High":stockCustomData[2],"Low":stockCustomData[3],"Volume":stockCustomData[6]}
        stockData = pd.DataFrame(
            {
                "Close": stockCustomData.loc[0:, "Close"],
                "Open": stockCustomData.loc[0:, "Open"],
                "High": stockCustomData.loc[0:, "High"],
                "Low": stockCustomData.loc[0:, "Low"],
                "Volume": stockCustomData.loc[0:, "Volume"],
            }
        )
        Chipsconcentrations = 1  # 筹码集中度，算法未处理，暂时为1
        saveTime = datetime.strptime(
            date_part + " " + time_part, "%Y-%m-%d %H:%M:%S"
        ).time()
        datas = [
            saveTime,
            stockTimeData[0],
            stockTimeData[1],
            stockTimeData[6],
            stockTimeData[7],
            Chipsconcentrations,
        ]
        return stockData, datas


# 股票各因素检测
def startQuantifytest(stockNum, now, enginstr, ma=20):
    formatted = now.strftime("%Y-%m-%d %H:%M:%S")
    date_part, time_part = formatted.split(" ")
    # base_time_part = "00:00:00"
    if now.time() >= time(15, 0, 0):
        time_part = "15:00:00"
    name = data_processor.GetDataFromSql("代码库", "代码", "名称", stockNum, enginstr)
    if name == "":
        html.getStocksTime(stockNum, now, enginstr)
        name = data_processor.GetDataFromSql("代码库", "代码", "名称", stockNum, enginstr)
    timename = name + "分时"
    result = getStockTimeData(date_part, time_part, name, enginstr, timename)
    if result is None:
        return
    else:
        stockData, datas = result
        stock_instance = Stock(stockData, datas)
        # 获取某个股票的检测结果
        final = stock_instance.get_final_result(ma)
        if final is True:
            print(f"{name}检测结果为:{final},满足趋势向上放量反包")
        # else:
        #     print(f"{name}检测结果为:{final},未满足条件")


# 检测全局5000支股票，提取满足要求股票
def check_total_stocks(now, table, value, start, end, enginstr):
    # todo 获取全局股票代码
    # todo 利用第三方接口获取每个股票制定开启关闭时间
    # await _check_total_stocks(now, table, value, start, enginstr)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            _check_total_stocks(now, table, value, start, end, enginstr)
        )
    finally:
        loop.close()


async def _check_total_stocks(now, table, value, start, end, enginstr):
    global check
    if check:
        return
    check = True
    formatted = now.strftime("%Y-%m-%d %H:%M:%S")
    date_part, time_part = formatted.split(" ")
    # 获取日级别数据
    stockdatas = await html.checkAllStock(table, value, start, end, enginstr)
    # await html.checkAllTimeStock()
    # print(f"{stockdatas},get stocks")
    index = 0
    # rowDatas = []
    saveTime = datetime.strptime(
        date_part + " " + time_part, "%Y-%m-%d %H:%M:%S"
    ).time()
    for stockData in stockdatas:
        if index >= 1:
            break
        # 某一个股票的单位时间内的所有数据
        # for date, row in data.iterrows():
        #     saveTime = datetime.strptime(
        #         date_part + " " + time_part, "%Y-%m-%d %H:%M:%S"
        #     ).time()
        #     open_value = row["Open"]
        #     high_value = row["High"]
        #     low_value = row["Low"]
        #     close_value = row["Close"]
        #     adj_close_value = row["Adj Close"]
        #     volume_value = row["Volume"]
        #     rowDatas.append(
        #         [
        #             date,
        #             open_value,
        #             high_value,
        #             low_value,
        #             close_value,
        #             adj_close_value,
        #             volume_value,
        #         ]
        #     )
        # 获取分时级别数据
        stockNum = stockData["代码"].tolist()[0]
        # 分时数据
        headers, datas, name = await html.checkAllTimeStock(stockNum)
        # stockData = pd.DataFrame(
        #     rowDatas,
        #     columns=["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"],
        # )
        _datas = [
            saveTime,  # 数据获取时间
            datas[0],  # 当前价格
            datas[1],  # 换手率
            datas[6],  # 量比
            datas[7],  # 分时均价
            1,  # 筹码集中度
        ]
        stock_instance = Stock(stockData, _datas)
        day = 20
        final = stock_instance.get_final_result(day)
        if final is True:
            print(f"{name}检测结果为:{final},满足趋势向上放量反包")
        index += 1
    print("complete")
    # 利用均线来判断逻辑
