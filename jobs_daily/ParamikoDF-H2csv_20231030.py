import paramiko, datetime, csv, base64, os
import pandas as pd

# 切換工作目錄到相對路徑 ".\env311"
os.chdir(".\Env3116")

command = "df -H /"

# 讀取CSV檔案並回傳一個字典，鍵為CSV的第一列，值是(username, password)的陣列
def read_credentials_from_csv(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # 跳過標題列
        credentials = {}
        for row in reader:
            key, username, password = row
            credentials[key] = (username, password)
    return credentials

def read_hostnames_from_csv(filename):
    host_data = {}
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # 跳過標題列
        for row in reader:
            key = row[0]
            port = int(row[1])
            hosts = [hostname for hostname in row[2:] if hostname]
            host_data[key] = (port, hosts)
    return host_data

credentials = read_credentials_from_csv("account.csv")
host_data = read_hostnames_from_csv("hostname.csv")

# 可以透過key來取得相應的帳號和密碼
# username, password = credentials["default"]

# 創建目標文件夾的相對路徑
output_folder = ".\DF-Hcsv"
'''
# 檢查目標文件夾是否存在，如果不存在就創建
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
'''
# 使用相對路徑設定輸出文件的路徑
output_file_path = os.path.join(output_folder, f'{datetime.datetime.now().strftime("%Y%m%d%H")}.txt')

# 創建並寫入文件
with open(output_file_path, 'w') as f:
#with open(f'{datetime.datetime.now().strftime("%Y%m%d%H")}.txt', 'w') as f:
    for key, data in host_data.items():
        port, hosts = data

        # 取得Base64編碼的用戶名和密碼
        encoded_username, encoded_password = credentials[key]
        
        # 進行Base64解碼
        username = base64.b64decode(encoded_username).decode('utf-8')
        password = base64.b64decode(encoded_password).decode('utf-8')

        for host in hosts:
            client = paramiko.client.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(host, username=username, password=password, port=port)

            # Make SSH session client
            ssh_session = client.get_transport().open_session()
            ssh_session.exec_command(command)
            output = ssh_session.recv(1024)

            f.write(f'{host}\n{output.decode()}\n')
            ssh_session.close()
            client.close()

# Read the text file
with open(output_file_path, 'r') as f:
#with open(f'{datetime.datetime.now().strftime("%Y%m%d%H")}.txt', 'r') as f:
    data = f.read()

# 解析文本
lines = data.strip().split("\n")
rows = []

for i in range(0, len(lines), 4):
    ip = lines[i]
    fs_info = lines[i+2].split()
    row = [ip] + fs_info
    rows.append(row)

# convert to DataFrame
df = pd.DataFrame(rows, columns=["IP", "Filesystem", "Size", "Used", "Avail", "Use%", "Mounted on"])

# insert a new column
df["Host"] = ["",]
# 使用str.split方法分割網址列取得主機名
# df['Host'] = df['IP'].str.split('.').str[-1]

# 將"Host"移動到第0列
cols = df.columns.tolist()
cols = ['Host'] + cols[:-1]
df = df[cols]
print(df)
df = df.sort_values(by='IP')

# 使用相對路徑設定輸出CSV文件的路徑
csv_file_path = os.path.join(output_folder, f'{datetime.datetime.now().strftime("%Y%m%d%H%M")}.csv')
# 將DataFrame寫入CSV文件
df.to_csv(csv_file_path, index=False)
# Save the DataFrame to a CSV file
#df.to_csv(f'{datetime.datetime.now().strftime("%Y%m%d%H%M")}.csv', index=False)

'''
 * Program Name: Paramiko remote server disk space check.
 * Subject: "Paramilo to use command "df -H /", "Save as CSV".
 * Input: ssh server IP, username, password, port & session.exec_command('df -H /').
 * Output: ./"%Y%m%d%H%M.csv".
 * Since 2023/10/11
 * 2023/10/11, add subprocess CSV convert. 
 * 2023/10/12, auto search server disk by different password
 * 2023/10/20, account & password useing csv file, and file useing base64 encode.
 * 2023/10/30, chdir to Env311, and add relative path.
 * ToolKit: VS Code 1.83.1, Python 3.11.0
 * Author: Finley
 *         Computer Center, Tatung University

if __name__ == '__main__':
    # add main function in here
    print("    __ _       _                                        \n");
    print("   / _(_)_ __ | | ___ _   _                             \n");
    print("  | |_| |  _  | |/ _   | | |                            \n");
    print("  |  _| | | | | |  __/ |_| |                            \n");
    print("  |_| |_|_| |_|_||___|___  |                            \n");
    print("                      |___/                             \n");
    print("********************************************************\n");
    print("* E-mail_fnali@gm.ttu.edu.tw                           *\n");
    print("* Website_https://finleyli.medium.com/                 *\n");
    print("********************************************************\n");
'''