import time
from selenium import webdriver
import requests
from collect_i2p_docker.myutils.config import config
from collect_i2p_docker.myutils.logger import logger, traffic_logger

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

proxy_host_port = f"{config['proxy']['host']}:{config['proxy']['port']}"


def upload(url, file_path, traffic_name):
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
    try:
        # Navigate to the URL
        logger.info(f"正在访问 {url}")
        driver.get(url)

        # 等待页面加载并找到 nojs-panel 选项卡
        nojs_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "nojs-tab"))
        )
        nojs_tab.click()
        time.sleep(1)
        # 等待 nojs-panel 显示出来并找到文件选择输入框
        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//div[@id='nojs-panel']//div[@class='upload_form_cont']//form[@id='upload_form']//input[@type='file' and @name='upload_file']",
                )
            )
        )
        time.sleep(1)
        # 选择文件
        file_input.send_keys(file_path)
        time.sleep(1)
        traffic_logger.info(f"开始上传{file_path}，流量位于{traffic_name}")
        # 找到并点击上传按钮
        upload_button = driver.find_element(
            By.XPATH, "//div[@id='nojs-panel']//input[@type='submit']"
        )
        upload_button.click()
        time.sleep(1)

        # 等待上传完成（可以根据页面的响应来设置等待条件）
        WebDriverWait(driver, 400).until(
            EC.presence_of_element_located((By.ID, "upload_response"))
        )
        traffic_logger.info(f"上传完成{file_path}，流量位于{traffic_name}")

        logger.info(f"成功访问 {url}")
        driver.quit()
        return True
    except Exception as e:
        logger.warning(f"访问 {url} 失败，失败原因 {str(e).split('Stacktrace')[0]}")
        driver.quit()
        return False


if __name__ == "__main__":
    upload("http://sharefile.i2p")
