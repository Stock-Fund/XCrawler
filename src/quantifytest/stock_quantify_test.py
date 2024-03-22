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
num_simulations = 10000


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
        table = name + "历史资金统计"
        stockInflow_OutflowData = data_processor.GetAllStockCode(
            table, "主力净额", enginstr
        )
        chipname = name + "筹码情况"
        Chips90concentrations = data_processor.GetAllStockCode(
            chipname, "90%集中度:", enginstr
        )  # 获取90筹码集中度数组的最新情况
        Chips90Prices = data_processor.GetAllStockCode(chipname, "90%成本:", enginstr)
        Profitratios = data_processor.GetAllStockCode(chipname, "获利比例:", enginstr)
        ChipAverageValues = data_processor.GetAllStockCode(
            chipname, "平均成本:", enginstr
        )
        stockData = stockCustomData
        saveTime = datetime.strptime(
            date_part + " " + time_part, "%Y-%m-%d %H:%M:%S"
        ).time()
        datas = [
            saveTime,
            stockTimeData,
            stockInflow_OutflowData,
            Chips90concentrations,
            Chips90Prices,
            Profitratios,
            ChipAverageValues,
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
        name = data_processor.GetDataFromSql(
            "代码库", "代码", "名称", stockNum, enginstr
        )
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
    day = 20
    simulated_prices = stock_instance.monte_carlo_simulation(num_simulations)
    if final is True:
        print(f"{name}检测结果为:{final},满足趋势向上放量反包")
        bias_rate = stock_instance.get_over_trade(day)
        if bias_rate >= 1:
            print(f"{name}{day}检测结果为:超卖")
        elif bias_rate <= -1:
            # 排除超买情况
            print(f"{name}{day}检测结果为:超买")
        elif bias_rate > 1 and bias_rate < -1:
            print(f"{name}{day}检测结果为:震荡区间")
    else:
        print(f"{name}检测结果为:{final},观望为主")
    macd, macd_signal, macd_hist = stock_instance.get_MACD()

    ma5 = stock_instance.getMA(5)
    ma10 = stock_instance.getMA(10)
    ma20 = stock_instance.getMA(20)
    ma30 = stock_instance.getMA(30)
    ma40 = stock_instance.getMA(40)
    ma60 = stock_instance.getMA(60)

    df = stock_instance.calculate_kdj()

    weekClose = stock_instance.get_weekClose
    mouthClose = stock_instance.get_mouthClose
    # print(f"{weekClose},{mouthClose}")
    buy = stock_instance.StockBuy()
    buy_short = stock_instance.StockBuy_short()
    sell_short = stock_instance.StockSell_short()
    day = 25
    flow = stock_instance.checkFlow(day)
    print(f"{name},{day}日内资金情况为{flow}")

    volum = stock_instance.checkVolumLogic()
    print(f"{name}, 成就量判断后市为{volum}")
    # if buy_short is False:
    #     print("非短期买入区间")
    # else:
    #     print("短期可买入区间")

    # if sell_short is False:
    #     print("非短期卖出区间")
    # else:
    #     print("短期可卖出区间")

    # if buy is False:
    #     print("非买入区间")
    # else:
    #     print("可买入区间")
    weekly_close = ma5
    monthly_close = ma30
    weekly_macd, weekly_signal, weekly_hist = ta.MACD(
        weekly_close, fastperiod=5, slowperiod=10, signalperiod=9
    )
    monthly_macd, monthly_signal, mouthly_hist = ta.MACD(
        monthly_close, fastperiod=20, slowperiod=30, signalperiod=9
    )
    # 绘制MACD图像
    plt.figure(figsize=(20, 6))
    plt.subplot(4, 1, 1)  # 创建第一个子图
    plt.plot(macd, label="Daily MACD")
    plt.plot(macd_signal, label="MACD Daily Signal Line")
    plt.bar(range(len(macd_hist)), macd_hist, label="Daily Histogram")

    # 将NaN值替换为0
    macd_hist = np.nan_to_num(macd_hist)

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
    plt.subplot(4, 1, 2)  # 创建第二个子图
    plt.plot(closeValues, label="Close Prices")
    plt.plot(ma5, label="MA5")
    # 添加图例和标签
    plt.legend()
    plt.title("Moving Averages")
    plt.xlabel("Period")
    plt.ylabel("Price")

    weekly_signal = np.nan_to_num(weekly_signal)
    monthly_signal = np.nan_to_num(monthly_signal)
    # annual_signal = np.nan_to_num(annual_signal)
    plt.subplot(4, 1, 3)
    plt.plot(weekly_macd, label="Weekly MACD")
    plt.plot(weekly_signal, label="Weekly Signal")
    plt.bar(range(len(weekly_hist)), weekly_hist, label="Week Histogram")
    plt.title("Weekly MACD")
    plt.legend()

    plt.subplot(4, 1, 4)
    plt.plot(monthly_macd, label="Monthly MACD")
    plt.plot(monthly_signal, label="Monthly Signal")
    plt.bar(range(len(mouthly_hist)), mouthly_hist, label="Mouth Histogram")
    plt.title("Monthly MACD")
    plt.legend()

    plt.figure(figsize=(10, 6))
    plt.plot(simulated_prices.T, alpha=0.1)
    plt.title("Monte Carlo Simulation for {}".format(stockNum))
    plt.xlabel("Days")
    plt.ylabel("Price")

    # 绘制KDJ图表
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df["k"], label="K")
    plt.plot(df.index, df["d"], label="D")
    plt.plot(df.index, df["j"], label="J")
    plt.legend()
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.title("KDJ Indicator")
    plt.xticks(rotation=45)
    plt.grid(True)

    plt.tight_layout()  # 自动调整子图的布局
    # 展示图表
    plt.show()
    # plt.subplot(5, 1, 5)
    # plt.plot(annual_macd, label="Annual MACD")
    # plt.plot(annual_signal, label="Annual Signal")
    # plt.title("Annual MACD")
    # plt.legend()
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
        if index > 20:
            break
        # 获取分时级别数据
        stockNum = stockData["代码"].tolist()[0]
        # 分时数据
        headers, datas, name = await html.checkAllTimeStock(stockNum)
        table = name + "历史资金统计"
        stockInflow_OutflowData = data_processor.GetAllStockCode(
            table, "主力净额", enginstr
        )
        chipname = name + "筹码情况"
        Chips90concentrations = data_processor.GetAllStockCode(
            chipname, "90%集中度:", enginstr
        )  # 获取90筹码集中度数组的最新情况
        Chips90Prices = data_processor.GetAllStockCode(chipname, "90%成本:", enginstr)
        Profitratios = data_processor.GetAllStockCode(chipname, "获利比例:", enginstr)
        ChipAverageValues = data_processor.GetAllStockCode(
            chipname, "平均成本:", enginstr
        )
        _datas = [
            saveTime,  # 数据获取时间
            datas,
            stockInflow_OutflowData,
            Chips90concentrations,  # 90筹码集中度
            Chips90Prices,  # 90筹码成本
            Profitratios,  # 筹码盈利比例
            ChipAverageValues,  # 筹码均价
            stockNum,
            name,
        ]
        stock_instance = Stock(stockData, _datas)
        day = 20
        final = stock_instance.get_final_result(day)
        short = stock_instance.get_short_result()
        if short is True:
            print(f"{name}检测结果为:{short},短期情绪高涨")
        if final is True:
            # 加入乖离率来判断该股票是否存在超卖/超买情况，并以此作标准来判断是否可以关注
            print(f"{name}检测结果为:{final},满足趋势向上放量反包")
            bias_rate = stock_instance.get_over_trade(day)
            if bias_rate >= 1:
                index += 1
                print(f"{name}{day}检测结果为:超卖")
            elif bias_rate <= -1:
                # 排除超买情况
                print(f"{name}{day}检测结果为:超买")
            elif bias_rate > 1 and bias_rate < -1:
                index += 1
                print(f"{name}{day}检测结果为:震荡区间")
        else:
            print(f"{name}检测结果为:{final},不满足放量反包条件")
    print("complete")
