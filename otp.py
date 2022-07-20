from io import TextIOWrapper
import random
import sys
import os

BYTES_PER_SEGMENT = 4

def generate_key(bytes: int, f: TextIOWrapper):
    print("DISCLAIMER: THIS IS NOT A TRUE OTP IF YOU USE THIS")
    print("MAKE YOUR OWN KEY WITH TRUE RANDOM NUMBER GENERATION")
    choices = set()
    key = b""
    for i in range(bytes):
        while True:
            tried = random.randint(0, 2**32-1)
            if tried not in choices:
                choices.add(tried)
                key += int.to_bytes(tried, BYTES_PER_SEGMENT, "big")
                break
    f.write(key)

def encrypt(f: TextIOWrapper, e: TextIOWrapper, d: TextIOWrapper):
    while True:
        e_nib = e.read(BYTES_PER_SEGMENT)
        f_nib = f.read(BYTES_PER_SEGMENT)
        if not e_nib or not f_nib:
            break
        e_nib_int = int.from_bytes(e_nib, "big")
        f_nib_int = int.from_bytes(f_nib, "big")
        enc_nib = e_nib_int ^ f_nib_int
        d.write(int.to_bytes(enc_nib, BYTES_PER_SEGMENT, "big"))
    d.close()
    f.close()
    d.close()

def decrypt(f: TextIOWrapper, d: TextIOWrapper, l: TextIOWrapper):
    d_nib = d.read(1)
    f_nib = f.read(1)
    while True:
        if not d_nib or not f_nib:
            break
        d_nib_int = int.from_bytes(d_nib, "big")
        f_nib_int = int.from_bytes(f_nib, "big")
        denc_nib = d_nib_int ^ f_nib_int
        denc_bytes = int.to_bytes(denc_nib, 1, "big")

        d_nib = d.read(1)
        f_nib = f.read(1)

        if not d_nib:
            denc_bytes = denc_bytes.lstrip(b"\0")
        l.write(denc_bytes)
    f.close()
    d.close()
    l.close()

def main():
    command = sys.argv[1]
    if command == "genkey":
        key = sys.argv[2]
        bytes = int(sys.argv[3])
        generate_key(bytes, open(key, "wb"))
    if command == "encrypt":
        key = sys.argv[2]
        file = sys.argv[3]
        encrypt(open(key, "rb"), open(file, "rb"), open(f"{file}.otp", "wb"))
    if command == "decrypt":
        key = sys.argv[2]
        file = sys.argv[3]
        ext = f".{os.path.basename(file).split('.')[1]}"
        decrypt(open(key, "rb"), open(file, "rb"), open(f"{file}{ext}", "wb") )

if __name__ == "__main__":
    main()