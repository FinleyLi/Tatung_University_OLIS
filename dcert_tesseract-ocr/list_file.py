# -*- coding: utf-8 -*-
# dir > output.txt

# 讀取資料夾內所有檔案名稱放進list裡
'''
import os
#↑載入OS模組
dir_path = ( ".\PDF")
#dir_path = os.path.dirname(os.path.realpath(__file__))
#↑獲取當前資料夾名稱然後存成dir_path變數

all_file_name = os.listdir(dir_path)
#↑讀取資料夾內所有檔案名稱然後放進all_file_name這個list裡

print(all_file_name)
'''

# 列出目錄中所有檔案：os.listdir

from os import listdir
from os.path import isfile, isdir, join

# 指定要列出所有檔案的目錄
mypath = ( ".\PDF")#"/var/log"

# 取得所有檔案與子目錄名稱
files = listdir(mypath)

# 以迴圈處理
with open('output.txt', 'w') as file:
  for f in files:
    # 產生檔案的絕對路徑
    fullpath = join(mypath, f)
    # 判斷 fullpath 是檔案還是目錄
    if isfile(fullpath):
      print(f)
      file.write(f + '\n')
    elif isdir(fullpath):
      print("目錄：", f)
'''
#!/usr/bin/python
# -*- coding: utf-8 -*-
from os import listdir
from os.path import isfile, isdir, join

# 指定要列出所有檔案的目錄
mypath = "/var/log"

# 取得所有檔案與子目錄名稱
files = listdir(mypath)

# 以迴圈處理
for f in files:
  # 產生檔案的絕對路徑
  fullpath = join(mypath, f)
  # 判斷 fullpath 是檔案還是目錄
  if isfile(fullpath):
    print("檔案：", f)
  elif isdir(fullpath):
    print("目錄：", f)
'''

# 列出目錄中所有檔案：os.walk
'''
from os import walk

# 指定要列出所有檔案的目錄
mypath = "/var/log"

# 遞迴列出所有子目錄與檔案
for root, dirs, files in walk(mypath):
  print("路徑：", root)
  print("  目錄：", dirs)
  print("  檔案：", files)
'''
'''
from os import walk
from os.path import join

# 指定要列出所有檔案的目錄
mypath = ( ".\PDF")#"/var/log"

# 遞迴列出所有檔案的絕對路徑
for root, dirs, files in walk(mypath):
  for f in files:
    fullpath = join(root, f)
    print(fullpath)
'''

# pandas比對兩個csv檔案，並將不同的資料寫入新的csv檔案
'''
import pandas as pd
 
 
df1 = pd.read_csv('coursea_data.csv').rename(columns={'course_title':'name'})
 
df2 = pd.read_csv('Coursera_courses.csv')
 
result = df1.merge(df2, how='outer', indicator=True).loc[lambda x : x['_merge'] == 'left_only']
 
print(result)

'''