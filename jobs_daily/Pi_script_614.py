#!/usr/bin/python3
'''
sudo nano /etc/lightdm/lightdm.conf
xserver-command=X -s 0 -dpms
sudo reboot

crontab -e
@reboot /usr/bin/python3 /home/finley/script.py >> /home/finley/logfile.log 2>&1
0 */6 * * * sudo reboot
'''

import requests
import time
import threading
import Adafruit_DHT
import RPi.GPIO as GPIO

# 傳送至 ThingSpeak
def send_to_thingspeak(temperature, humidity):
    api_key = ''  # 替換為您的 ThingSpeak 寫入 API Key
    base_url = 'https://api.thingspeak.com/update'
    payload = {
        'api_key': api_key,
        'field1': temperature,
        'field2': humidity
    }
    try:
        response = requests.get(base_url, params=payload, timeout=10)
        print(f"ThingSpeak response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending to ThingSpeak: {e}")

# 傳送至 LINE Notify
def send_to_line(temperature, humidity, light_status):
    line_token = ""  # 替換為你的 LINE Notify 令牌
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_token}'}
    light_message = "燈光已關閉。" if not light_status else "燈光已開啟。"
    #light_message = "燈光已開啟。" if light_status else "燈光未開啟。"
    message = f"A5-614 溫度: {temperature}°C 濕度: {humidity}%。{light_message}詳細資料: https://thingspeak.com/channels/2331423/charts/1?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&type=line&update=15"
    data = {'message': message}
    
    try:
        response = requests.post(line_notify_api, headers=headers, data=data, timeout=10)
        print(f"LINE response: {response.text}")  # 這行在正式運行時也可註釋掉
    except requests.exceptions.RequestException as e:
        print(f"Error sending LINE notification: {e}")

'''
# 替換下面的函數為實際發送數據到ThingSpeak和LINE的函數
def send_to_thingspeak(temperature, humidity):
    pass  # 實際的代碼來發送數據到ThingSpeak

def send_to_line(message):
    pass  # 實際的代碼來發送訊息到LINE
'''

class TemperatureMonitor:
    def __init__(self, sensor=Adafruit_DHT.DHT22, pin=4, light_sensor_pin=18, threshold=26, interval=60):
        self.sensor = sensor
        self.pin = pin
        self.light_sensor_pin = light_sensor_pin
        self.threshold = threshold
        self.interval = interval
        self.last_alert_time = None
        self.light_on = False

        # 設置光敏電阻模組的GPIO模式
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.light_sensor_pin, GPIO.IN)

    def read_temperature_humidity(self):
        # 讀取溫濕度值
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
        return temperature, humidity

    def check_light_status(self):
        # 檢測光敏電阻模組狀態
        while True:
            new_light_on = not GPIO.input(self.light_sensor_pin)  # 假設輸入為低電平表示燈亮
            if new_light_on != self.light_on:
                # 當光照狀態發生變化時列印狀態
                self.light_on = new_light_on
                print(f"光狀態變化: {'開' if self.light_on else '關'}")  # 正式使用時可以註釋掉
            time.sleep(1)  # 每秒檢查一次

    def send_data(self):
        # 定期發送數據
        while True:
            temperature, humidity = self.read_temperature_humidity()
            if temperature is not None and humidity is not None:
                send_to_thingspeak(temperature, humidity)
            time.sleep(self.interval)

    def monitor_environment(self):
        # 環境監控
        while True:
            temperature, humidity = self.read_temperature_humidity()
            if temperature is not None and temperature > self.threshold or self.light_on:
                current_time = time.time()
                if self.last_alert_time is None or current_time - self.last_alert_time > 600:  # 10分钟
                    # 调用send_to_line函数并传递温度、湿度和照明状态
                    send_to_line(temperature, humidity, self.light_on)
                    # 打印日志消息
                    print(f"發送警報: 溫度: {temperature}°C 濕度: {humidity}%，燈光已開啟。")  # 正式使用时可以注释掉
                    self.last_alert_time = current_time

    def start(self):
        # 開始監控
        threading.Thread(target=self.send_data).start()
        threading.Thread(target=self.monitor_environment).start()
        threading.Thread(target=self.check_light_status).start()

# 主程序入口
if __name__ == "__main__":
    monitor = TemperatureMonitor()
    monitor.start()

'''
+-----+------------------+---------------+--------------------------------+
| PIN | Raspberry Pi 3   | Sensor        | Description                    |
+-----+------------------+---------------+--------------------------------+
|   1 | 3.3V             | DHT22         | Power supply for DHT22 sensor  |
|   2 | 5V               | Light Sensor  | Power supply for Light Sensor  |
|   4 | GPIO 4 (BCM)     | DHT22         | Data input for DHT22 sensor    |
|  12 | GPIO 18 (BCM)    | Light Sensor  | Digital output for light level |
| GND | Ground           | DHT22         | Ground for DHT22 sensor        |
| GND | Ground           | Light Sensor  | Ground for Light Sensor        |
+-----+------------------+---------------+--------------------------------+


+-----+-----+---------+------+---+---Pi 3---+---+------+---------+-----+-----+
| BCM | wPi |   名稱  | Mode | V | Physical | V | Mode |   名稱  | wPi | BCM |
+-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
|     |     |    3.3v |      |   |  1 || 2  |   |      |    5v   |     |     |
|   2 |   8 |   SDA.1 | ALT0 | 1 |  3 || 4  |   |      |    5v   |     |     |
|   3 |   9 |   SCL.1 | ALT0 | 1 |  5 || 6  |   |      |    0v   |     |     |
|   4 |   7 | GPIO. 7 |   IN | 1 |  7 || 8  | 1 | ALT0 | TxD.1   | 15  | 14  |
|     |     |      0v |      |   |  9 || 10 | 1 | ALT0 | RxD.1   | 16  | 15  |
|  17 |   0 | GPIO. 0 |   IN | 0 | 11 || 12 | 0 | IN   | GPIO. 1 | 1   | 18  |
|  27 |   2 | GPIO. 2 |   IN | 0 | 13 || 14 |   |      |    0v   |     |     |
|  22 |   3 | GPIO. 3 |   IN | 0 | 15 || 16 | 0 | IN   | GPIO. 4 | 4   | 23  |
|     |     |    3.3v |      |   | 17 || 18 | 0 | IN   | GPIO. 5 | 5   | 24  |
|  10 |  12 |   MOSI. | ALT0 | 0 | 19 || 20 |   |      |    0v   |     |     |
|   9 |  13 |   MISO. | ALT0 | 0 | 21 || 22 | 0 | IN   | GPIO. 6 | 6   | 25  |
|  11 |  14 |   SCLK. | ALT0 | 0 | 23 || 24 | 1 | ALT0 | CE0.    | 10  |  8  |
|     |     |      0v |      |   | 25 || 26 | 1 | ALT0 | CE1.    | 11  |  7  |
|   0 |  30 |   SDA.0 | ALT0 | 1 | 27 || 28 | 1 | ALT0 | SCL.0   | 31  |  1  |
|   5 |  21 | GPIO.21 |   IN | 1 | 29 || 30 |   |      |    0v   |     |     |
|   6 |  22 | GPIO.22 |   IN | 0 | 31 || 32 | 0 | IN   | GPIO.26 | 26  | 12  |
|  13 |  23 | GPIO.23 |   IN | 0 | 33 || 34 |   |      |    0v   |     |     |
|  19 |  24 | GPIO.24 |   IN | 0 | 35 || 36 | 0 | IN   | GPIO.27 | 27  | 16  |
|  26 |  25 | GPIO.25 |   IN | 0 | 37 || 38 | 0 | IN   | GPIO.28 | 28  | 20  |
|     |     |      0v |      |   | 39 || 40 | 0 | IN   | GPIO.29 | 29  | 21  |
+-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+

'''