import base64

def encrypt_text(input_text):
    text_bytes = input_text.encode('utf-8')
    encoded_bytes = base64.b64encode(text_bytes)
    return encoded_bytes.decode('utf-8')

def decrypt_text(input_text):
    text_bytes = input_text.encode('utf-8')
    decoded_bytes = base64.b64decode(text_bytes)
    return decoded_bytes.decode('utf-8')

mode = "encrypt"
while True:
    # 提示目前模式
    if mode == "encrypt":
        text = input("當前模式：加密\n請輸入一段文字：")
    else:
        text = input("當前模式：解密\n請輸入Base64加密過的文字：")
    
    if text == ":q!":
        break
    elif text == ":converter":
        mode = "decrypt" if mode == "encrypt" else "encrypt"
        continue
    
    if mode == "encrypt":
        print("Base64加密的結果：", encrypt_text(text))
    else:
        try:
            print("Base64解密的結果：", decrypt_text(text))
        except:
            print("解密失敗，請確保輸入的是有效的Base64加密過的文字。")

print("程式已結束。")
