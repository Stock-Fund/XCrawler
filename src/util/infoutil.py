import platform
import socket
import psutil

# 获取计算机的操作系统信息
def get_os_info():
    os_info = platform.platform()
    # print("操作系统信息:", os_info)
    return os_info

# 获取计算机的操作系统类型
def get_os_type():
    os_type = platform.system()
    # print("操作系统类型:", os_type)
    return os_type

# 获取计算机的主机名
def get_hostname():
    hostname = socket.gethostname()
    # print("主机名:", hostname)
    return hostname

# 获取计算机的IP地址
def get_ip_address():
    ip_address = socket.gethostbyname(socket.gethostname())
    # print("IP地址:", ip_address)
    return ip_address


# 获取计算机的处理器信息
def get_processor_info():
    processor_info = platform.processor()
    # print("处理器信息:", processor_info)
    return processor_info

# 获取计算机的总内存
def get_total_memory():
    system_memory = psutil.virtual_memory()
    return system_memory
    # print("总内存:", system_memory.total)
    # print("可用内存:", system_memory.available)

def get_total_info():
    info = get_os_info()
    type = get_os_type()
    host = get_hostname()
    ip = get_ip_address()
    processor_info = get_processor_info()
    memory = get_total_memory()
    return f"{info},{type},{host},{ip},{processor_info},{memory}"