from collect_i2p_docker.myutils import project_path
import os
import json
import random
from collect_i2p_docker.myutils.config import config
from collect_i2p_docker.myutils.logger import logger
import queue
from datetime import datetime
import time
import threading
import subprocess


log_path_queue = queue.Queue()
time_name = queue.Queue()


def traffic():
    # 获取当前时间
    now = datetime.now()
    # 格式化时间输出，格式为YYYYMMDDHHMMSS
    formatted_now = now.strftime("%Y%m%d%H")
    traffic_dir = os.path.join(project_path, "data")
    os.makedirs(traffic_dir, exist_ok=True)

    traffic_name = os.path.join(traffic_dir, f"{formatted_now}.pcap")

    # 设置tcpdump命令的参数
    tcpdump_command = [
        "tcpdump",
        "-n",
        "not",
        "port",
        "22",
        "and",
        "not",
        "port",
        "443",
        "and",
        "not",
        "port",
        "80",
        "-w",
        traffic_name,  # 输出文件的路径
    ]

    log_path = os.path.join(project_path, "data", "aimafan.log")
    if os.path.exists(log_path):
        # 删除文件
        os.remove(log_path)
    # 开流量收集
    subprocess.Popen(tcpdump_command)

    return traffic_name


def browser_action():
    while True:
        # 开流量收集
        traffic_thread = threading.Thread(target=traffic, args=())
        traffic_thread.start()
        traffic_thread.join()
        logger.info("开始捕获流量")
        time.sleep(1)

        # 开i2pd结点
        i2pd_path = os.path.join(project_path, "i2pd_aimafan", "build", "i2pd")
        subprocess.Popen([i2pd_path], stdout=subprocess.PIPE)
        time.sleep(5)
        logger.info("i2pd结点开启成功")

        while True:
            time.sleep(100)


if __name__ == "__main__":
    browser_action()
