import websocket
async def receive_notification():
    async with websocket.connect("ws://localhost:8000") as websocket:
        # 接收字节流
        notification_bytes = await websocket.recv()

        # 将字节流反序列化为通知对象
        notification = Notification()
        notification.ParseFromString(notification_bytes)

        # 读取通知内容
        message = notification.message
        print("Received notification:", message)

asyncio.get_event_loop().run_until_complete(receive_notification())