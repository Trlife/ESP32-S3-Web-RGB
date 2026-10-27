import network
import socket
import time
from machine import Pin
from neopixel import NeoPixel

# 1. 硬件初始化
pin = Pin(48, Pin.OUT)
np = NeoPixel(pin, 1)
np[0] = (0, 0, 0)
np.write()

# 2. WiFi 配置
SSID = "You_Wifi_Name"      # 改成你的 2.4G WiFi 名字
PASSWORD = "You_Password"  # 改成你的密码

# 3. 连接 WiFi
def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('正在连接网络...')
        np[0] = (0, 0, 255) # 蓝灯闪烁表示连接中
        np.write()
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            pass
    print('网络连接成功！IP地址:', wlan.ifconfig()[0])
    np[0] = (0, 255, 0) # 绿灯常亮表示连接成功
    np.write()
    return wlan.ifconfig()[0]

# 4. 启动 Web 服务器
ip = connect()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80)) # 监听 80 端口
s.listen(5)
print(f"请用手机浏览器访问: http://{ip}")

# 5. 死循环等待接收指令
try:
    while True:
        conn, addr = s.accept()
        request = conn.recv(1024).decode('utf-8')
        
        # 1. 处理浏览器请求图标（favicon.ico）的情况
        if 'GET /favicon.ico' in request:
            conn.close()
            continue
            
        # 2. 判断开灯/关灯指令
        if 'GET /on' in request:
            np[0] = (255, 0, 0)
            np.write()
            print("收到指令：开灯")
            response = "OK: Light ON"
        elif 'GET /off' in request:
            np[0] = (0, 0, 0)
            np.write()
            print("收到指令：关灯")
            response = "OK: Light OFF"
        else:
            response = "ESP32 Server is Running!"
            
        # 3. 网页响应头
        html = f"""HTTP/1.1 200 OK
Content-Type: text/html
Connection: close

<h1>{response}</h1>
<a href="/on">点我开灯</a><br><br>
<a href="/off">点我关灯</a>
"""
        conn.send(html)
        
        # 4.等待网页反应 
        time.sleep(0.1) 
        conn.close()

except KeyboardInterrupt:
    # 就算被强杀，也要关灯（虽然大概率被底层重置）
    print("服务器关闭")
    np[0] = (0, 0, 0)
    np.write()
    s.close()