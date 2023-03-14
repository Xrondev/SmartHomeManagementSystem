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
此处未开启SSL/TLS（即443端口https协议访问），如果要使用参考：<br />在映射的configuration.yaml中，需要增加配置项
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

1. 有公网ip，直接访问（端口转发） 转到[端口转发](#fMRuz)这一节。
2. 内网穿透 （**但是需要一个中转服务器**）
   1. Zerotier （**也需要服务器**）内网穿透方案之一
   2. 问题：需要在LAN中运行脚本或程序，所以要么是LAN中某设备不关机运行内网穿透，要么是树莓派想办法使用docker使用内网穿透容器。
3. 安装HACS插件后，可以搜索到molohub，直接用他们的服务 （这个比较快捷，如果前三个没操作过，推荐这个）教程：
<a name="rJ1bT"></a>
#### 不用公网
直接在HA里把其他设备，连到homekit里<br />如果你的手机是iphone，在家里留一台ipad或者homepod，就可以远程控制。<br />缺点：限制比较大，HA里别的功能也不能远程操作了。而且设备要求多
<a name="lxjHJ"></a>
## 语音及ChatGPT

This page displayed a workflow for a possible voice helper.<br />**语音助手集成还没有在HAOS中实现，需要寻找其他解决方案。**<br />**但是Conversation，Intent，tts或stt集成都可能对其他潜在解决方案有帮助。**

对于米家设备：小爱音响有可能的解决方案：

对于百度设备：小度音响可能的解决方案：但是百度设备不在SSR范围内，流程可以参考无需实现


<a name="fMRuz"></a>
## 从公网访问：端口转发
从公网访问的意义：人不在家，但仍然可以操作家庭内设备或使用内网搭建好的相关服务。<br />学校**电信宽带**闪讯拨号上网可以分配到公网IP，每一次拨号IP会换，每约24小时持续连接会自动重新拨号一次。<br />考虑以下设备连接方式<br />_因为想用路由器智能用移动宽带，但是移动没有分配公网ip -> _[远程控制](#vSdyn)<br />![](https://cdn.nlark.com/yuque/0/2023/jpeg/34376379/1678608304817-fd7b488a-d9d0-4c8f-b98c-9b37362a56ec.jpeg)<br />AP处接入互联网（公网）。HAOS所在设备需先经过路由再访问公网（HAOS不支持使用闪讯或PPPoE拨号上网），所以想从公网访问HAOS同理，公网IP只能定位到路由所在位置而不是HAOS所在位置。在路由内配置端口转发。<br />例如，访问X.X.X.X:8888 （X.X.X.X是路由的公网IP）时，将该端口的流量转发到内网192.168.1.2（HAOS内网IP）的8123端口上。<br />端口转发在路由管理中可以配置。<br />仅考虑学校拨号可获取公网IP的情况，在其他地区拨号可能无法获取公网IP（IPv4分配有限，人口设备密集区上级还有交换机，考虑内网穿透）<br />考虑公网IP配置域名：IP会变化域名不会，方便访问。考虑ddns服务，部分域名商有相关api，花生壳等有相关服务。需要配置路由或部署脚本到持续运行设备上。

---

<a name="mLWxz"></a>
# TODO:

- [ ] 测试家具
- [ ] 定制界面
- [ ] 自动化:
- [ ] configuration
- [ ] 远程控制
- [ ] 内网穿透
- [ ] Molohub
- [ ] ChatGPT
- [ ] xiaoGPT部署
- [ ] 搞到一个小爱音响
- [ ] HA integration

