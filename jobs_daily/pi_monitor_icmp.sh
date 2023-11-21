# @reboot /bin/bash /home/您的用戶名/pi_monitor.sh >> /var/log/pi_monitor.log 2>&1
# sudo touch /var/log/pi_monitor.log

#!/bin/bash

# 設定目標 Raspberry Pi 的 IP 地址
PI_HOSTS=("192.168.1.10" "192.168.1.11") # 更改為您的 Raspberry Pi IP 地址

# 設定檢查間隔時間（秒）
CHECK_INTERVAL=300

# 設定您的 LINE Notify Token
LINE_TOKEN="YOUR_LINE_TOKEN" # 將 YOUR_LINE_TOKEN 替換成您的 Token

# 發送 LINE 通知的函數
send_line_notify() {
    local message=$1
    curl -X POST -H "Authorization: Bearer $LINE_TOKEN" -F "message=$message" https://notify-api.line.me/api/notify
}

# 無限循環執行檢查
while true; do
    for HOST in "${PI_HOSTS[@]}"; do
        # 使用 ping 命令檢查 Raspberry Pi 是否在線
        if ping -c 1 $HOST &> /dev/null; then
            echo "$HOST is online"
        else
            echo "$HOST is offline"
            # 發送 LINE 通知
            send_line_notify "$HOST is offline"
        fi
    done

    # 等待設定的間隔時間後再次檢查
    sleep $CHECK_INTERVAL
done
