
from multiprocessing import Process
import src.html


def try_start():

     p1 = Process(target=src.html.eastmoney.cycleStocks,args=(600036,))
     p1.daemon =True
     p1.start()


     # p2 = Process(target=src.html.eastmoney.cycleSHBoard,args=())
     # p2.daemon = True
     # p2.start() 
     
     # 600895 张江高科
     # 600036 招商银行
     # p3 = Process(target=src.html.eastmoney.getStockData_datareader,args=('600895',))
     # p3.daemon = True
     # p3.start()
     
     
