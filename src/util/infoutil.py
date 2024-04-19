import platform
import socket

# 获取计算机的操作系统信息
print("操作系统:", platform.system())
print("操作系统版本:", platform.release())

# 获取计算机的主机名
print("主机名:", socket.gethostname())

# 获取计算机的IP地址
ip_address = socket.gethostbyname(socket.gethostname())
print("IP地址:", ip_address)

# 获取计算机的处理器信息
print("处理器:", platform.processor())

# 获取计算机的内存信息
system_memory = platform.virtual_memory()
print("总内存:", system_memory.total)
print("可用内存:", system_memory.available)