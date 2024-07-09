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

取消网卡合并包
```
ethtool -K enp1s0 tso off gso off gro off lro off
ethtool -K eth0 tso off gso off gro off lro off
ethtool -K docker0 tso off gso off gro off lro off
ethtool -K br-1efccf5b3cc9 tso off gso off gro off lro off
```
## 原理
主要包括以下网站，分别是

论坛类：
http://i2pforum.i2p

wiki网站
http://wiki.i2p-projekt.i2p/

新闻
http://threatpost.i2p/

