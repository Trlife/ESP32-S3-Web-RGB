 ESP32-S3 Web RGB 无线控制灯

这是一个基于 ESP32-S3 开发板的微型物联网项目。通过简单的 MicroPython 代码，将 ESP32 变成一个微型 Web 服务器，使用手机或电脑浏览器即可在局域网内控制板载 RGB 灯的颜色。

✨ 功能特点
- 纯离线运行，无需连接外网云端。
- 局域网内手机 Web 网页一键控制。
- 包含异常处理机制（防止程序崩溃导致硬件卡死）。

🛠️ 硬件清单
- 主控板：ESP32-S3 (N16R8 版本，带 8MB PSRAM)
- RGB灯珠：板载 WS2812 (连接 IO48 引脚)
- 一根能传输数据的 Type-C 线

🚀 快速上手教程

1. 烧录固件
使用 Thonny 或官方 Flash Download Tool 为 ESP32-S3 烧录 MicroPython 固件。
⚠️ 避坑警告：如果你的板子带有 Octal-SPIRAM（如 N16R8），请务必下载带有 'SPIRAM_OCT' 后缀的固件（如 'ESP32_GENERIC_S3-SPIRAM_OCT-.bin'），否则会报 PSRAM 初始化错误。

2. 修改并运行代码
将 'main.py' 代码下载到本地，修改其中的 'SSID' 和 'PASSWORD' 为你自己的 Wi-Fi 信息。
⚠️ 避坑警告：ESP32 仅支持 2.4G Wi-Fi。如果你用手机开热点，请确保开启了“最大兼容性”或强制设为 2.4GHz 频段。

3. 开始控制
运行代码后，在 Thonny 的串口终端中查看 ESP32 获取的局域网 IP 地址（例如 '192.168.43.12'）。在连着同一 Wi-Fi 的手机浏览器中输入该 IP 地址，即可看到控制页面。

🐛 踩坑记录与解决（新手必看）
1. 无法识别端口：检查是否安装了 'CP2102'或 'CH340' 驱动。
2. 烧录一直报错 'invalid header'：尝试按住板子上的 BOOT 键，再按一下 RST 键，进入下载模式。
3. 网页点击关灯卡顿/提示网络错误：在 HTTP 响应头中加入 'Connection: close'，并加入 'time.sleep(0.1)' 让数据发送完毕后再断开连接。

📄 开源协议
本项目基于 MIT License 开源。