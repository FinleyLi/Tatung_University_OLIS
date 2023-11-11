# 文件名: decrypt_data.py

import tenseal as ts

def decrypt_data():
    with open("context_with_secret_key.seal", "rb") as f:
        context = ts.context_from(f.read())

    with open("encrypted_data.seal", "rb") as f:
        encrypted_data = ts.ckks_vector_from(context, f.read())

    decrypted_data = encrypted_data.decrypt()

    print("Decrypted data:", decrypted_data)

if __name__ == "__main__":
    decrypt_data()
