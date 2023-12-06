
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
     
def run_forever(check):
     if check:
        schedule.every().day.at("19:19").do(_runProcess)
        while not done.is_set():
          # localtime = src.timeutil.get_local_time()
          # 每天15:00遍历一次网页的数据
          schedule.run_pending()
          time.sleep(1)
     else :
       _runProcess()
       
def _runMysql():
     # 执行命令
     cmd = 'mysqladmin -u root -p status'
     result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
     # 检查执行结果
     if result.returncode == 0 and 'Uptime' in result.stdout:
       print("MySQL已启动")
       return True
     else:
       return False

def try_start():     
     if _runMysql():
        thread = threading.Thread(target=run_forever,args=(True,),daemon=True)
        thread.start() 
     else :
        print("MySQL启动失败")
        

def start():
    if _runMysql():
        thread = threading.Thread(target=run_forever,args=(False,),daemon=True)
        thread.start() 
    else :
        print("MySQL启动失败")

     
