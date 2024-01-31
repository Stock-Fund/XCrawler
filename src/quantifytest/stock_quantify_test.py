import src.data_processor as data_processor
import src.html as html
from algorithm.stock import Stock
from datetime import datetime, time
import pandas as pd
import asyncio
import matplotlib.pyplot as plt
import talib as ta
import numpy as np

check = False


def getStockTimeData(
    date_part, time_part, start, end, name, enginstr, timename, stockNum
):
    # 某只股票所有的第三方数据
    stockCustomData = data_processor.GetAllDataFromTable(name, enginstr, start, end)
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
                # 记录股票数据的时间范围
                "Date": stockCustomData.loc[0, "Date"],
            }
        )

        # stockCustomData["Date"] = pd.to_datetime(stockCustomData["Date"])
        # # 将"Date"列设置为索引
        # stockCustomData.set_index("Date", inplace=True)
        # day1 = stockCustomData.index[0]
        # day2 = stockCustomData.index[-1]
        # print(f"开始时间：{day1}")
        # print(f"结束时间：{day2}")

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
            stockNum,
            name,
        ]
        return stockData, datas


def get_stock(stockNum, now, start, enginstr, ma=20):
    formatted = now.strftime("%Y-%m-%d %H:%M:%S")
    formatted_start = start
    date_part, time_part = formatted.split(" ")
    # base_time_part = "00:00:00"
    if now.time() >= time(15, 0, 0):
        time_part = "15:00:00"
    name = data_processor.GetDataFromSql("代码库", "代码", "名称", stockNum, enginstr)
    if name == "":
        print(f"get_stock {stockNum}")
        html.getStocksTime(stockNum, now, enginstr)
        name = data_processor.GetDataFromSql("代码库", "代码", "名称", stockNum, enginstr)
    timename = name + "分时"
    result = getStockTimeData(
        date_part, time_part, start, "", name, enginstr, timename, stockNum
    )
    if result is None:
        return None
    else:
        stockData, datas = result
        stock_instance = Stock(stockData, datas)
        return stock_instance


# 股票各因素检测
def startQuantifytest(stockNum, now, start, enginstr, ma=20):
    stock_instance = get_stock(stockNum, now, start, enginstr, ma)
    if stock_instance is None:
        return
    # 获取某个股票的检测结果
    final = stock_instance.get_final_result(ma)
    name = stock_instance.get_Name
    if final is True:
        print(f"{name}检测结果为:{final},满足趋势向上放量反包")
    else:
        print(f"{name}检测结果为:{final},观望为主")
    macd, macd_signal, macd_hist = stock_instance.get_MACD()
    # 绘制MACD图像
    plt.figure(figsize=(20, 6))
    plt.subplot(2, 1, 1)  # 创建第一个子图
    plt.plot(macd, label="MACD")
    plt.plot(macd_signal, label="MACD Signal Line")
    plt.bar(range(len(macd_hist)), macd_hist, label="Histogram")

    # 将NaN值替换为0
    macd_hist = np.nan_to_num(macd_hist)
    print(macd_hist)

    # 指定横轴刻度
    plt.xticks(range(len(macd_hist)), [str(i + 1) for i in range(len(macd_hist))])

    # 计算纵轴刻度位置和标签
    max_hist = max(macd_hist)
    min_hist = min(macd_hist)
    hist_range = max_hist - min_hist
    # 计算纵轴刻度位置
    yticks = [min_hist, min_hist + hist_range / 2, max_hist]
    # 计算纵轴刻度标签
    ytick_labels = [
        f"{min_hist:.2f}",
        f"{(min_hist + hist_range/2):.2f}",
        f"{max_hist:.2f}",
    ]
    # 指定纵轴刻度
    plt.yticks(yticks, ytick_labels)
    # 设置图表标题和标签
    plt.title("MACD Indicator")
    plt.xlabel("Day")
    plt.ylabel("MACD")

    # 绘制ma均线图
    closeValues = stock_instance.get_Close_Values
    ma5 = stock_instance.getMA(5)
    plt.subplot(2, 1, 2)  # 创建第二个子图
    plt.plot(closeValues, label="Close Prices")
    plt.plot(ma5, label="MA5")
    # 添加图例和标签
    plt.legend()
    plt.title("Moving Averages")
    plt.xlabel("Period")
    plt.ylabel("Price")

    plt.tight_layout()  # 自动调整子图的布局
    # 展示图表
    plt.show()
    # todo 周，月，年macd图 及 红柱区域

    # else:
    # print(f"{name}检测结果为:{final},未满足条件")


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
            stockNum,
            name,
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
