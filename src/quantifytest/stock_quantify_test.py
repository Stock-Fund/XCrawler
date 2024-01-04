import src.data_processor as data_processor
import src.html as html
from algorithm.stock import Stock
from datetime import datetime, time
import pandas as pd


def startQuantifytest(stockNum, now, enginstr):
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
    # 某只股票所有的第三方数据
    stockCustomData = data_processor.GetAllDataFromTable(name, enginstr)
    # 某一天的第三方数据
    # value = date_part + " " + base_time_part
    # stockCustomData = data_processor.GetDatasFromSql1(name, "Date", value, enginstr)
    stockTimeData = data_processor.GetDatasFromSql2(
        timename,
        {"id": "日期", "value": date_part},
        {"id": "时间", "value": time_part},
        enginstr,
    )

    if stockTimeData is None:
        print(f"{timename} table is not exist")
    elif stockCustomData is None:
        print(f"{name} table is not exist")
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
        Chipsconcentrations = 1  # 算法未处理
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
        stock_instance = Stock(stockData, datas)
        # 现有逻辑简单判断
        day = 10
        netVolume = stock_instance.checkNetVolumes(day)
        volumeStr = f"成交量:{netVolume} 成交量为正" if netVolume > 0 else f"成交量:{netVolume} 成交量为负"
        print(f"{name} 最近{day}日 {volumeStr}")
    # print(f'{stock_instance.checkVolums()}')
    # if stock_instance.checkVolums() >= 1:
    #     print("放量反包上涨")
    # if stock_instance.get_slope(5) > 0 and stock_instance.get_slope(10) > 0:
    #     print(f'{stock_instance.get_slope(5)} {stock_instance.get_slope(10)}')
    #     if stock_instance.checkVolums() > 0.5:
    #         print(f'{stock_instance.checkVolums()}')
    #         days = stock_instance.check_close_near_ma(2)
    #         if len(days) > 0:
    #             for day in days:
    #                 print(f'{day}')
    #                 print(f"{name}可以买入")
