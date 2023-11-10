import os
import fitz  # PyMuPDF套件 (請確保已使用 'pip install PyMuPDF' 安裝)
import re
import PySimpleGUI as sg  # PySimpleGUI套件 (請確保已使用 'pip install PySimpleGUI' 安裝)

def extract_and_save_pdf_by_number(pdf_folder, output_folder):
    # 定義正則表達式模式，以匹配連續的9位數字
    pattern = r'\d{9}'

    # 遍歷文件夾中的PDF文件
    success_count = 0  # 用於跟蹤成功轉換的PDF數量

    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)

            # 打開PDF文件
            pdf_document = fitz.open(pdf_path)

            # 遍歷每一頁並提取文字內容
            for page_num in range(len(pdf_document)):
                page = pdf_document[page_num]
                text = page.get_text("text")

                # 使用正則表達式查找連續的9位數字
                matches = re.findall(pattern, text)

                # 如果找到符合條件的數字
                if matches:
                    for match in matches:
                        # 確定要建立的新檔案名稱
                        new_filename = f"{match}_ch.pdf"
                        output_path = os.path.join(output_folder, new_filename)

                        # 複製指定頁面到新的PDF檔案
                        new_pdf = fitz.open()
                        new_pdf.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)
                        new_pdf.save(output_path)
                        new_pdf.close()

                        # 增加成功計數器
                        success_count += 1

                        print(f"已從文件 {filename} 的第 {page_num + 1} 頁提取數字 {match}，另存為 {new_filename}")

            # 關閉PDF文件
            pdf_document.close()

    return success_count  # 返回成功轉換的數量

if __name__ == "__main__":
    # 文字圖
    text_art = (
        "    __ _       _                                        \n"
        "   / _(_)_ __ | | ___ _   _                             \n"
        "  | |_| |  _  | |/ _   | | |                            \n"
        "  |  _| | | | | |  __/ |_| |                            \n"
        "  |_| |_|_| |_|_||___|___  |                            \n"
        "                      |___/                             \n"
    )

    # 創建PySimpleGUI窗口，用戶可以選擇輸入和輸出資料夾
    layout = [
        [sg.Text("選擇PDF文件夾：")],
        [sg.InputText(key="pdf_folder", enable_events=True), sg.FolderBrowse()],
        [sg.Text("選擇另存新檔的文件夾：")],
        [sg.InputText(key="output_folder"), sg.FolderBrowse()],
        [sg.Button("執行")],
        [sg.Output(size=(80, 20))],  # 創建一個類似終端的區域
        [sg.Text("", size=(80, 1), key="success_count")],  # 用於顯示成功轉換的數量
        [sg.Text(f"© 2023.10.28 by Finley", size=(80, 1), justification="right", font=("Helvetica", 8))]  # 版權說明
    ]

    window = sg.Window("PDF處理工具", layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break
        elif event == "執行":
            pdf_folder = values["pdf_folder"]
            output_folder = values["output_folder"]

            # 執行PDF處理
            success_count = extract_and_save_pdf_by_number(pdf_folder, output_folder)

            # 更新顯示成功轉換的數量
            window["success_count"].update(f"成功轉換了 {success_count} 個PDF文件")

    window.close()
