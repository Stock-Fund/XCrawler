import asyncio
class Coroutine:
# 协程
    def __init__(self):
       print('Coroutine init')
       
    # 外部传入异步方法，返回一个Function对象，这个对象不是async_func本身
    def run(self, async_func):
       return asyncio.run(async_func())

    # 外部传入异步方法，并创建成为task，返回出去，指定返回task
    async def create_task(self,async_func):
       task = asyncio.create_task(async_func())
       return task

    # 外部传入异步方法，
    async def ensure_future(self,async_func):
       """使用ensure_future运行协程"""
       task = asyncio.ensure_future(async_func())
       return task
  