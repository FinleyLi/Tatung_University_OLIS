# import module
from PIL import Image
import pytesseract
import cv2

def i2cv():
    # ==cv2==
    # 讀取圖檔
    img = cv2.imread("page0.jpg")
    # 裁切區域的 x 與 y 座標（左上角）
    x = 1250#1240
    y = 350#350
    # 裁切區域的長度與寬度
    w = 170
    h = 50
    # 裁切圖片
    crop_img = img[y:y+h, x:x+w]
    # 寫入圖檔
    cv2.imwrite('page_out.jpg', crop_img)


def i2t():
    # ==pytesseract OCR==
    image = Image.open('page_out.jpg')
    #code = pytesseract.image_to_string(image, lang='chi_tra')
    code = pytesseract.image_to_string(image, lang='eng')

    return code

