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

## 收集bt流量的步骤
首先对于i2pd.conf文件，需要打开i2cp选项


热门种子有这些
| 种子 | 大小 |
| --- | --- |
| magnet:?xt=urn:btih:d5c4b9e3fb726f8c115c91bd5bd0b49a4fe918dc | 1.4G |
| magnet:?xt=urn:btih:3cc693c5e0321d4820e557b427c358dc5e94be7f | 1.6G |
| magnet:?xt=urn:btih:5bd760a4e0d3b4d11bfa031d3dba4570f1859a0d | 1.5G |
| magnet:?xt=urn:btih:690bd086100b3d379af93579e43bc8fcbdb64157 | 44M |
| magnet:?xt=urn:btih:26cd91d8e488bcb4bf8ece3d2b3d7258cb4ae59f | 411K |
| magnet:?xt=urn:btih:caeecd4cd9ae59cda23a231344dda125909010d3 | 150M |
| magnet:?xt=urn:btih:461b73684dc7b97779ed6e9735e4d5e7a43c5ccf | 200M |
| magnet:?xt=urn:btih:87377fc18674fdab8bb475f043b7371b328e2105 | 8M |