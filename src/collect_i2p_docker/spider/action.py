from collect_i2p_docker.myutils import project_path
import os
from collect_i2p_docker.myutils.logger import logger
from collect_i2p_docker.spider.upload_file import upload
import queue
from datetime import datetime
import time
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


def file_share_action():
    data_path = os.path.join(project_path, "data")
    file_paths = [
        os.path.join(data_path, "100K"),
        os.path.join(data_path, "200K"),
        os.path.join(data_path, "500K"),
        os.path.join(data_path, "1M"),
        os.path.join(data_path, "2M"),
        os.path.join(data_path, "5M"),
        os.path.join(data_path, "10M"),
        os.path.join(data_path, "20M"),
    ]
    count = 0
    while True:
        # 开流量收集
        count = count % len(file_paths)
        url = "http://sharefile.i2p"
        traffic_process, traffic_name = traffic(file_paths[count])
        logger.info("开始捕获流量")
        time.sleep(1)

        # 开i2pd结点
        i2pd_path = os.path.join(project_path, "i2pd_aimafan", "build", "i2pd")
        process = subprocess.Popen([i2pd_path], stdout=subprocess.PIPE)
        time.sleep(20)
        logger.info("i2pd结点开启成功")

        # 文件上传(要注意和访问网页的流区分开)
        for i in range(50):
            if upload(url, file_paths[count], traffic_name):
                break
            else:
                time.sleep(10)

        # 关i2pd结点
        process.kill()
        time.sleep(2)
        # 关流量收集
        traffic_process.kill()
        count += 1
        time.sleep(10)


if __name__ == "__main__":
    file_share_action()
