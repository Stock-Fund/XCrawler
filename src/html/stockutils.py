from enum import Enum


# 股票的工具类
class StockType(Enum):
    SH_A = "上海A股"
    SH_B = "上海B股"
    SZ_A = "深圳A股"
    SZ_B = "深圳B股"
    CHUANGYEBAN = "创业板"
    UNKNOWN = "未知类型"


def stockcheck(stockNum):
    if stockNum.startswith("00"):
        return StockType.SZ_A
    elif stockNum.startswith("200"):
        return StockType.SZ_B
    elif stockNum.startswith("300"):
        return StockType.CHUANGYEBAN
    elif stockNum.startswith("60"):
        return StockType.SH_A
    elif stockNum.startswith("900"):
        return StockType.SH_B
    else:
        return StockType.UNKNOWN


def getStockTimeUrl(stockNum):
    stockType = stockcheck(stockNum)
    if stockType == StockType.SH_A or stockType == StockType.SH_B:
        return f"http://quote.eastmoney.com/sh{stockNum}.html"
    elif stockType == StockType.SZ_A or stockType == StockType.SZ_B:
        return f"http://quote.eastmoney.com/sz{stockNum}.html"


def getStockSuffix(stockNum):
    stockType = stockcheck(stockNum)
    if stockType == StockType.SH_A or stockType == StockType.SH_B:
        return ".ss"
    elif stockType == StockType.SZ_A or stockType == StockType.SZ_B:
        return ".sz"
