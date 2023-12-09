
from multiprocessing import Process
import src.html as html
import time
import schedule
import threading
import subprocess
enginstr = "mysql+pymysql://root:Akeboshi123~@localhost:3306/stock"

done = threading.Event()
def _runProcess():
     # 招商分时
     p1 = Process(target=html.getStocksTime,args=(600036,enginstr,))
     p1.daemon =True
     p1.start()
     
     # 张江高科分时
     p2 = Process(target=html.getStocksTime,args=(600895,enginstr,))
     p2.daemon =True
     p2.start()
     
     # 江苏舜天
     p6 = Process(target=html.getStocksTime,args=(600287,enginstr,))
     p6.daemon =True
     p6.start()

     # 主板
     p3 = Process(target=html.getSHBoard,args=("http://quote.eastmoney.com/center/gridlist.html#sh_a_board",enginstr,))
     p3.daemon = True
     p3.start() 
     
     # 600036 招商银行
     # 招商收盘开盘量比等数据
     p4 = Process(target=html.getStockData_datareader,args=('600287',enginstr,))
     p4.daemon = True
     p4.start()
     
     # 600895 张江高科
     # 张江高科收盘开盘量比等数据
    #  p5 = Process(target=html.getStockData_datareader,args=('600895',"张江高科",enginstr,))
    #  p5.daemon = True
    #  p5.start()
     done.set()

def run_forever(check):
     if check:
        schedule.every().day.at("15:00").do(_runProcess)
        while not done.is_set():
          # localtime = src.timeutil.get_local_time()
          # 每天15:00遍历一次网页的数据
          schedule.run_pending()
          time.sleep(1)
     else :
       _runProcess()

def try_start():
     thread = threading.Thread(target=run_forever,args=(True,),daemon=True)
     thread.start() 
  

def start():
   run_forever(False)

def find(stockNum):
     p = Process(target=html.getStocksTime,args=(f'{stockNum}',enginstr,))
     p.daemon = True
     p.start()
     
     p1 = Process(target=html.getStockData_datareader,args=(f'{stockNum}',enginstr,))
     p1.daemon = True
     p1.start()
     print(f"查找对应代码{stockNum}股票")

     
