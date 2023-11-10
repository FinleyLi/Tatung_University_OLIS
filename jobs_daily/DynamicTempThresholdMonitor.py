import math
import time

def calculate_dynamic_threshold(t, delta_T, delta_T_max, k):
    """
    計算動態溫度閾值。

    參數:
    t -- 從溫度跳變檢測開始的時間。
    delta_T -- 正常操作溫度範圍的一半寬度。
    delta_T_max -- 當檢測到溫度瞬間跳動時，閾值應該達到的最大值。
    k -- 正的比例常數，它決定了閾值恢復到 delta_T 的速率。
    """
    return delta_T + (delta_T_max - delta_T) * math.exp(-k * t)

# 這部分代碼檢查當前是否為主程序的運行，並不是被另一個文件導入時運行。
if __name__ == "__main__":
    # 程序開始時刻的時間戳
    start_time = time.time()
    
    # 初始參數設定
    delta_T = 3         # 正常操作溫度範圍的一半寬度為 3 度
    delta_T_max = 10    # 最大溫度閾值為 10 度
    k = 0.1             # 比例常數

    # TODO: 使用 DHT22 傳感器獲取溫度數據
    # temperature = read_temperature_from_DHT22()

    while True:
        # 獲取系統當前時間
        current_time = time.time()
        # 計算從溫度跳變檢測開始到現在的時間
        time_since_jump = current_time - start_time

        # 計算當前的動態溫度閾值
        dynamic_threshold = calculate_dynamic_threshold(time_since_jump, delta_T, delta_T_max, k)
        
        # 打印當前時間的動態溫度閾值
        print(f"當前動態閾值: {dynamic_threshold:.2f} 度")
        time.sleep(1)  # 每秒更新一次
