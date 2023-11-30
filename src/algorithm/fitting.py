import numpy as np
import matplotlib.pyplot as plt
     

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
