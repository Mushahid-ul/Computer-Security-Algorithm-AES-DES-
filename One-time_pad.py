def otp_encrypt(plaintext, key):
    ciphertext = ""

    for p, k in zip(plaintext, key):
        if p.isalpha():
            start = ord('A') if p.isupper() else ord('a')
            shift = ord(k.upper()) - 65
            c = (ord(p) - start + shift) % 26
            ciphertext += chr(c + start)
        else:
            ciphertext += p

    return ciphertext


def otp_decrypt(ciphertext, key):
    plaintext = ""

    for c, k in zip(ciphertext, key):
        if c.isalpha():
            start = ord('A') if c.isupper() else ord('a')
            shift = ord(k.upper()) - 65
            p = (ord(c) - start - shift) % 26
            plaintext += chr(p + start)
        else:
            plaintext += c 

    return plaintext


# -------- User Input --------
choice = input("Type E for Encrypt or D for Decrypt: ").upper()
message = input("Enter message: ")
key = input("Enter key (same length): ")

if len(message) != len(key):
    print("❌ Key length must be same as message length")

else:
    if choice == "E":
        encrypted = otp_encrypt(message, key)
        print("\nEncrypted:", encrypted)

    elif choice == "D":
        decrypted = otp_decrypt(message, key)
        print("\nDecrypted:", decrypted)

    else:
        print("❌ Invalid choice! Use E or D.")