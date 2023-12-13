import numpy as np
import statistics
import fitting
class Stock:
     def __init__(self,nums):
        self.Time = nums[0]# 10点之前打到预测ma5直接买，下午就缓缓
        ## 所有的数组类数据全部为倒置存储，第0位就是当前天的数据
        # 当前价格
        self.CurrentValue = nums[1]
        # 60日内的收盘价格列表
        self.CloseValues = nums[2]
        # 60日内的开盘价格列表
        self.OpenValues = nums[3]
        self.MaxValues = nums[4]
        self.MinValues = nums[5]
        # 60内，30日，20日，10日，5日均线价格
        self.MA5s = nums[6]
        self.MA10s = nums[7]
        self.MA20s = nums[8]
        self.MA30s = nums[9]
        self.MA60s = nums[10]
       
        # 60日内成交量
        self.Volumes = nums[11]
        # 60日内成交金额
        self.VolumesValues = nums[12]
        # 60日内换手率
        self.turnoverRates = nums[13]
        # 60日量比
        self.QuantityRatios = nums[14]
        
        # 60日分时均价  均价=成交总额/成交量 由于分时均价频率较高，则使用   均价 = 每日收盘时的成交总额/每日收盘时的成交量
        self.AveragePrices = nums[15]
        
        # 60内筹码集中度
        # 筹码集中度=成本区间的（高值-低值）/（高值+低值）
        self.Chipsconcentrations = nums[16]
        
        # 止盈卖出系数
        self.TakeProfit = 1.1
        # 止损卖出系数
        self.StopLoss = 0.97
        
        self.Calculate5_predict(self,s=1.099)
     
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
           MA5 = self.MA5s[0]
           MA10 = self.MA10s[0]
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
     def detect_trend(ma5s, ma10s, ma20s):
         trend = []
         for i in range(len(ma5s)):
            if ma5s[i] > ma10s[i] and ma5s[i] > ma20s[i]:
               trend.append("上涨")
            elif ma5s[i] < ma10s[i] and ma5s[i] < ma20s[i]:
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
     def checkBroken(self,ma5,ma10,ma20,ma30,ma60):
         closeValue = self.CloseValues[0]
         if(closeValue<ma5):
             print("破5日线")
         elif(closeValue<ma10):
             print("破10日线")
         elif(closeValue<ma20):
             print("破20日线")
         elif(closeValue<ma30):
             print("破30日线")
         elif(closeValue<ma60):
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
         # 1-60作为x轴的数值
         days = np.arange(1,61).reshape(-1,1)
         # 收盘价 趋势连续上涨。价格形成一系列超过坚振位的高点和低点,形成上扬趋势。
         slope = fitting.simple_fit(days,self.CloseValues)
         # todo 均线上行。成交量均线、动量指标等有力指标呈现上升趋势MA(C,5)>MA(C,10) AND MA(C,10)>MA(C,20) AND MA(C,20)>MA(C,60) AND MA(C,60)>MA(C,120) AND MA(C,120)>REF(MA(C,120),1) AND MA(C,5)>REF(MA(C,5),1);
         # todo 判断低位集中收购
         # todo 判断新高突破
         # todo 指标穿线支持。如动量指标金叉死叉等技术信号表明趋势有望继续
         # 简单判断，当60日收盘价拟合斜率为正，表示60日收盘价处于上涨趋势，可以简单的算作主升浪情况
         if slope > 0:
             return True
         return False
     
     # boll逻辑 todo
         

# # 计算MA5、MA10和MA20
# ma5 = moving_average(prices, 5)
# ma10 = moving_average(prices, 10)
# ma20 = moving_average(prices, 20)
# 执行趋势判断
# trend = detect_trend(ma5, ma10, ma20)   
    
     def Update(self,value):
         self.CurrentValue = value
         return self.CheckBuyByPredict()
        #  return self.CheckBuyValue(self)
     