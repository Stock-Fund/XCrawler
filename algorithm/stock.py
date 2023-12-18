import numpy as np
import statistics
import algorithm.fitting
import talib
class Stock:
     # 计算移动平均函数
     def moving_average(data, window):
         weights = np.repeat(1.0, window) / window
         ma = np.convolve(data, weights, 'valid')
         return ma  

     def CalculateAverage(self,num):
         nums = self.CloseValues
         return self.moving_average(self.CloseValues,num)

     # 上一个交易日是否是跌势
     def IsFallYesterday(self):
         value = self.CloseValues[1]
         open = self.OpenValues[1]
         return value <open
     
     # 当前交易日是否是跌势
     def IsFallToday(self):
         value = self.CloseValues[0]
         open = self.OpenValues[0]
         return value <open

     # 预测明天5日线价格,可能是阶段低点
     def Calculate5_predict(self,s=1.099):
         self.predictValue = (self.CloseValues[0]*s+self.CloseValues[0]+self.CloseValues[1]+self.CloseValues[2]+self.CloseValues[3])/5
         return self.predictValue
     # =========== 短线逻辑
     # 龙头低吸算法1（预测5日线买入算法）
     def CheckBuyByPredict(self):
          return self.CurrentValue < self.predictValue

     # 龙头低吸算法2（5日线-10日线检测买入算法）          
     def CheckBuy(self):
         currentValue = self.CurrentValue
         # 只有连续5板以上
         # 只有在昨天下跌的情况下
         if self.IsFallYesterday():         
           MA5 = self.MA5
           MA10 = self.MA10
           if currentValue > MA5:
              return False
            # 触摸5日线 
           elif currentValue == MA5:
               return True
            # 击穿5日线，就以10日线为准
           elif currentValue < MA5 :
                # 在5-10日线之间，没有支撑位，破位！
                if currentValue > MA10:
                   return False
                # 触摸到10日线，找到10日线
                elif currentValue == MA10 :
                    return True
                # 10日线以下，放弃
                else:
                    return False
                
     # 卖出逻辑           
     def CheckSell(self,value):
         # value 传入当前成本价
         return self.CurrentValue >= value * self.TakeProfit or self.CurrentValue <= value * self.StopLoss
     
     # 长线逻辑(趋势逻辑)
     # 判断趋势的逻辑
     def detect_trend(ma5, ma10, ma20):
         trend = []
         if ma5 > ma10 and ma5 > ma20:
            trend.append("上涨")
         elif ma5 < ma10 and ma5 < ma20:
            trend.append("下跌")
         else:
            trend.append("震荡")
         return trend
     
     # 箱体逻辑 
     def checkBox(self,max,min):
         if self.CurrentValue >= max:
             return True
         elif self.CurrentValue <= min:
             return False
         else:
             return False
         
     # 破位逻辑
     def checkBroken(self):
         closeValue = self.CloseValues[0]
         if(closeValue<self.MA5):
             print("破5日线")
         elif(closeValue<self.MA10):
             print("破10日线")
         elif(closeValue<self.MA20):
             print("破20日线")
         elif(closeValue<self.MA30):
             print("破30日线")
         elif(closeValue<self.MA60):
             print("破60日线")
             
    
     # 判断是否是放量
     # 以该股票最近一个月或者三个月的日均交易量为基准平均值。
     # 如果该日交易量高于基准平均值的一定倍数(如150%或者200%),则认为该日交易量较大,是放量。
     # 如果该日交易量低于基准平均值的一定比例(如50%或者70%),则认为该日交易量较小,是缩量。
     # 如果在基准平均值和放量标准之间,则认为交易量一般,既不是明显放量也不是缩量。
     def checkVolumeIncreaseOrShrink(self):
         totalVolume = sum(self.Volumes)
         count = len(self.volumes)
         average = totalVolume/count
         # 放量
         if self.Volumes[0] > average*1.5:
             return 1
         # 缩量
         elif self.Volumes[0] < average*0.5:
             return -1
         # 正常量
         else:
             return 0
    
     # 判断某天收盘是否为红盘(收盘价高于开盘价)
     def checkRise(self,index):
        return self.CloseValues[index] > self.OpenValues[index]
     
     # 判断是否阳包阴，还是阴包阳
     def checkVolums(self):
         today = self.Volumes[0]
         yesterday = self.Volumes[1]
         if not self.checkRise(0) and yesterday < today:
             return True
         else:
             return False 
     # 主升浪逻辑
     def MainSL(self):
         mainBoo = False
         # 1-60作为x轴的数值
         days = np.arange(1,61).reshape(-1,1)
         # 收盘价 趋势连续上涨。价格形成一系列超过坚振位的高点和低点,形成上扬趋势。
         slope = fitting.simple_fit(days,self.CloseValues)
         # 简单判断，当60日收盘价拟合斜率为正，表示60日收盘价处于上涨趋势，可以简单的算作主升浪情况
         # 日K线斜率在0.001~0.005之间。这个范围内表示股价走势呈现出小幅上涨趋势。
         # 日K线斜率在0.005~0.01之间。此时股价走势属于中等上涨趋势。
         # 日K线斜率在0.01以上。这种斜率代表股价处于明显的强劲上涨趋势中。
         mainBoo = True if slope > 0 else False
         
         # 均线上行。成交量均线、动量指标等有力指标呈现上升趋势MA(C,5)>MA(C,10) AND MA(C,10)>MA(C,20) AND MA(C,20)>MA(C,N) AND MA(C,N)>MA(C,120) AND MA(C,120)>REF(MA(C,120),1) AND MA(C,5)>REF(MA(C,5),1);
         slopeMA5 = fitting.simple_fit(days,self.MA5s)
         slopeMA10 = fitting.simple_fit(days,self.MA10s)
         slopeMA20 = fitting.simple_fit(days,self.MA20s)
         slopeMA60 = fitting.simple_fit(days,self.MA60s)
         slopeMA120 = fitting.simple_fit(days,self.MA120s)
         mainBoo = True if slopeMA5 > slopeMA10 and slopeMA10 > slopeMA20 and slopeMA20 > slopeMA60 and slopeMA60 > slopeMA120 else False
         # todo 判断低位集中收购
         
         # todo 判断新高突破
         # todo 指标穿线支持。如动量指标金叉死叉等技术信号表明趋势有望继续
         
         return mainBoo
     
     # boll逻辑 todo
         
     def Update(self,value):
         self.CurrentValue = value
         return self.CheckBuyByPredict()
        #  return self.CheckBuyValue(self)

     def dealcustomData(data):
        close_prices = data['Close'].tolist()
        close_prices_array = np.array(close_prices, dtype=np.double)
        # 计算MACD
        macd = talib.MACD(close_prices_array, fastperiod=12, slowperiod=26, signalperiod=9)
        # N日简单移动平均数
        ma5 = ta.SMA(close_prices_array, timeperiod=5)
        ma10 = ta.SMA(close_prices_array, timeperiod=10)
        ma30 = ta.SMA(close_prices_array, timeperiod=30)
   
     def __init__(self,data,datas):
        # N日内的收盘价格列表
        self.CloseValues = data['Close'].tolist()
        # N日内的开盘价格列表
        self.OpenValues = data['Open'].tolist()
        self.MaxValues = data['High'].tolist()
        self.MinValues = data['Low'].tolist()
        # N日内成交量
        self.Volumes = data['Volume'].tolist()
        # 5日收盘价均价
        self.MA5 = stock['Close'].rolling(window=5).mean() 
        self.MA10 = stock['Close'].rolling(window=10).mean() 
        self.MA20 = stock['Close'].rolling(window=20).mean() 
        self.MA30 = stock['Close'].rolling(window=30).mean() 
        self.MA40 = stock['Close'].rolling(window=40).mean() 
        self.MA60 = stock['Close'].rolling(window=60).mean() 
        
        self.Time = datas[0]# 10点之前打到预测ma5直接买，下午就缓缓
        ## 所有的数组类数据全部为倒置存储，第0位就是当前天的数据
        # 当前价格
        self.CurrentValue = datas[1]
        
        # N日内换手率
        self.turnoverRates = datas[2]
        
        # N日量比
        self.QuantityRatios = datas[3]
        
        # N日分时均价  均价=成交总额/成交量 由于分时均价频率较高，则使用   均价 = 每日收盘时的成交总额/每日收盘时的成交量
        self.AveragePrices = datas[4]

        # N内筹码集中度
        # 筹码集中度=成本区间的（高值-低值）/（高值+低值）
        self.Chipsconcentrations = datas[5]
        
        # 止盈卖出系数
        self.TakeProfit = 1.1
        # 止损卖出系数
        self.StopLoss = 0.97
        
        self.Calculate5_predict(self,s=1.099)
   