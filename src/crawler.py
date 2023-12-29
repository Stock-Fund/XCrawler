from multiprocessing import Process
import src.html as html
import src.quantifytest as quantifytest
import time
import schedule
import threading
import datetime

enginstr = "mysql+pymysql://root:Akeboshi123~@localhost:3306/stock"

done = threading.Event()


def _runProcess(check):
    stocks = [
        # "603721",
        # "600036",
        # "600895",
        # "603178",
        # "603189",
        # "600678",
        # "600355",
        # "603025",
        # "600661",
        # "603536",
        # "603660",
        # "600765",
        # "002555",
        # "603906",
        # "002466",
        "601166"
    ]
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
            for stock in stocks:
                _p = Process(
                    target=quantifytest.startQuantifytest,
                    args=(
                        stock,
                        now,
                        enginstr,
                    ),
                )
                _p.daemon = True
                _p.start()
                _p.join(30)
        else:
            # 开市时间做数据存储
            # 股票分时数据
            for stock in stocks:
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
            for stock in stocks:
                _p = Process(
                    target=html.getStockData_datareader,
                    args=(
                        stock,
                        now,
                        enginstr,
                        check,
                    ),
                )
                _p.daemon = True
                _p.start()
                _p.join(30)
    else:
        # 开市时间做数据存储
        # 股票分时数据
        for stock in stocks:
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
        for stock in stocks:
            _p = Process(
                target=html.getStockData_datareader,
                args=(
                    stock,
                    now,
                    enginstr,
                    check,
                ),
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


def run_forever(polling, check=False):
    if polling:
        schedule.every().day.at("15:00").do(lambda: _runProcess(check))
        while not done.is_set():
            # localtime = src.timeutil.get_local_time()
            # 每天15:00遍历一次网页的数据
            schedule.run_pending()
            time.sleep(1)
    else:
        _runProcess(check)


def try_start():
    thread = threading.Thread(target=run_forever, args=(True,), daemon=True)
    thread.start()


def start():
    run_forever(False)


def getAllStock():
    html.getAllStock(enginstr)


def find(stockNum):
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
        args=(
            f"{stockNum}",
            now,
            enginstr,
            check
        ),
    )
    p1.daemon = True
    p1.start()
    print(f"查找对应代码{stockNum}股票")


def showStockData(stockNum):
    html.showStockData(stockNum, enginstr)


def check():
    run_forever(False, True)
