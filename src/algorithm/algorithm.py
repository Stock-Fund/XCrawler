class Stock:
     def __init__(self,nums):
        self.Time = nums[0]
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

     # 预测明天5日线价格，也就是明天买入标准价格
     def Calculate5_predict(self,s=1.099):
         self.predictValue = (self.CloseValues[0]*s+self.CloseValues[0]+self.CloseValues[1]+self.CloseValues[2]+self.CloseValues[3])/5
         return self.predictValue

     # 如果价格跌穿预计5日线,需观察是否击穿10日线             
     def CheckBuyValue(self):
         currentValue = self.CurrentValue
         predictValue = self.predictValue
         # 当前价格如果达到预测价格
         if currentValue <= predictValue:
             return True
         
         MA5 = self.MA5s[0]
         MA10 = self.MA10s[0]
         if currentValue > MA5:
            return False
            # 击穿5日线，但没破10日线
         elif currentValue < MA5 and currentValue > MA10:
            return True
            ## 击穿10日线，破位
         elif currentValue <= MA10:
            return False
     