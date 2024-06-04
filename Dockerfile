FROM debian:bullseye

# 设置工作目录
WORKDIR /app

# 安装基本工具和依赖
RUN sed -i 's|http://deb.debian.org|http://mirrors.aliyun.com|g' /etc/apt/sources.list && \
    apt-get update && apt-get install -y \
    vim \
    sudo \
    python3.9 \
    python3-pip \
    python3.9-venv \
    net-tools \
    wget    \
    curl    \
    build-essential \
    gcc \
    make \
    inetutils-ping \
    python-is-python3 \
    cmake \
    libboost-date-time-dev \
    libboost-filesystem-dev \
    libboost-program-options-dev \
    libboost-system-dev \
    libssl-dev \
    zlib1g-dev \
    debhelper \
    fakeroot \
    devscripts \
    dh-apparmor \
    ethtool \
    libpcap-dev \
    tcpdump

# 将vim设为默认编辑器
RUN update-alternatives --set editor /usr/bin/vim.basic

ADD . .
# 取消网卡合并包，需要在启动容器之后跑
# RUN sudo ethtool -K eth0 tso off gso off gro off
RUN pip3 install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 安装weechat相关内容
RUN apt install -y ca-certificates dirmngr gpg-agent apt-transport-https
RUN mkdir /root/.gnupg
RUN chmod 700 /root/.gnupg
RUN mkdir -p /usr/share/keyrings
RUN gpg --no-default-keyring --keyring /usr/share/keyrings/weechat-archive-keyring.gpg --keyserver hkps://keys.openpgp.org --recv-keys 11E9DE8848F2B65222AA75B8D1820DB22A11534E
RUN echo "deb [signed-by=/usr/share/keyrings/weechat-archive-keyring.gpg] https://weechat.org/debian bullseye main" | sudo tee /etc/apt/sources.list.d/weechat.list
RUN echo "deb-src [signed-by=/usr/share/keyrings/weechat-archive-keyring.gpg] https://weechat.org/debian bullseye main" | sudo tee -a /etc/apt/sources.list.d/weechat.list
RUN apt-get update
RUN apt-get install -y weechat-curses weechat-plugins weechat-python weechat-perl


RUN cd i2pd_aimafan/build; cmake .; make -j7

# 默认命令，打开vim
CMD ["bash"]