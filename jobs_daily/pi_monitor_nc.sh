# @reboot /bin/bash /home/您的用戶名/pi_monitor.sh >> /var/log/pi_monitor.log 2>&1
# sudo touch /var/log/pi_monitor.log
# sudo chown $USER /var/log/pi_monitor.log

# nohup /home/您的用戶名/pi_monitor.sh &
# tail -f nohup.out
# ps aux | grep pi_monitor.sh
## ps -ef | grep pi_monitor.sh
## kill -9 PID

# tail -f /var/log/pi_monitor.log

# sudo apt install netcat-openbsd
# --------------------------------------------------

# sudo nano /etc/lightdm/lightdm.conf
# xserver-command=X -s 0 -dpms

#!/bin/bash

# 設定目標主機及其對應的端口
declare -A HOSTS
HOSTS["192.168.1.10"]=443 #ttucis
HOSTS["192.168.1.11"]=3389 #EDOC
HOSTS["192.168.1.12"]=80 #tshcis

# 設定檢查間隔時間（秒）
CHECK_INTERVAL=300

# 設定您的 LINE Notify Token
LINE_TOKEN="YOUR_LINE_TOKEN" # 將 YOUR_LINE_TOKEN 替換成您的 Token

# 時間戳記
timestamp() {
    local date_format=$1
    echo "$(date +"%Y-%m-%d %H:%M:%S")"
}

# 發送 LINE 通知的函數
send_line_notify() {
    local message=$1
    curl -X POST -H "Authorization: Bearer $LINE_TOKEN" -F "message=$message" https://notify-api.line.me/api/notify
}

# 無限循環執行檢查
while true; do
    echo "$(timestamp) Start checking..."
    for HOST in "${!HOSTS[@]}"; do
        PORT=${HOSTS[$HOST]}
        #echo "$(timestamp) Checking $HOST port $PORT"
        # 使用 nc 命令檢查主機的端口是否開放
        if nc -zv $HOST $PORT &> /dev/null; then
            echo "$HOST port $PORT is open"
        else
            echo "$HOST port $PORT is closed or host is down"
            # 發送 LINE 通知
            send_line_notify "$HOST port $PORT is closed or host is down"
        fi
    done

    # 等待設定的間隔時間後再次檢查
    sleep $CHECK_INTERVAL
done
