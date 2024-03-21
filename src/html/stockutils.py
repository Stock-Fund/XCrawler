from enum import Enum


# 股票的工具类
class StockType(Enum):
    SH_A = "上海A股"
    SH_B = "上海B股"
    SZ_A = "深圳A股"
    SZ_B = "深圳B股"
    CHUANGYEBAN = "创业板"
    ETF = "ETF基金"
    UNKNOWN = "未知类型"


def stockcheck(stockNum):
    if stockNum.startswith("00"):
        return StockType.SZ_A
    elif stockNum.startswith("200"):
        return StockType.SZ_B
    elif stockNum.startswith("300"):
        return StockType.CHUANGYEBAN
    elif stockNum.startswith("301"):
        return StockType.CHUANGYEBAN
    elif stockNum.startswith("60"):
        return StockType.SH_A
    elif stockNum.startswith("900"):
        return StockType.SH_B
    elif (
        stockNum.startswith("15")  # 深市上市
        or stockNum.startswith("51")  # 沪市上市
        or stockNum.startswith("58")  # 沪市上市 双创基金
    ):
        return StockType.ETF
    else:
        return StockType.UNKNOWN


def getStockTimeUrl(stockNum):
    stockType = stockcheck(stockNum)
    if stockType == StockType.SH_A or stockType == StockType.SH_B:
        return f"http://quote.eastmoney.com/sh{stockNum}.html"
    elif (
        stockType == StockType.SZ_A
        or stockType == StockType.SZ_B
        or stockType == StockType.CHUANGYEBAN
    ):
        return f"http://quote.eastmoney.com/sz{stockNum}.html"
    elif stockType == StockType.ETF:
        return ""


# 获取股票资金流入流出数据地址
def get_StockInflow_OutflowUrl(stockNum):
    stockType = stockcheck(stockNum)
    if stockType == StockType.ETF:
        return ""
    return f"http://data.eastmoney.com/zjlx/{stockNum}.html"


# 获取股票筹码数据地址
def get_Stock_chipsUrl(stockNum):
    stockType = stockcheck(stockNum)
    if stockType == StockType.SH_A:
        return f"http://quote.eastmoney.com/concept/sh{stockNum}.html#chart-k-cyq"
    elif (
        stockType == StockType.SZ_A
        or stockType == StockType.SZ_B
        or stockType == StockType.CHUANGYEBAN
    ):
        return f"http://quote.eastmoney.com/concept/sz{stockNum}.html#chart-k-cyq"
    elif stockType == StockType.ETF:
        return ""


def getStockSuffix(stockNum):
    stockType = stockcheck(stockNum)
    if stockType == StockType.SH_A or stockType == StockType.SH_B:
        return ".ss"
    elif (
        stockType == StockType.SZ_A
        or stockType == StockType.SZ_B
        or stockType == StockType.CHUANGYEBAN
    ):
        return ".sz"
    else:
        return ""


def checkGem(stockNum):
    if stockcheck(stockNum) == StockType.CHUANGYEBAN:
        return True
    else:
        return False
