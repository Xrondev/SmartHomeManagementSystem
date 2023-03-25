<a name="Ksb61"></a>
## 安装：使用Docker
虚拟机安装：确保docker已经安装<br />**部分跟随官方指导：**

- 需要切换镜像源：推荐阿里云个人镜像服务（免费），链接手动获取
- 手动设置config映射位置：此例为/etc/docker/HAOS
- 手动调整时区设置
- 不要使用官方ghcr Github的镜像仓库，巨慢
```shell
docker run -d \
--name homeassistant \
--privileged \
--restart=unless-stopped \
-e TZ=Asia/Chongqing \
-v /etc/docker/HAOS:/config \
--network=host \
home-assistant/home-assistant
```
应该不需要docker login

3.11 Update： **Docker容器类型的安装不支持Supervisor，Supervisor在后面安装中可能用到。**<br />**Jump to #虚拟机安装**<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/34376379/1678545221378-f85736ff-163f-4143-8a78-5ec1604f3d3e.png#averageHue=%23f7f7f7&clientId=u559e4d9c-996e-4&from=paste&height=457&id=uf609ab40&name=image.png&originHeight=737&originWidth=744&originalType=binary&ratio=1&rotation=0&showTitle=false&size=46308&status=done&style=none&taskId=u7835f03c-de38-4571-98ad-720cef0c3d8&title=&width=461)
<a name="AEzMH"></a>
### 网络：反向代理
可以用IP+端口访问网页，如果想使用域名访问网页需要使用反向代理。<br />以NGINX为例：
```shell
map $http_upgrade $connection_upgrade {
    default upgrade;
    ''      close;
}
server {
    listen 80;
    server_name example.cn; # 这里是反向代理的域名

    location / {
        proxy_pass http://127.0.0.1:8123;
        proxy_set_header Host $host;
        proxy_redirect http:// https://;
        proxy_http_version 1.1;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
    }
}
```
此处未开启SSL/TLS（即443端口https协议访问），如果要使用参考：<br />**在映射的configuration.yaml中，需要增加配置项**
```yaml
http:
	use_x_forwarded_for: true
	trusted_proxies:
		- 127.0.0.1      # Add the IP address of the proxy server  
			# You may also provide the subnet mask
```
trusted_proxies下方配置反向代理服务器的地址，如果是本机的反向代理服务则使用127.0.0.1，localhost疑似无法正确识别

启动后访问服务器ip:8123<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/34376379/1678109995310-8d695092-48bf-4db7-9c4b-ec38b4ff85f7.png#averageHue=%23f6f6f6&clientId=ue8bfa005-92d6-4&from=paste&height=298&id=fZHSZ&name=image.png&originHeight=332&originWidth=527&originalType=binary&ratio=1&rotation=0&showTitle=false&size=13239&status=done&style=none&taskId=udb9e9a13-e0f2-446b-b33c-6f6bb6ce571&title=&width=473)<br />[https://www.home-assistant.io/docs/configuration/](https://www.home-assistant.io/docs/configuration/)

---

米家设备支持绑定小米账号操作，其他品牌设备可能无法从公网通过HAOS访问：<br />所以尝试虚拟机安装：
<a name="O8zb6"></a>
## 安装：虚拟机
安装前：打开CPU虚拟化 （BIOS）<br />Virtual Box / VMware On Windows

不考虑Docker on Windows： 容器安装HAOS有限制（无法使用Supervisor）

**3.11 Update： 虚拟机安装问题（网络环境问题）**<br />需要访问8123端口，桥接后访问不到虚拟机的8123端口。桥接网络到实体机，使用官方所述的homeassistant.local:8123或localhost:8123或homeassistant:8123或IP:8123均无法访问。<br />使用`net info`查看HAOS的网络配置情况发现ETH0的IPv4及IPv6未能正确自动配置地址。转到[https://www.yuque.com/elysium-gigg0/lwng7m/hq71i207erihkaw2#aArqo](#aArqo)
<a name="aArqo"></a>
## 安装：树莓派[成功]
虚拟机网络环境配置复杂，switch to RasPi.<br />设备：Raspberry Pi 4B - 4GB RAM ver. - 64GB SD card

Step Changed：不使用balenaEtcher的“从URL刷入”功能，先使用科学上网从上方教程给出的Github链接下载镜像并解压，随后选择“从文件烧录”。

**3.08 Update: 网络环境问题**<br />问题在网络方面：没有路由器组建局域网，直接网线连接PC与树莓派，IPv4不能自动配置，IPv6可以自动配置，PC使用树莓派IPv6作为网关，手动配置IPv6地址网络适配界面提示已连接，homeassistant.local可以ping通，但8123无法访问，怀疑没有Internet连接，而HAOS可能需要联网进行一些配置或后续下载？（因为设备已经可以通过IPv6访问但是8123端口上的服务没有启动）<br />使用net update wlan0 提供加密方式ssid及密码可以连接到WiFi，访问IP:8123或其他可能的地址依然无法显示页面

**路由器到货 -> Switch to 路由器**<br />学校电信宽带用路由器设置比较麻烦，移动会比较容易

**3.12 Update: 由于宽带网络没有翻墙，所以在preparing环节下载过慢**<br />![屏幕截图 2023-03-12 225735.png](https://cdn.nlark.com/yuque/0/2023/png/25679654/1678633090896-cdf9391d-e826-4f12-b770-d94b5243ba76.png#averageHue=%23f0f0f0&clientId=ub874f907-75db-4&from=ui&height=427&id=ub4f4baa7&name=%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202023-03-12%20225735.png&originHeight=901&originWidth=658&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=77198&status=done&style=none&taskId=u9ca024dc-048d-40e7-a57f-8132cc5cca8&title=&width=312)
```
23-03-12 22:08:36 ERROR (MainThread) [asyncio] Task exception was never retrieved
future: <Task finished name='Task-1790' coro=<Repository.update() done, defined at /usr/src/supervisor/supervisor/store/repository.py:104> exception=StoreJobError("'GitRepo.pull' blocked from execution, no supervisor internet connection")>
Traceback (most recent call last):
File "/usr/src/supervisor/supervisor/store/repository.py", line 108, in update
await self.git.pull() File "/usr/src/supervisor/supervisor/jobs/decorator.py", line 116, in wrapper
raise self.on_condition(error_msg, _LOGGER.warning) from None
supervisor.exceptions.StoreJobError: 'GitRepo.pull' blocked from execution, no supervisor internet connection
```
**Workaround:**

- 给路由器装翻墙插件，但是比较麻烦，如果之前已经配置过了比较推荐这样做
- **找到了国内镜像站点** 
   - 与官网标准版的有些不同，内置了部分add-on

**国内镜像站点这个可用！不过百度云下载很慢，需要的话问我来要！**<br />**下面的步骤按这个来 **<br />账号：Capstone<br />密码：WKU12345(大写)<br />安装过程会自动识别在局域网内的设备
<a name="FraEc"></a>
### 配置HACS：用于下载米家 等插件

1. 配置 -> 开打高级模式 -> 加载项 ->Samba share 配置（这是个远程访问插件） -> 确认账号密码

![屏幕截图 2023-03-12 235204.png](https://cdn.nlark.com/yuque/0/2023/png/25679654/1678636370267-a728104a-80e4-49f3-9b7d-b85c36bc7467.png#averageHue=%23f9f9f9&clientId=u4b06b0cf-6ad6-4&from=ui&height=441&id=u8430866d&name=%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202023-03-12%20235204.png&originHeight=1189&originWidth=1882&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=89107&status=done&style=none&taskId=u172478b0-cd30-4354-9faa-0ee3930e969&title=&width=698.65625)

2. If you are on Windows you use \\<IP_ADDRESS>\, if you are on MacOS you use smb://<IP_ADDRESS> to connect to the shares. -> 用来访问树莓派里的haos
3. 下载hacs解压到 custom_components文件夹里
4. 开发者工具 -> 重新启动
5. 配置 -> 设备与服务->添加集成 -> 搜索HACS -> integrate 你的 github
<a name="N8zZX"></a>
### 在HACS中用MI IOT插件将米家连接到HA
~~目前还没有小米设备能给咱用。。。想想办法~~ 有米家台灯一个，可能还需要一个小爱音响测试ChatGPT方面<br />没有Apple Homekit设备
<a name="vSdyn"></a>
### 远程控制
人不在家，但仍然可以操作家庭内设备或使用内网搭建好的相关服务
<a name="mIjma"></a>
#### 用公网
查看路由WAN口ip是否与百度搜索IP得到的结果一致，若一致则有公网IP否则没有。若WAN口IP形如10.x.x.x，则没有。

1. 有公网ip，直接访问（端口转发） 转到[端口转发](#fMRuz)这一节。
2. 没有公网ip，内网穿透 （**但是需要一个中转服务器**）
   1. ~~Zerotier （~~**~~也需要服务器~~**~~）内网穿透方案之一 ~~采用FRP进行内网穿透
   2. 问题：需要在LAN中运行脚本或程序，所以要么是LAN中某设备不关机运行内网穿透（update: 树莓派本身即可），要么是树莓派想办法使用docker使用内网穿透容器。
      1. 尝试使用FRP，服务端部署完成。[Steps here](#FhFUV)
      2. ~~3.14 问题：~~~~从ssh打开docker，镜像pull失败（疑似镜像源在国外原因），更改镜像源尝试重启docker服务，发现systemctl命令不存在，service命令找不到docker compose服务和docker服务，尝试重启，重启后无法正常开机~~
      3. ~~尝试使用HomeAssistant add-on： tunnel2local，安装问题依然存在~~
         1. 问题原因依然是下载，看源码是从GitHub下载的，HA超时会报错
      4. 客户端通过SSH & Terminal插件，手动安装FRP并配置。[参考Server-side以及Client-side](#FhFUV)
3. ~~安装HACS插件后，可以搜索到molohub，直接用他们的服务 （这个比较快捷，如果前三个没操作过，推荐这个）教程：~~不彳亍，该插件的服务已经停止运行，开发组也换了
<a name="rJ1bT"></a>
#### 不用公网
直接在HA里把其他设备，连到homekit里<br />如果你的手机是iphone，在家里留一台ipad或者homepod，就可以远程控制。<br />缺点：限制比较大，HA里别的功能也不能远程操作了。而且设备要求多
<a name="FhFUV"></a>
#### FRP: Docker部署方式 Server-side
确保Docker以及Docker-compose已经安装<br />新建空文件夹来保存docker-compose.yml以及配置文件frps.ini
```shell
mkdir /root/docker-compose-data/frp/
cd /root/docker-compose-data/frp/
touch docker-compose.yml
touch frps.ini

nano docker-compose.yml
```
> nano是文本编辑器，使用vim或vi也可以

编辑`docker-compose.yml`
```yaml
version: '3.3'
services:
    frps:
        restart: always
        network_mode: host
        volumes:
            - '/root/docker-compose-data/frp/frps.ini:/etc/frp/frps.ini'
        container_name: frps
        image: snowdreamtech/frps:0.48.0
```
此处0.48.0是版本号，最好确保版本号与客户端使用的版本一致<br />修改`frps.ini`
```
[common]
bind_port = 7000
# 启用面板
dashboard_port = 4900
# 面板登录名和密码
dashboard_user = ASD
dashboard_pwd = SAMPLEPWD
# 自己的域名 (根据实际情况修改,可以不要)
subdomain_host = penetrate.yourdomain.top  
# 服务token(根据实际情况修改),相当于连接密码,建议设置，与客户端配置的必须一致
token = SAMPLETOKEN
```
不要直接复制其他教程的ini，**有些教程的注释与配置项在同一行，这样会识别为配置项的一部分！**<br />血泪教训，稍后客户端的frpc.ini同理，**千万不能把＃注释和配置项写在同一行**。很多教程都是写在同一行。<br />**注意服务器安全组放行上述对应端口（bind_port以及dashboard_port），如果使用了类似BTPanel等快速配置面板的服务器，注意在面板中放行对应端口。注意还需要放行frpc.ini中配置的remote_port端口！**
<a name="d869t"></a>
#### FRP: 手动部署方式 Client-side
尝试使用docker及docker-compose部署FRP失败，重启后CLI工作正常但是无法访问8123端口，FRP的add-on tunnel2local由于下载问题，商店无法直接安装，所以采用手动安装。_~~前提：镜像内需要有SSH & Terminal 插件来使用Linux命令行（HA的命令行是不能使用Linux相关命令的）~~_<br />**其实并不是一定要装terminal，手动解压之后利用samba传上去也可以（但是注意frp那个文件会被win识别成病毒自动删除，需要设置一下）**<br />跟随中客户端（树莓派）部分的引导配置客户端的FRP服务。**不要直接复制教程内的frpc.ini文件使用，注释不能在配置项同一行。**<br />**同时推荐打开日志输出：**
> 最好加一个重定向错误输出的参数，而且用全局变量最好，frpc.ini里面可以加一个日志输出，我这边用的frpc.ini:<br />[common]<br />server_addr = xxxxx<br />server_port = xxx<br />token = xxx

log_file = /config/frp/frp/log/frpc.log<br />log_level = info<br />log_max_days = 3

[HomeAssistant]<br />type = tcp<br />local_ip = 192.168.xx.xx<br />local_port = 8123<br />remote_port = xxxxx

然后命令是HA里面的configuration.yaml命令是:<br />shell_command:<br />frpc: nohup /config/frp/frp/frpc -c /config/frp/frp/frpc.ini >/config/frp/frp/log/1234.log 2>&1 & <br />这样不管是错误还是frp的日志都能看的很清楚

frpc.ini中配置的remote_port务必在服务器段配置安全组放行该端口。<br />**记得改一下这个shell命令中的路径为自己放置的frpc的路径**<br />如遇错误可以查看log定位，同时，也可以访问服务器端dashboard来查看是否有客户端连接：左侧Proxies -> TCP<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/34376379/1678962087209-f4120759-0ff2-4ba0-8c36-742ac7b7ac4a.png#averageHue=%23ead0af&clientId=ud8a442c1-a650-4&from=paste&height=241&id=u05667dca&name=image.png&originHeight=241&originWidth=1281&originalType=binary&ratio=1&rotation=0&showTitle=false&size=7346&status=done&style=none&taskId=uf7738b83-7117-430c-9813-7608548e025&title=&width=1281)<br />确认后可以访问ServerIP:remote_port查看本地的服务。
:::info
**如果遇到了各种不明原因无法启动frpc，注意看一下有没有实际运行那个shell命令，有时候HAOS很奇怪读不出那个config.yaml，那就需要自己手动运行下frpc**
:::
<a name="lxjHJ"></a>
## 语音及ChatGPT

This page displayed a workflow for a possible voice helper.<br />**语音助手集成还没有在HAOS中实现，需要寻找其他解决方案。**<br />**但是Conversation，Intent，tts或stt集成都可能对其他潜在解决方案有帮助。**

对于米家设备：小爱音响有可能的解决方案：

对于百度设备：小度音响可能的解决方案：但是百度设备不在SSR范围内，流程可以参考无需实现


<a name="fMRuz"></a>
## 从公网访问：端口转发
从公网访问的意义：人不在家，但仍然可以操作家庭内设备或使用内网搭建好的相关服务。<br />学校**电信宽带**闪讯拨号上网可以分配到公网IP，每一次拨号IP会换，每约24小时持续连接会自动重新拨号一次。<br />考虑以下设备连接方式<br />_因为想用路由器智能用移动宽带，但是移动没有分配公网ip -> _[远程控制](#vSdyn)<br />![](https://cdn.nlark.com/yuque/0/2023/jpeg/34376379/1678608304817-fd7b488a-d9d0-4c8f-b98c-9b37362a56ec.jpeg)<br />AP处接入互联网（公网）。HAOS所在设备需先经过路由再访问公网（HAOS不支持使用闪讯或PPPoE拨号上网），所以想从公网访问HAOS同理，公网IP只能定位到路由所在位置而不是HAOS所在位置。在路由内配置端口转发。<br />例如，访问X.X.X.X:8888 （X.X.X.X是路由的公网IP）时，将该端口的流量转发到内网192.168.1.2（HAOS内网IP）的8123端口上。<br />端口转发在路由管理中可以配置。<br />仅考虑学校拨号可获取公网IP的情况，在其他地区拨号可能无法获取公网IP（IPv4分配有限，人口设备密集区上级还有交换机，考虑内网穿透）<br />考虑公网IP配置域名：IP会变化域名不会，方便访问。考虑ddns服务，部分域名商有相关api，花生壳等有相关服务。需要配置路由或部署脚本到持续运行设备上。

<a name="edfRs"></a>
## 备份与恢复
<a name="L1CfG"></a>
### Windows
使用win32diskimager，新建一个空白文件，后缀为img，打开工具选中sd卡所在分区与该空白镜像。点击**读取**即可开始备份。<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/34376379/1678962619753-00448af1-2485-4c42-92fe-29dfb61b9dc3.png#averageHue=%23e8e8e8&clientId=ud8a442c1-a650-4&from=paste&height=225&id=u9a467b29&name=image.png&originHeight=342&originWidth=496&originalType=binary&ratio=1&rotation=0&showTitle=false&size=13067&status=done&style=none&taskId=u2f90f0a3-c87a-4d20-9539-fd443efa90d&title=&width=326)![image.png](https://cdn.nlark.com/yuque/0/2023/png/34376379/1678962697866-93519674-8720-41c3-9a86-9df3725e95d4.png#averageHue=%23e8e7e7&clientId=ud8a442c1-a650-4&from=paste&height=234&id=u38b27e73&name=image.png&originHeight=342&originWidth=496&originalType=binary&ratio=1&rotation=0&showTitle=false&size=17869&status=done&style=none&taskId=ue3194691-d1ee-449b-9747-21746a1db1e&title=&width=339)<br />缺点是全盘备份，**即SD卡有多大，镜像就大约有多大**。下一次烧录镜像到sd卡时，sd卡容量必须大于该镜像容量。提示读取成功即备份完成。64GB容量的sd卡备份镜像大小约58GB。<br />**不要勾选仅读取已分配分区。**实测备份出来镜像大小只有33MB，远不足刷入时的镜像大小。
<a name="D0gZe"></a>
### Linux【或Linux虚拟机】
下面这种方法我认为最稳妥也最方便，也有其他手动方法可以创建img文件。很多教程的备份是在树莓派官方系统的前提下，并且树莓派开机的情况下在树莓派本机上完成的。下面的方法是不依靠树莓派，使用读卡器读sd卡备份。
> 我使用的是VMware 16， Kali系统，分配磁盘空间最好大于两倍SD卡容量

首先打开终端，切换到root用户，列出挂载的所有磁盘
```shell
sudo su
[输入密码]

lsblk
```
连接sd卡与读卡器并插入设备，如果使用Linux虚拟机，注意设置该USB设备连接到虚拟机而不是主机（物理机）。确保该设备挂载（Kali中盘会出现在桌面且透明，说明没有挂载，双击即可挂载）后，重复上方命令，查看多出来的盘符。或前往/dev下方前后对比查看也可以。<br />盘符应该形如sdb。sda应该是默认本机的磁盘不是新挂载的。<br />随后开始创建**全盘镜像，大小将约为SD卡容量大小。**if后方是挂载的sd卡的盘符，of是生成的img文件目标地址，bs是块大小不必更改。
```shell
dd if=/dev/sdb of=./rpi.img bs=8M
```
需要等待一段时间，不要中断命令或关闭终端窗口。在此期间，新建一个终端窗口进行脚本下载，你也可以在目标目录使用ls -lh观察生成的img文件大小是否变化来判断创建镜像进程是否在正常运行。<br />脚本下载， 这个脚本将会把镜像中没有用的部分裁切掉。下载，更改权限，放入环境使其能在其他文件夹也能运行（可选）。
```shell
wget https://raw.githubusercontent.com/Drewsif/PiShrink/master/pishrink.sh
chmod +x pishrink.sh
sudo mv pishrink.sh /usr/local/bin
```
可能网络环境导致无法正常下载该脚本，对于VMware虚拟机，可以在宿主机上下载好直接拖放到虚拟机。<br />等待dd命令运行完成后，形如：![image.png](https://cdn.nlark.com/yuque/0/2023/png/34376379/1678987141560-4a7d9e43-9980-4474-9e67-4540cfc9a8ec.png#averageHue=%23272b37&clientId=u9a7f5165-d9a2-4&from=paste&height=66&id=u07f59356&name=image.png&originHeight=66&originWidth=495&originalType=binary&ratio=1&rotation=0&showTitle=false&size=16971&status=done&style=none&taskId=ud592358f-2bc4-4e55-8fc0-7687f587230&title=&width=495)<br />在终端中使用PiShrink
```shell
sudo pishrink.sh [原镜像地址] [新镜像地址]
```
该命令会先复制原镜像到新镜像目录随后进行裁剪。随后等待命令运行完成即可获得压缩后的镜像。<br />原镜像约58GB，裁剪后约8GB。<br />**使用Windows方法创建的镜像也可以用这种方法减小体积。**
<a name="aGCWZ"></a>
### 恢复
使用Win32diskImager，步骤如Windows节中，选中后点击**写入**即可。烧录的镜像可能需要重新分配磁盘。
<a name="RogXR"></a>
### IMAGE
创建镜像的用处在于出现错误配置或需要转移设备或存储容器时，可以最快速度恢复服务。<br />这是一份可用的镜像，配置好了Dev log中提到的绝大多数客户端**基础**内容。3.17更新<br />如果遇到内网穿透服务未启动情况，请参考上方相关章节。<br />链接：[https://pan.baidu.com/s/13SJGUc1jbu7lTPEwuVjw3w?pwd=HASS](https://pan.baidu.com/s/13SJGUc1jbu7lTPEwuVjw3w?pwd=HASS) <br />提取码：HASS <br />--来自百度网盘超级会员V5的分享

<a name="iPQ8R"></a>
## 小爱同学接入ChatGPT
搞到一台小爱音箱，然后按照[https://github.com/yihong0618/xiaogpt](https://github.com/yihong0618/xiaogpt)里面的视频教程走就可以了<br />过程中遇到了一些小问题：<br />1.视频教程中显示的配置ChatGPT的Github链接在readme里被删掉了，应该是[https://github.com/acheong08/ChatGPT](https://github.com/acheong08/ChatGPT)<br />2.安装项目时用的pip指令报错“python setup.py egg_info did not run successfully”，一方面是pip版本太低，可用pip install --upgrade pip,pip install --upgrade setuptools,pip install ez_setup三个指令升级一下版本，还不行的话就试试直接安装zip包：pip3 install miservice.zip<br />3.因为教程里给的是Mac OS 或 Linux的命令，在Windows里没法用，所以要把export改成set，查询设备DID时的micli.py list改用Python3 ./micli.py list<br />4.用set设置环境变量时注意要在下一级目录里，设置完之后的命令返回上一级文件目录执行<br />5.给小爱音箱配网没法用学校的Wifi，可以开个手机热点<br />6.需要小米的账号和ChatGPT的账号，需要用电脑的蓝牙连上小爱音箱

---
## Lovelace定制界面
找了多篇教程，最终决定使用Homekit Infused实现主题效果，其UI的效果演示如视频https://www.bilibili.com/video/BV1uF411z7rg/?spm_id_from=333.337.search-card.all.click&vd_source=f0d7d70133f9043694a4bcb05174541e, 而其教程就在视频简介中有提及分为文字指南和视频教程都可以去了解一下这里就不多提。其中我们需要进入jimz011的github(https://jimz011.github.io/homekit-infused/)下载相关的源码并做好Home Assistant中的插件的准备工作，插件的准备都可以在HACS中完成对照作者给出的要求表已经下载完成了。源码根据视频教程中的步骤去粘贴相应文件到我们自己的config文件中，作者jimz011也给出了相应的步骤如图![image](https://user-images.githubusercontent.com/116329733/227723792-ea167018-083d-4401-8782-2dbcfdd800d4.png)note中提及的两个文件我们暂且复制进去，有需要我会删除这两个选文件


<a name="mLWxz"></a>
# TODO:

- [ ] 测试家具
- [ ] 定制界面
- [ ] 自动化:
- [ ] configuration
- [x] 远程控制
- [x] 内网穿透
- [x] FRP
- [x] Server side
- [x] Client side
- [ ] 反向代理
- [x] ~~Molohub ~~Deprecated: 该add-on的服务已停止运行
- [x] 树莓派 创建镜像与备份
- [ ] ChatGPT
- [ ] xiaoGPT部署
- [ ] 搞到一个小爱音响
- [ ] HA integration

