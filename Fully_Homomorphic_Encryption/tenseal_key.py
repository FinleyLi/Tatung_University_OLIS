# 文件名: generate_context.py

import tenseal as ts

def generate_context():
    # Creating a context for CKKS scheme
    context = ts.context(
        ts.SCHEME_TYPE.CKKS,
        poly_modulus_degree=8192,
        coeff_mod_bit_sizes=[60, 40, 40, 60]
    )
    context.global_scale = 2**40
    context.generate_galois_keys()

    # Saving context with the secret key
    with open("context_with_secret_key.seal", "wb") as f:
        f.write(context.serialize(save_secret_key=True))

    print("Context with secret key has been generated and saved.")

if __name__ == "__main__":
    generate_context()
