
from multiprocessing import Process
import src.html as html
import time
import schedule
import threading
import subprocess
enginstr = "mysql+pymysql://root:Akeboshi123~@localhost:3306/stock"

done = threading.Event()
def _runProcess():     
     stocks = ['600036','600895','603178','603189','600678','600355','603025','600661','603536','603660']
     # 股票分时数据
     for stock in stocks:
        _p = Process(target=html.getStocksTime,args=(stock,enginstr,))
        _p.daemon = True
        _p.start()
        _p.join(30)
     
     # 股票收盘开盘量比等数据
     for stock in stocks:
        _p = Process(target=html.getStockData_datareader,args=(stock,enginstr,))
        _p.daemon = True
        _p.start()
        _p.join(30)
        
     # 主板
     p = Process(target=html.getSHBoard,args=("http://quote.eastmoney.com/center/gridlist.html#sh_a_board",enginstr,))
     p.daemon = True
     p.start() 
     
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

     
