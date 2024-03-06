from multiprocessing import Process
import src.html as html
import src.quantifytest as quantifytest
import time
import schedule
import threading
import datetime

enginstr = "mysql+pymysql://gxm:password@localhost:3306/stock"
stocks = [
    "000938",
    "002466",
    "002460",
    "603888",
    "600036",
    "603019",
    "601136",
    "002229",
    "603666",
    "301138",
    "002673",
    "601611",
    "600745",
    "000777"
    
]
done = threading.Event()


def _runProcess(check, _stocks, ma, start):
    now = datetime.datetime.now()
    if check:
        # 收盘时间
        target_time1 = datetime.time(11, 30)
        target_time2 = datetime.time(15, 00)
        target_time3 = datetime.time(13, 00)
        # 大于三点做买入卖出逻辑判断
        if now.time() > target_time2 or (
            now.time() < target_time3 and now.time() >= target_time1
        ):
            # 直接从数据库获取数据
            for stock in _stocks:
                _p = Process(
                    target=quantifytest.startQuantifytest,
                    args=(stock, now, start, enginstr, ma),
                )
                _p.daemon = True
                _p.start()
                _p.join(30)
        else:
            # 开市时间做数据存储
            # 股票分时数据
            for stock in _stocks:
                _p = Process(
                    target=html.getStocksTime,
                    args=(
                        stock,
                        now,
                        enginstr,
                    ),
                )
                _p.daemon = True
                _p.start()
                _p.join(30)

            # 股票收盘开盘量比等数据
            for stock in _stocks:
                _p = Process(
                    target=html.getStockData_datareader,
                    args=(stock, now, start, enginstr, check, ma),
                )
                _p.daemon = True
                _p.start()
                _p.join(30)
    else:
        # 开市时间做数据存储
        # 股票分时数据
        for stock in _stocks:
            _p = Process(
                target=html.getStocksTime,
                args=(
                    stock,
                    now,
                    enginstr,
                ),
            )
            _p.daemon = True
            _p.start()
            _p.join(30)

        # 股票收盘开盘量比等数据
        for stock in _stocks:
            _p = Process(
                target=html.getStockData_datareader,
                args=(stock, now, start, enginstr, check, ma),
            )
            _p.daemon = True
            _p.start()
            _p.join(30)

        # 主板
        p = Process(
            target=html.getSHBoard,
            args=(
                "http://quote.eastmoney.com/center/gridlist.html#sh_a_board",
                enginstr,
            ),
        )
        p.daemon = True
        p.start()

    done.set()


def run_forever(polling, _stocks, ma=5, start=None, check=False):
    if polling:
        schedule.every().day.at("15:00").do(
            lambda: _runProcess(check, _stocks, ma, now)
        )
        while not done.is_set():
            # localtime = src.timeutil.get_local_time()
            # 每天15:00遍历一次网页的数据
            schedule.run_pending()
            time.sleep(1)
    else:
        _runProcess(check, _stocks, ma, start)


def try_start():
    thread = threading.Thread(
        target=run_forever,
        args=(
            True,
            stocks,
        ),
        daemon=True,
    )
    thread.start()


def start():
    run_forever(False, stocks)


def getAllStock():
    html.getAllStock(enginstr)


def find(stockNum, ma=5):
    now = datetime.datetime.now()
    check = True
    p = Process(
        target=html.getStocksTime,
        args=(
            f"{stockNum}",
            now,
            enginstr,
        ),
    )
    p.daemon = True
    p.start()

    p1 = Process(
        target=html.getStockData_datareader,
        args=(f"{stockNum}", now, None, enginstr, check, ma),
    )
    p1.daemon = True
    p1.start()
    print(f"查找对应代码{stockNum}股票")


def showStockData(stockNum):
    html.showStockData(stockNum, enginstr)


def check(customstocks=None, ma=5, start=None):
    if not customstocks:
        customstocks = stocks
    run_forever(False, customstocks, ma, start, True)


def filter():
    print("开始全局筛选")
    now = datetime.datetime.now()
    quantifytest.check_total_stocks(
        now,
        "2024-01-29-allstock",
        "代码",
        "2024-01-28",
        "2024-01-29",
        "2024-01-29",
        enginstr,
    )


def getMarginAllData():
    now = datetime.datetime.now()
    html.getmargindata("https://data.eastmoney.com/rzrq/detail/all.html", now, enginstr)
