'''
 * Program Name: Dcert PDF 2 OCR
 * Subject: "PDF to Image, Image convert to text, Save as PDF".
 * Input: ./PDF/"Scanner PDF files".
 * Output: ./PDF_convert/"StudentID_ch.pdf".
 * Since 2022/11/06
 * 2022/11/08, add subprocess py & PDFs convert. 
 * ____/__/__, auto search student ID location, now => (img[y:y+h, x:x+w])
 * ToolKit: VS Code 1.73.0, Python 3.11.0
 * Author: Finley
 *         Computer Center, Tatung University
'''

# import module
import os, sys
import sub_p2i, sub_t2p
from sub_i2t import i2cv, i2t

def proc():
    # ==batch process==
    path = ( ".\PDF")
    for fname in os.listdir(path):
        path = path.replace('.\PDF',"")

        pdfFactor(os.path.join(path, fname))

def pdfFactor(name):
    # ==PDF 2 Image==
    fileName = f'.\PDF\{name}' 
    try:
        sub_p2i.p2i(fileName)
    except:
        sys.exit(f'{fileName} p2i error')

    # ==cv2==
    try:
        i2cv()
        code = i2t()
    except:
        sys.exit(f'{fileName} cv2 or i2t error')

    # ==PyPDF2-2.11.1==
    try:
        sub_t2p.t2p(code, fileName)
    except:
        sys.exit(f'{fileName} t2p error')

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
    proc()