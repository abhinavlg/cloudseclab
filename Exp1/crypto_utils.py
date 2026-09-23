from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def encrypt_file(input_file, output_file, key):
    cipher = AES.new(key, AES.MODE_EAX)
    with open(input_file, 'rb') as f:
        data = f.read()
    ciphertext, tag = cipher.encrypt_and_digest(data)
    with open(output_file, 'wb') as f:
        for x in (cipher.nonce, tag, ciphertext):
            f.write(x)

def decrypt_file(input_file, output_file, key):
    with open(input_file, 'rb') as f:
        nonce, tag, ciphertext = [f.read(x) for x in (16, 16, -1)]
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)
    with open(output_file, 'wb') as f:
        f.write(data)

def generate_key():
    return get_random_bytes(16)  # 128-bit AES key; store securely!
