# import module
from PyPDF2 import PdfFileReader, PdfFileWriter

def t2p(code, fileName):
    # ==PyPDF2-2.11.1==
    #實例化一個writer
    pdf_writer = PdfFileWriter()

    #開啟已有的PDF檔，並實例化一個reader
    file_to_get = open(fileName, 'rb')
    pdf_reader = PdfFileReader(file_to_get)
    code = code.replace('\n',"")

    #開啟要存的新檔
    newPDF = open(f'.\PDF_convert\{code}_ch.pdf', 'wb')
    newpage = pdf_reader.getPage(0)
    pdf_writer.addPage(newpage)
    pdf_writer.write(newPDF)

    #記得關閉檔案！若沒有關閉檔案會出現錯誤，少一頁    
    newPDF.close()

    print(f'to .\PDF_convert\{code}_ch.pdf OK')
