# import module
from pdf2image import convert_from_path
from PIL import Image

def p2i(name):
    # pdf2image
    # 註冊組提供原始畢業證書掃描檔
    image = convert_from_path(name)
    print(f'convert from path, {name}')

    # PDF儲存為JPEG
    for i in range(len(image)):
        image[i].save('page'+ str(i) + '.jpg', 'JPEG')
