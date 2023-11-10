# filesystem_analysis.py
import os
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# Pandas 用於數據處理，安裝方法：pip install pandas
# Matplotlib 用於繪圖，安裝方法：pip install matplotlib
'''
powershell
- pip list | Select-String pandas
cmd
- pip list | findstr pandas
'''

def read_csv_files(path):
    all_data = {}
    for file in os.listdir(path):
        if file.endswith('.csv'):
            full_path = os.path.join(path, file)
            df = pd.read_csv(full_path)
            # 從檔名提取日期
            date_str = os.path.splitext(file)[0][:8]
            date = datetime.strptime(date_str, '%Y%m%d')
            df['Date'] = date
            # 假設 IP 地址在 'IP' 列中
            for ip in df['IP'].unique():
                ip_df = df[df['IP'] == ip]
                if ip not in all_data:
                    all_data[ip] = []
                all_data[ip].append(ip_df)
    return all_data

import numpy as np

def analyze_and_plot(all_data):
    for ip, data_list in all_data.items():
        # 合併該 IP 地址的所有 DataFrame
        data = pd.concat(data_list)
        # 確保日期是排序的
        data = data.sort_values(by='Date')

        # 轉換 Size、Used 和 Avail 列為數值型，並假設它們是以 G 為單位
        data['Size'] = pd.to_numeric(data['Size'].str.replace('G', ''), errors='coerce')
        data['Used'] = pd.to_numeric(data['Used'].str.replace('G', ''), errors='coerce')
        data['Avail'] = pd.to_numeric(data['Avail'].str.replace('G', ''), errors='coerce')

        # 計算使用百分比
        data['Used%'] = (data['Used'] / data['Size']) * 100

        # 創建一個圖表
        fig, ax1 = plt.subplots(figsize=(10, 6))
        
        # 繪製折線圖
        ax1.plot(data['Date'], data['Used'], label='Used Capacity (GB)')
        ax1.plot(data['Date'], data['Avail'], label='Available Capacity (GB)')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Capacity (GB)')
        
        # 添加第二個 y 軸用於百分比長條圖
        ax2 = ax1.twinx()
        ax2.set_ylabel('Usage %')
        
        # 繪製長條圖
        bar_colors = np.where(data['Used%'] > 80, 'orange', 'blue')
        ax2.bar(data['Date'], data['Used%'], color=bar_colors, alpha=0.3)

        plt.title(f'Capacity Usage for IP: {ip}')
        ax1.legend(loc='upper left')

        # plt.savefig(f'/path/to/save/graphs/Capacity_Usage_{ip}.png')
        plt.show()

def dev_main(path):
    '''
    all_data = read_csv_files(path)
    print(all_data)
    analyze_and_plot(all_data)
    '''
    all_data = read_csv_files(path)
    print("Available IPs: ", list(all_data.keys()))
    selected_ip = input("Enter an IP to plot (leave empty to plot all): ").strip()

    if selected_ip:
        if selected_ip in all_data:
            analyze_and_plot({selected_ip: all_data[selected_ip]})
        else:
            print(f"IP {selected_ip} not found.")
    else:
        analyze_and_plot(all_data)

# 確保其他函數 (read_csv_files, analyze_and_plot) 依然在代碼中


if __name__ == "__main__":
    dev_main(".\DF-Hcsv")
