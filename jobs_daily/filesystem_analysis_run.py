# run_filesystem_analysis.py
import filesystem_analysis, os

def main():
    # 切換工作目錄到相對路徑 ".\env311"
    os.chdir(".\Env3116")
    path = ".\\DF-Hcsv\\"
    filesystem_analysis.dev_main(path)

if __name__ == "__main__":
    main()
