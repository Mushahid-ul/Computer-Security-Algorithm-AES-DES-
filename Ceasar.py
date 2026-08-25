def caesar(text, shift):
    result = ""
    shift = shift % 26

    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - start + shift) % 26 + start)
        else:
            result += char

    return result


# ---- User Input ----
choice = input("Type E for Encrypt or D for Decrypt: ").upper()
text = input("Enter text: ")
shift = int(input("Enter shift value: "))

if choice == "E":
    output = caesar(text, shift)
    print("Cipher Text:", output)

elif choice == "D":
    output = caesar(text, -shift)
    print("Plain Text:", output)

else:
    print("Invalid choice! Use E or D.")