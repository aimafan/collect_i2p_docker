import requests
from collect_i2p_docker.myutils.config import config
from collect_i2p_docker.myutils.logger import logger
from bs4 import BeautifulSoup
import re


def get_url_from_index(index_url):
    # 代理的IP地址和端口号
    proxy_host = config["proxy"]["host"]
    proxy_port = int(config["proxy"]["port"])
    timeout = int(config["spider"]["index_timeout"])
    url = []

    # 设置HTTP代理
    http_proxy = f"http://{proxy_host}:{proxy_port}"
    https_proxy = f"https://{proxy_host}:{proxy_port}"
    proxies = {
        "http": http_proxy,
        "https": https_proxy,
    }
    logger.info(
        f"正在从{index_url}获取url链接，如果{str(timeout)}s内没有响应，自动退出程序......"
    )
    try:
        # 发送带有代理的请求
        response = requests.get(index_url, proxies=proxies, timeout=timeout)

        # 检查响应状态码
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            table = soup.find("table", {"id": "sitetrack"})
            tbody = table.find("tbody")
            td_list = tbody.find_all("td", {"class": "b32"})
            for td in td_list:
                harf = td.a["href"]
                url.append(harf)

        else:
            logger.error("Failed to retrieve page. Status code:", response.status_code)

    except requests.exceptions.RequestException as e:
        logger.error("Error:", e)
    except Exception as e:
        logger.error("Error:", e)

    return url


if __name__ == "__main__":
    urls = get_url_from_index("http://notbob.i2p/")
    with open("./my_list.txt", "w") as file:
        for url in urls:
            file.writelines(url)
