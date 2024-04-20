from multiprocessing import Process
import src.html as html
import src.quantifytest as quantifytest
import time
import schedule
import threading
import datetime
import src.cProfile_test
import src.util.infoutil as info

enginstr = "mysql+pymysql://gxm:password@localhost:3306/stock"
stocks = ["300552", "300496", "000628","603019","000911"]  # "300552", "300496", "000628",
done = threading.Event()

FUNCTION_MAP = {
    "html.getStocksTime": html.getStocksTime,
    "html.getStockInflowOutflow": html.getStockInflowOutflow,
    "html.getStockChips": html.getStockChips,
    "html.getStockData_datareader": html.getStockData_datareader,
    "quantifytest.startQuantifytest": quantifytest.startQuantifytest,
}

def run_stock_process(target, stocks, now, enginStr, start=None, check=None, ma=None):
    func = FUNCTION_MAP[target]
    for stock in stocks:
        args = (stock, now, enginStr)
        if target == "quantifytest.startQuantifytest":
            args = (stock, now, start, enginStr, ma)
        elif target == "html.getStockData_datareader":
            args = (stock, now, start, enginStr, check, ma)
        _p = Process(target=func, args=args)
        _p.daemon = True
        _p.start()
        _p.join(30)


def _runProcess(key,token,pushover,check, _stocks, ma, start):
    now = datetime.datetime.now()
    # 收盘时间
    target_time1 = datetime.time(11, 30)
    target_time2 = datetime.time(15, 00)
    target_time3 = datetime.time(13, 00)
    # 大于三点做买入卖出逻辑判断
    if check and (
        now.time() > target_time2
        or (now.time() < target_time3 and now.time() >= target_time1)
    ):
        run_stock_process(
            "quantifytest.startQuantifytest", _stocks, now, enginstr, start, ma
        )
    else:
        run_stock_process("html.getStocksTime", _stocks, now, enginstr)
        run_stock_process("html.getStockInflowOutflow", _stocks, now, enginstr)
        run_stock_process("html.getStockChips", _stocks, now, enginstr)
        run_stock_process(
            "html.getStockData_datareader", _stocks, now, enginstr, start, check, ma
        )
        if not check:
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
            p.join(30)
    message = info.get_total_info()
    pushover(key,token,"股票数据获取取完成")
    done.set()


# def _runProcess(check, _stocks, ma, start):
#     now = datetime.datetime.now()
#     if check:
#         # 收盘时间
#         target_time1 = datetime.time(11, 30)
#         target_time2 = datetime.time(15, 00)
#         target_time3 = datetime.time(13, 00)
#         # 大于三点做买入卖出逻辑判断
#         if now.time() > target_time2 or (
#             now.time() < target_time3 and now.time() >= target_time1
#         ):
#             # 直接从数据库获取数据
#             for stock in _stocks:
#                 _p = Process(
#                     target=quantifytest.startQuantifytest,
#                     args=(stock, now, start, enginstr, ma),
#                 )
#                 _p.daemon = True
#                 _p.start()
#                 _p.join(30)
#         else:
#             # 开市时间做数据存储
#             # 股票分时数据
#             for stock in _stocks:
#                 _p = Process(
#                     target=html.getStocksTime,
#                     args=(
#                         stock,
#                         now,
#                         enginstr,
#                     ),
#                 )
#                 _p.daemon = True
#                 _p.start()
#                 _p.join(30)

#             # 获取股票的资金流入流出数据
#             for stock in _stocks:
#                 _p = Process(
#                     target=html.getStockInflowOutflow,
#                     args=(stock, now, enginstr),
#                 )
#                 _p.daemon = True
#                 _p.start()
#                 _p.join(30)

#             # 获取股票的筹码数据
#             for stock in _stocks:
#                 _p = Process(
#                     target=html.getStockChips,
#                     args=(stock, now, enginstr),
#                 )
#                 _p.daemon = True
#                 _p.start()
#                 _p.join(30)

#             # 获取股票第三方数据
#             for stock in _stocks:
#                 _p = Process(
#                     target=html.getStockData_datareader,
#                     args=(stock, now, start, enginstr, check, ma),
#                 )
#                 _p.daemon = True
#                 _p.start()
#                 _p.join(30)
#     else:
#         # 开市时间做数据存储
#         # 股票分时数据
#         for stock in _stocks:
#             _p = Process(
#                 target=html.getStocksTime,
#                 args=(
#                     stock,
#                     now,
#                     enginstr,
#                 ),
#             )
#             _p.daemon = True
#             _p.start()
#             _p.join(30)

#         # 获取股票的资金流入流出数据
#         for stock in _stocks:
#             _p = Process(
#                 target=html.getStockInflowOutflow,
#                 args=(stock, now, enginstr),
#             )
#             _p.daemon = True
#             _p.start()
#             _p.join(30)

#         # 获取股票的筹码数据
#         for stock in _stocks:
#             _p = Process(
#                 target=html.getStockChips,
#                 args=(stock, now, enginstr),
#             )
#             _p.daemon = True
#             _p.start()
#             _p.join(30)

#         # 获取股票第三方数据
#         for stock in _stocks:
#             _p = Process(
#                 target=html.getStockData_datareader,
#                 args=(stock, now, start, enginstr, check, ma),
#             )
#             _p.daemon = True
#             _p.start()
#             _p.join(30)

#         # 主板
#         p = Process(
#             target=html.getSHBoard,
#             args=(
#                 "http://quote.eastmoney.com/center/gridlist.html#sh_a_board",
#                 enginstr,
#             ),
#         )
#         p.daemon = True
#         p.start()

#     done.set()


def run_forever(key,token,pushover,polling, _stocks, ma=5, start=None, check=False):
    if polling:
        schedule.every().day.at("15:00").do(
            lambda: _runProcess(key,token,pushover,check, _stocks, ma, start)
        )
        while not done.is_set():
            # localtime = src.timeutil.get_local_time()
            # 每天15:00遍历一次网页的数据
            schedule.run_pending()
            time.sleep(1)
    else:
        _runProcess(key,token,pushover,check, _stocks, ma, start)


def try_start(key,token,pushover):
    thread = threading.Thread(
        target=run_forever,
        args=(
            key,
            token,
            pushover,
            True,
            stocks,
        ),
        daemon=True,
    )
    thread.start()

def start(key,token,pushover):
    src.cProfile_test.cProfile_test(run_forever,key,token,pushover,False,stocks)
    # run_forever(False, stocks)


def getAllStock(key,token,pushover):
    html.getAllStock(key,token,pushover,enginstr)


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
        target=html.getStockInflowOutflow,
        args=(f"{stockNum}", now, enginstr),
    )
    p1.daemon = True
    p1.start()

    p2 = Process(
        target=html.getStockChips,
        args=(f"{stockNum}", now, enginstr),
    )
    p2.daemon = True
    p2.start()

    p3 = Process(
        target=html.getStockData_datareader,
        args=(f"{stockNum}", now, None, enginstr, check, ma),
    )
    p3.daemon = True
    p3.start()

    print(f"查找对应代码{stockNum}股票")


def showStockData(stockNum):
    html.showStockData(stockNum, enginstr)


def check(key,token,pushover,customstocks=None, ma=5, start=None):
    if not customstocks:
        customstocks = stocks
    run_forever(key,token,pushover,False, customstocks, ma, start, True)


def filter(key,token,notification):
    print("开始全局筛选")
    now = datetime.datetime.now()
    quantifytest.check_total_stocks(
        key,token,notification,
        now,
        "2024-03-22-allstock",
        "代码",
        "2024-03-12",
        "2024-03-22",
        "2024-03-22",
        enginstr,
    )


def getMarginAllData(key,token,notification):
    now = datetime.datetime.now()
    html.getmargindata(key,token,notification,"https://data.eastmoney.com/rzrq/detail/all.html", now, enginstr)
