from collect_i2p_docker.myutils import project_path
import os
import json
import random
from collect_i2p_docker.myutils.config import config
from collect_i2p_docker.myutils.logger import logger
from collect_i2p_docker.spider.i2p_forum_spider import i2pforum_spider
from collect_i2p_docker.spider.wiki_spider import wiki_spider
import queue
from datetime import datetime
import time
import threading
import subprocess


log_path_queue = queue.Queue()
time_name = queue.Queue()


def traffic(file_path):
    # 获取当前时间
    now = datetime.now()
    # 格式化时间输出，格式为YYYYMMDDHHMMSS
    formatted_now = now.strftime("%Y%m%d%H%M%S")
    traffic_dir = os.path.join(project_path, "data", "traffic")
    os.makedirs(traffic_dir, exist_ok=True)

    traffic_name = os.path.join(
        traffic_dir, f"{formatted_now}_{os.path.basename(file_path)}.pcap"
    )

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
    traffic_process = subprocess.Popen(tcpdump_command)

    return traffic_process, traffic_name


def browser_action():
    url_lists = [
        i2pforum_spider,
        wiki_spider,
    ]
    website_name = ["i2pforum", "wiki"]
    count = 0
    while True:
        # 开流量收集
        count = count % len(url_lists)
        traffic_process, traffic_name = traffic(website_name[count].split("://")[-1])
        logger.info("开始捕获流量")
        time.sleep(1)

        # 开i2pd结点
        i2pd_path = os.path.join(project_path, "i2pd_aimafan", "build", "i2pd")
        process = subprocess.Popen([i2pd_path], stdout=subprocess.PIPE)
        time.sleep(20)
        logger.info("i2pd结点开启成功")

        while True:
            if not url_lists[count](traffic_name):
                time.sleep(30)
                continue
            else:
                logger.info(f"{website_name[count]}网站访问完成")
                break

        # 关i2pd结点
        process.kill()
        time.sleep(2)
        # 关流量收集
        traffic_process.kill()
        count += 1
        time.sleep(10)


if __name__ == "__main__":
    browser_action()
