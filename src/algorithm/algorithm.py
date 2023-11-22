class Stock:
     def __init__(self,nums):
        self.Time = nums[0]# 10点之前打到预测ma5直接买，下午就缓缓
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
        
        # 止盈卖出系数
        self.TakeProfit = 1.1
        # 止损卖出系数
        self.StopLoss = 0.97
        
        self.Calculate5_predict(self,s=1.099)
       

     def Calculate5(self):
         nums = self.CloseValues
         return (nums[0]+nums[1]+nums[2]+nums[3]+nums[4])/5

     def Calculate10(self):
         nums = self.CloseValues
         return (nums[0]+nums[1]+nums[2]+nums[3]+nums[4]
            +nums[5]+nums[6]+nums[7]+nums[8]+nums[9])/10

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
     
        
     def Update(self,value):
         self.CurrentValue = value
         return self.CheckBuyByPredict()
        #  return self.CheckBuyValue(self)
     