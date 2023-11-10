#!/usr/bin/python3
'''
crontab -e
@reboot /usr/bin/python3 /home/finley/script.py >> /home/finley/logfile.log 2>&1
0 */6 * * * sudo reboot
'''

import Adafruit_DHT
import requests
import time

# 測試數據
def test_data():
    return 25, 50  # 假設的溫度和濕度

# 讀取 DHT11 數據
# def read_dht11():
def read_dht22():
    # sensor = Adafruit_DHT.DHT11
    sensor = Adafruit_DHT.DHT22
    gpio_pin = 4
    humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio_pin)
    if humidity is not None and temperature is not None:
        return temperature, humidity
    else:
        print("Failed to get reading from the sensor.")
        return None, None

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
def send_to_line(temperature, humidity):
    line_token = ""  # 替換為你的 LINE Notify 令牌
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_token}'}
    #message = f"Temperature: {temperature}°C, Humidity: {humidity}%"
    message = f"溫度: {temperature}°C 濕度: {humidity}%。詳細資料: https://thingspeak.com/channels/2327006/charts/1?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&type=line&update=15"
    data = {'message': message}
    try:
        response = requests.post(line_notify_api, headers=headers, data=data, timeout=10)
        print(f"LINE response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending LINE notification: {e}")

# 主程式
def main():
    last_alert_time = None

    while True:
        # 使用真實數據 - 從 DHT11 讀取
        # temperature, humidity = read_dht11()
        temperature, humidity = read_dht22()

        # 或者使用測試數據 - 解除下一行的註解並註解掉上一行
        # temperature, humidity = test_data()

        if temperature is not None and humidity is not None:
            # send_to_line(temperature, humidity)
            send_to_thingspeak(temperature, humidity)
            # print(f"Temperature: {temperature}°C, Humidity: {humidity}%")

            # 處理溫度過高的警告
            if temperature > 25:
                current_time = time.time()
                if last_alert_time is None or current_time - last_alert_time > 600:  # 10 分鐘
                    send_to_line(temperature, humidity)
                    last_alert_time = current_time
            else:
                last_alert_time = None  # 重置警告時間
        time.sleep(60)  # 每 60 秒執行一次

if __name__ == "__main__":
    main()
'''
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