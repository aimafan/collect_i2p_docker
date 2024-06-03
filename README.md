# collect i2p docker
使用docker收集i2p流量

收集的流量主要有5*4类，分别是：
- none
- browser
- irc
- bt

- L
- O
- P
- X

> L limit bandwidth to 32 KB/sec, O - to 256 KB/sec, P - to 2048 KB/sec,
> X - unlimited

## how to use
用于收集browser流量，步骤如下：
1. 克隆项目
```
git clone -b browser https://github.com/aimafan/collect_i2p_docker.git
```

2. 修改`bushu/i2pd.conf`配置，主要修改`bandwidth`配置
3. 修改`bushu/docker-compose.yml`配置，主要修改挂载的路径
3. 开始部署，在`bushu`中
```
docker-compose up -d
```

4. 取消网卡合并包
```
ethtool -K enp1s0 tso off gso off gro off lro off
ethtool -K docker0 tso off gso off gro off lro off
ethtool -K br-bd55e4ff81fd tso off gso off gro off lro off
```

5. 进入容器
```
docker exec -it bushu_i2p_spider_1 bash
```

6. 取消网卡合并包
```
ethtool -K eth0 tso off gso off gro off lro off
```

6. 在`/app/src`中，执行
```
python -m collect_i2p_docker.spider.action
```