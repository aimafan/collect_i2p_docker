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


def look_topic(driver, stop_event, traffic_name):
    # 创建一个集合来存储已经访问过的链接
    visited_links = set()
    # 获取所有站内链接

    for i in range(50):
        links = driver.find_elements(By.XPATH, "//a[contains(@href, '/wiki/')]")
        if stop_event.is_set():
            break

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
                index = driver.find_elements(
                    By.XPATH,
                    '//a[text()="Main page"]',
                )[0].get_attribute("href")
                logger_result.info(f"{traffic_name} - 发送GET请求 {index}")
                driver.get(index)
                logger_result.info(f"{traffic_name} - 请求完成 {index}")

                logger.info("返回之前的界面")
                time.sleep(3)  # 等待页面加载完成
            except Exception as e:
                logger.info(
                    f"访问过程中 {href} 失败，失败原因 {str(e).split('Stacktrace')[0]}"
                )
                continue
    return


def wiki_spider(traffic_name):
    # 用于爬取http://i2pforum.i2p/网站
    # 进入主页之后，首先进入Router，然后再Router里面选择topic进行加载
    url = "http://wiki.i2p-projekt.i2p/"
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
        time.sleep(2)
        logger.info(f"访问页面 {url}")
        timer_thread = threading.Thread(target=stop_driver)
        timer_thread.start()
        look_topic(driver, stop_event, traffic_name)

        driver.quit()
        return True
    except Exception as e:
        driver.quit()
        return False


if __name__ == "__main__":
    aa = wiki_spider("name")
    logger.info(aa)
