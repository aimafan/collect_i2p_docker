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
    tcpdump \
    openjdk-17-jdk

# 将vim设为默认编辑器
RUN update-alternatives --set editor /usr/bin/vim.basic 

ADD . .
# 取消网卡合并包，需要在启动容器之后跑
# RUN sudo ethtool -K eth0 tso off gso off gro off
RUN pip3 install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

RUN cd i2pd_aimafan/build; cmake .; make -j7

# 默认命令，打开vim
CMD ["bash"]