
from multiprocessing import Process
import src.html as html
enginstr = "mysql+pymysql://root:Akeboshi123~@localhost:3306/stock"

def try_start():

     # 招商分时
     p1 = Process(target=html.cycleStocksTime,args=(600036,"招商银行分时",enginstr,))
     p1.daemon =True
     p1.start()
     
     # # 张江高科分时
     p2 = Process(target=html.cycleStocksTime,args=(600036,"张江高科分时",enginstr,))
     p2.daemon =True
     p2.start()

     # # 主板
     p3 = Process(target=html.cycleSHBoard,args=("http://quote.eastmoney.com/center/gridlist.html#sh_a_board",enginstr,))
     p3.daemon = True
     p3.start() 
     
     # =============== 有些问题，分时数据由于是从第三方获取数据，不能同时拉取多个数据
     # 600036 招商银行
     # 招商收盘开盘量比等数据
     p4 = Process(target=html.getStockData_datareader,args=('600036','招商银行',enginstr,))
     p4.daemon = True
     p4.start()
     
     # 600895 张江高科
     # 张江高科收盘开盘量比等数据
     # p5 = Process(target=html.getStockData_datareader,args=('600895',"张江高科",enginstr,))
     # p5.daemon = True
     # p5.start()
     
     
