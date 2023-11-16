
from multiprocessing import Process
import src.html

def try_start():

     p1 = Process(target=src.html.eastmoney.cycle,args=())
     p1.daemon =True
     p1.start()


     p2 = Process(target=src.html.sinafinance.cycle,args=())
     p2.daemon = True
     p2.start()  
