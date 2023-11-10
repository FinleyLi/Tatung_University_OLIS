import os
import fitz  # PyMuPDF套件 (請確保已使用 'pip install PyMuPDF' 安裝)

import re

def extract_and_save_pdf_by_number(pdf_folder, output_folder):
    """
    從指定文件夾中的PDF文件中提取連續的9位數字，並另存為新的PDF文件。

    Args:
    pdf_folder (str): 包含PDF文件的文件夾路徑。
    output_folder (str): 保存新PDF文件的目標文件夾路徑。

    Returns:
    None
    """
    # 定義正則表達式模式，以匹配連續的9位數字
    pattern = r'\d{9}'

    # 遍歷文件夾中的PDF文件
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

                        print(f"已從文件 {filename} 的第 {page_num + 1} 頁提取數字 {match}，另存為 {new_filename}")

            # 關閉PDF文件
            pdf_document.close()

if __name__ == "__main__":
    # 設定PDF文件所在的文件夾和另存新檔的文件夾
    pdf_folder = "./PDF"
    output_folder = "./PDF_convert"

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

    # 呼叫函數進行PDF處理
    extract_and_save_pdf_by_number(pdf_folder, output_folder)
