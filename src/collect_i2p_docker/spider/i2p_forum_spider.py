import time
from selenium import webdriver
import requests
from collect_i2p_docker.myutils.config import config
from collect_i2p_docker.myutils.logger import logger, logger_result

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import threading

proxy_host_port = f"{config['proxy']['host']}:{config['proxy']['port']}"


def look_topic(driver, url, stop_event, traffic_name, neirong):
    # 创建一个集合来存储已经访问过的链接
    visited_links = set()
    for i in range(25):
        if stop_event.is_set():
            break
        links = driver.find_elements(
            By.XPATH, "//a[contains(@href, 'viewtopic.php?t=')]"
        )
        href = links[i].get_attribute("href")
        if href not in visited_links:
            visited_links.add(href)
            # 重新获取元素并访问
            try:
                logger_result.info(f"{traffic_name} - 发送GET请求 {href}")
                driver.get(href)
                logger_result.info(f"{traffic_name} - 请求完成 {href}")
                logger.info(f"访问链接{href}")
                time.sleep(3)  # 等待页面加载完成
                neirong_url = driver.find_elements(
                    By.XPATH,
                    '//a[@class="left-box arrow-left" and span[contains(text(), "Return to")]]',
                )[0].get_attribute("href")
                logger_result.info(f"{traffic_name} - 发送GET请求 {neirong_url}")
                driver.get(neirong_url)
                logger_result.info(f"{traffic_name} - 请求完成 {neirong_url}")

                logger.info("返回之前的界面")
                time.sleep(3)  # 等待页面加载完成
            except Exception as e:
                logger.info(
                    f"访问过程中 {href} 失败，失败原因 {str(e).split('Stacktrace')[0]}"
                )
                continue
    return


def i2pforum_spider(traffic_name):
    # 用于爬取http://i2pforum.i2p/网站
    # 进入主页之后，首先进入Router，然后再Router里面选择topic进行加载
    url = "http://i2pforum.i2p/"
    timeout = int(config["spider"]["url_timeout"])

    # sleep_time = int(config["spider"]["sleep_time"])

    # Set up Selenium WebDriver with the proxy
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"--proxy-server=http://{proxy_host_port}")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--remote-debugging-port=9222")
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(timeout)
    stop_event = threading.Event()

    def stop_driver():
        time.sleep(int(config["spider"]["stop_time"]))  # 等待三分钟
        logger.info("计时器时间到，发送停止信号")
        stop_event.set()

    # 启动计时器线程
    try:
        # Navigate to the URL
        logger_result.info(f"{traffic_name} - 发送GET请求 {url}")
        driver.get(url)
        logger_result.info(f"{traffic_name} - 请求完成 {url}")
        time.sleep(3)
        logger.info(f"访问页面 {url}")
        timer_thread = threading.Thread(target=stop_driver)
        timer_thread.start()

        # 获取所有站内链接
        index_urls = driver.find_elements(
            By.XPATH, "//a[contains(@href, 'viewforum.php?f=')]"
        )

        router_url = index_urls[3].get_attribute("href")

        logger_result.info(f"{traffic_name} - 发送GET请求 {router_url}")
        driver.get(router_url)
        logger_result.info(f"{traffic_name} - 请求完成 {router_url}")
        time.sleep(3)
        logger.info(f"访问Router界面：{router_url}")

        # 遍历Routerinfo的帖子
        look_topic(driver, url, stop_event, traffic_name, "Router")

        index_link = driver.find_elements(
            By.XPATH, "//a[contains(@href, 'index.php?')]"
        )[0].get_attribute("href")
        logger_result.info(f"{traffic_name} - 发送GET请求 {index_link}")
        driver.get(index_link)  # 返回主页
        logger_result.info(f"{traffic_name} - 请求完成 {index_link}")
        time.sleep(3)
        i2psnark_url = driver.find_elements(
            By.XPATH, "//a[contains(@href, 'viewforum.php?f=')]"
        )[6].get_attribute("href")
        logger_result.info(f"{traffic_name} - 发送GET请求 {i2psnark_url}")
        driver.get(i2psnark_url)
        logger_result.info(f"{traffic_name} - 请求完成 {i2psnark_url}")
        time.sleep(3)
        logger.info(f"访问I2PSnark界面：{router_url}")
        look_topic(driver, url, stop_event, traffic_name, "I2PSnark")

        driver.quit()
        return True
    except Exception as e:
        driver.quit()
        return False


if __name__ == "__main__":
    aa = i2pforum_spider("http://i2pforum.i2p", "name")
    print(aa)
