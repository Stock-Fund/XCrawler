
from multiprocessing import Process
import src.html as html
import time
import schedule
import threading
enginstr = "mysql+pymysql://root:Akeboshi123~@localhost:3306/stock"

done = threading.Event()
def _runProcess():
      # 招商分时
     p1 = Process(target=html.cycleStocksTime,args=(600036,"招商银行分时",enginstr,))
     p1.daemon =True
     p1.start()
     
     # # 张江高科分时
     p2 = Process(target=html.cycleStocksTime,args=(600895,"张江高科分时",enginstr,))
     p2.daemon =True
     p2.start()

     # # 主板
     p3 = Process(target=html.cycleSHBoard,args=("http://quote.eastmoney.com/center/gridlist.html#sh_a_board",enginstr,))
     p3.daemon = True
     p3.start() 
     
     # 600036 招商银行
     # 招商收盘开盘量比等数据
     p4 = Process(target=html.getStockData_datareader,args=('600036','招商银行',enginstr,))
     p4.daemon = True
     p4.start()
     
     # 600895 张江高科
     # 张江高科收盘开盘量比等数据
     p5 = Process(target=html.getStockData_datareader,args=('600895',"张江高科",enginstr,))
     p5.daemon = True
     p5.start()
     done.set()
     
def run_forever():
     schedule.every().day.at("15:00").do(_runProcess)
     while not done.is_set():
       # localtime = src.timeutil.get_local_time()
       # 每天15:00遍历一次网页的数据
       schedule.run_pending()
       time.sleep(1)

def try_start():
     thread = threading.Thread(target=run_forever,daemon=True)
     thread.start() 

     
