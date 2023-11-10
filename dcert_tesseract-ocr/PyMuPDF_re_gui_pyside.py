import sys
import os
import fitz
import re
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QTextEdit

class PDFExtractorApp(QWidget):
    def __init__(self):
        super().__init__()

        # 設置窗口標題和大小
        self.setWindowTitle("PDF處理工具")
        self.resize(600, 400)

        # 布局設置
        layout = QVBoxLayout(self)

        # 創建文件夾選擇區域
        self.pdf_folder_edit = QLineEdit(self)
        self.output_folder_edit = QLineEdit(self)
        pdf_folder_button = QPushButton("瀏覽", self)
        output_folder_button = QPushButton("瀏覽", self)
        pdf_folder_button.clicked.connect(lambda: self.choose_folder(self.pdf_folder_edit))
        output_folder_button.clicked.connect(lambda: self.choose_folder(self.output_folder_edit))

        pdf_folder_layout = QHBoxLayout()
        pdf_folder_layout.addWidget(QLabel("選擇PDF文件夾："))
        pdf_folder_layout.addWidget(self.pdf_folder_edit)
        pdf_folder_layout.addWidget(pdf_folder_button)

        output_folder_layout = QHBoxLayout()
        output_folder_layout.addWidget(QLabel("選擇另存新文件的文件夾："))
        output_folder_layout.addWidget(self.output_folder_edit)
        output_folder_layout.addWidget(output_folder_button)

        layout.addLayout(pdf_folder_layout)
        layout.addLayout(output_folder_layout)

        # 創建按鈕和文本輸出區
        run_button = QPushButton("執行", self)
        run_button.clicked.connect(self.run_extraction)
        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)

        layout.addWidget(run_button)
        layout.addWidget(self.output_text)

    def choose_folder(self, line_edit):
        folder = QFileDialog.getExistingDirectory(self, "選擇文件夾")
        if folder:
            line_edit.setText(folder)

    def run_extraction(self):
        pdf_folder = self.pdf_folder_edit.text()
        output_folder = self.output_folder_edit.text()

        if pdf_folder and output_folder:
            success_count = extract_and_save_pdf_by_number(pdf_folder, output_folder)
            self.output_text.append(f"成功轉換了 {success_count} 個PDF文件")

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
    app = QApplication([])
    window = PDFExtractorApp()
    window.show()
    sys.exit(app.exec())
