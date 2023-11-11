# 文件名: encrypt_data.py

import tenseal as ts
import numpy as np

def encrypt_data():
    with open("context_with_secret_key.seal", "rb") as f:
        context = ts.context_from(f.read())

    data = np.array([3, 22, 6, 20])
    encrypted = ts.ckks_vector(context, data) * 2

    with open("encrypted_data.seal", "wb") as f:
        f.write(encrypted.serialize())

    print("Data has been encrypted and saved.")

if __name__ == "__main__":
    encrypt_data()
