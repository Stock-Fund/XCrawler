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
def check_total_stocks(now, table, value, start, end_single, end_total, enginstr):
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            _check_total_stocks(
                now, table, value, start, end_single, end_total, enginstr
            )
        )
    finally:
        loop.close()


async def _check_total_stocks(
    now, table, value, start, end_single, end_total, enginstr
):
    global check
    if check:
        return
    check = True
    formatted = now.strftime("%Y-%m-%d %H:%M:%S")
    date_part, time_part = formatted.split(" ")
    # 获取日级别数据
    stockdatas = await html.checkAllStock(
        table, value, start, end_single, end_total, enginstr
    )
    index = 0
    saveTime = datetime.strptime(
        date_part + " " + time_part, "%Y-%m-%d %H:%M:%S"
    ).time()
    for stockData in stockdatas:
        # 获取分时级别数据
        stockNum = stockData["代码"].tolist()[0]
        # 分时数据
        headers, datas, name = await html.checkAllTimeStock(stockNum)
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
            # 加入乖离率来判断该股票是否存在超卖/超买情况，并以此作标准来判断是否可以关注
            print(f"{name}检测结果为:{final},满足趋势向上放量反包")
            bias_rate = stock_instance.get_over_trade(day)
            if bias_rate == 1:
                index += 1
                print(f"{name}{day}检测结果为:超卖")
            elif bias_rate == -1:
                # 排除超买情况
                print(f"{name}{day}检测结果为:超买")
            elif bias_rate == 0:
                index += 1
                print(f"{name}{day}检测结果为:震荡区间")
        else:
            print(f"{name}检测结果为:{final},不满足放量反包条件")
    print("complete")
