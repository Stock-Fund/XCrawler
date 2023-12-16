import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
## 拟合

## 0-60日收盘价简单拟合
def simple_fit(days, closeprices):
    lr = LinearRegression().fit(days, closeprices)
    # 返回斜率
    return lr.coef_[0]
## rsrs拟合
N_near = 18  # 计算最新斜率 slope，拟合度 r2 参考最近 N 天,一般是最近18天
M_norm = 600  # 计算最新标准分 zscore，rsrs_score 参考最近 M 天,一般通过最近600日的数据进行归一化
score_threshold = 0.7  # rsrs 标准分指标阈值

# 对输入的自变量每日最低价x和因变量每日最高价y,建立 OLS 回归模型,返回斜率,截距
def ols_fitting(x, y):
    x = np.array(x)
    y = np.array(y)
    res = np.polyfit(x, y, 1)  # 一阶线性拟合
    slope, intercept = res[0], res[1]

    return slope, intercept

# 通过前 M_norm 日最高最低价的线性回归计算斜率,返回斜率的列表，主要的作用是为了之后的归一化
def M_day_slope(stockNum,low,high):
    # low,high分别为N天内的最低价和最高价列表
    res = []
    # 选择M个斜率，每个斜率的值为N的OLS回归值
    for i in range(M_norm):
        low_temp = low[i:i + N_near]
        high_temp = high[i:i + N_near]
        one_slope, _ = ols_fitting(low_temp, high_temp)
        res.append(one_slope)
    return res

# r2 统计学线性回归决定系数，也叫拟合优度。r2 \in [0~1]，拟合优度越大，自变量对因变量的解释程度越高。
def calc_r2(x, y):
    x = np.array(x)
    y = np.array(y)

    slope, intercept = ols_fitting(x, y)  # 一阶函数的斜率和截距
    y_pred = slope * x + intercept

    sse = sum((y - y_pred) ** 2)
    sse_temp = sse / (len(y) - 1)
    y_var = np.var(y, ddof=1)
    r2 = 1 - (sse_temp / y_var)
    return r2

# 通过斜率列表计算并返回截至回测结束日的最新标准分
def normalization(slopes):
    mean = np.mean(slopes)
    std = np.std(slopes)
    return (slopes[-1] - mean) / std

# RSRS 择时信号
def sell_or_buy(stockNum,lowdatas,highdatas):
    # 选择前N日的最高价和最低价
    print('最近', N_near, '日最高价', highdatas)#最近 18 日最高价 [192.0, 188.5, 188.5, 189.9, 191.5, 189.65, 189.8, 195.51, 193.56, 194.78, 192.74, 190.8, 194.8, 194.74, 199.62, 202.66, 202.8, 205.0]
    print('最近', N_near, '日最低价', lowdatas)#最近 18 日最低价 [188.68, 184.75, 185.0, 186.58, 188.0, 186.5, 184.2, 188.0, 189.05, 187.61, 187.54, 186.0, 190.96, 188.47, 193.35, 196.26, 198.2, 198.0]
    # 计算M日的斜率，返回数据是大小为M的list
    slopes = M_day_slope(stockNum,lowdatas,highdatas)
    r2 = calc_r2(lowdatas, highdatas)  # 计算r2的值
    print('r2的值', r2) #r2的值 0.9272263254381972
    # 通过前M日的数据对最新数据归一化
    rsrs_score = normalization(slopes) * r2
    print('rsrs_score 的值', rsrs_score)#rsrs_score 的值 -0.3155920886739633
    # 通过rsrs_score给出指示信号
    if rsrs_score > score_threshold:
        return "BUY"
    elif rsrs_score < -score_threshold:
        return "SELL"
    else:
        return "KEEP"


# ======================================

# 计算移动平均函数
def moving_average(data, window):
    weights = np.repeat(1.0, window) / window
    ma = np.convolve(data, weights, 'valid')
    return ma

def draw_average(prices):
    # 计算MA5和MA10
    ma5 = moving_average(prices, 5)
    ma10 = moving_average(prices, 10)
    ma20 = moving_average(prices, 20)
    ma30 = moving_average(prices, 30)
    ma60 = moving_average(prices, 60)

    # 绘制股票价格和移动平均曲线
    x = np.arange(len(prices))
    plt.plot(x, prices, label='Stock Prices')
    plt.plot(x[4:], ma5, label='MA5')
    plt.plot(x[9:], ma10, label='MA10')
    plt.plot(x[19:], ma20, label='MA20')
    # plt.plot(x[29:], ma30, label='MA30')
    # plt.plot(x[59:], ma60, label='MA60')

    # 设置图例和标题
    plt.legend()
    plt.title('Moving Averages')

    # 显示图形
    plt.show()
    
# draw_average([10, 12, 11, 15, 14, 13, 12, 11, 10, 12, 13, 11, 12, 11, 10,9,8,9,10,9,11,12,13,14,13,13,14,15,16,15,14])
