import src.process

class SimpleProcess(src.process.multiprocessing.Process):
    def __init__(self, target, args=()):
        super().__init__()
        # 设置为true，表示该进程为守护进程，当主进程关闭时，会关闭所有守护进程
        self.daemon = True
        self.target = target
        self.args = args

    def start(self):
        # Process的start()内部会调用本类(SimpleProcess)的run方法
        super().start()
    
    def run(self):
        self.target(*self.args)
        # print("process run"+self.args)
    def join(self):
        print("join")
        super().join()
        
# def function(name):
#     print(f'Hello {name}')
    
# if __name__ == '__main__':
#     p = SimpleProcess(function, args=('Tom',))
#     p.start()
#     p.join()