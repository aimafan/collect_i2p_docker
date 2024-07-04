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

## file_share分支
用来进行文件的传输，包括上传和下载

关键域名：http://sharefile.i2p/

部署步骤：
sudo ethtool -K eth0 tso off gso off gro off
sudo ethtool -K br-705317af73e5 tso off gso off gro off

