# STEP 0: STANDARD DES TABLES (fixed by the DES specification)

# Initial Permutation table
IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

# Final Permutation (Inverse of IP)
FP = [40, 8, 48, 16, 56, 24, 64, 32,
      39, 7, 47, 15, 55, 23, 63, 31,
      38, 6, 46, 14, 54, 22, 62, 30,
      37, 5, 45, 13, 53, 21, 61, 29,
      36, 4, 44, 12, 52, 20, 60, 28,
      35, 3, 43, 11, 51, 19, 59, 27,
      34, 2, 42, 10, 50, 18, 58, 26,
      33, 1, 41, 9, 49, 17, 57, 25]

# Expansion table: expands 32-bit R to 48 bits
E = [32, 1, 2, 3, 4, 5,
     4, 5, 6, 7, 8, 9,
     8, 9, 10, 11, 12, 13,
     12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21,
     20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29,
     28, 29, 30, 31, 32, 1]

# Permutation applied after S-box substitution
P = [16, 7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9,
     19, 13, 30, 6, 22, 11, 4, 25]

# Permuted Choice 1: reduces 64-bit key to 56 bits (drops parity bits)
PC1 = [57, 49, 41, 33, 25, 17, 9,
       1, 58, 50, 42, 34, 26, 18,
       10, 2, 59, 51, 43, 35, 27,
       19, 11, 3, 60, 52, 44, 36,
       63, 55, 47, 39, 31, 23, 15,
       7, 62, 54, 46, 38, 30, 22,
       14, 6, 61, 53, 45, 37, 29,
       21, 13, 5, 28, 20, 12, 4]

# Permuted Choice 2: selects 48-bit round subkey from 56 bits
PC2 = [14, 17, 11, 24, 1, 5,
       3, 28, 15, 6, 21, 10,
       23, 19, 12, 4, 26, 8,
       16, 7, 27, 20, 13, 2,
       41, 52, 31, 37, 47, 55,
       30, 40, 51, 45, 33, 48,
       44, 49, 39, 56, 34, 53,
       46, 42, 50, 36, 29, 32]

# Left shift schedule per round (16 rounds)
SHIFT_SCHEDULE = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

# The 8 S-boxes (each maps 6 input bits -> 4 output bits)
S_BOXES = [
    # S1
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
    # S2
    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
    # S3
    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
    # S4
    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
    # S5
    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
    # S6
    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
    # S7
    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
    # S8
    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]],
]


# STEP 1: GENERIC BIT-PERMUTATION HELPER

def permute(bits, table):
    """Rearrange/select bits according to `table` (1-indexed positions)."""
    return [bits[i - 1] for i in table]


def left_shift(bits, n):
    """Circular left shift of a bit list by n positions."""
    return bits[n:] + bits[:n]


def xor(bits1, bits2):
    return [b1 ^ b2 for b1, b2 in zip(bits1, bits2)]


# STEP 2: KEY SCHEDULE - generates 16 round subkeys (48 bits each)
def generate_keys(key64_bits):
    """
    key64_bits: list of 64 bits (0/1) - the raw DES key (with parity bits)
    Returns: list of 16 subkeys, each a list of 48 bits
    """
    # PC-1: 64 bits -> 56 bits (drops 8 parity bits)
    key56 = permute(key64_bits, PC1)

    # Split into two 28-bit halves
    C, D = key56[:28], key56[28:]

    round_keys = []
    for round_num in range(16):
        # Left-circular-shift both halves per the schedule
        C = left_shift(C, SHIFT_SCHE
                       |DULE[round_num])
        D = left_shift(D, SHIFT_SCHEDULE[round_num])

        # PC-2: combine and select 48 bits -> this round's subkey
        combined = C + D
        subkey = permute(combined, PC2)
        round_keys.append(subkey)

    return round_keys


# STEP 3: THE ROUND (FEISTEL) FUNCTION f(R, subkey)
def sbox_substitution(expanded_48bit):
    """Splits 48 bits into eight 6-bit chunks, runs each through its
    S-box, and concatenates the eight 4-bit outputs -> 32 bits total."""
    output_bits = []
    for i in range(8):
        chunk = expanded_48bit[i * 6:(i + 1) * 6]

        # Row = outer bits (1st and 6th), Column = middle 4 bits
        row = (chunk[0] << 1) | chunk[5]
        col = (chunk[1] << 3) | (chunk[2] << 2) | (chunk[3] << 1) | chunk[4]

        sbox_value = S_BOXES[i][row][col]          # 0-15
        # Convert the 4-bit result to a list of bits
        bits_4 = [int(b) for b in format(sbox_value, '04b')]
        output_bits.extend(bits_4)

    return output_bits


def feistel_function(R, subkey):
    """f(R, K) = P( S-boxes( E(R) XOR K ) )"""
    expanded = permute(R, E)              # 32 -> 48 bits
    xored = xor(expanded, subkey)         # XOR with round subkey
    substituted = sbox_substitution(xored)  # 48 -> 32 bits via S-boxes
    return permute(substituted, P)        # final permutation


def des_round(L, R, subkey):
    """One Feistel round: L' = R,  R' = L XOR f(R, K)"""
    new_L = R
    new_R = xor(L, feistel_function(R, subkey))
    return new_L, new_R


# STEP 4: FULL 64-BIT BLOCK ENCRYPT / DECRYPT
def process_block(block64_bits, round_keys, mode="encrypt"):
    """
    block64_bits: list of 64 bits (plaintext OR ciphertext block)
    round_keys: list of 16 subkeys from generate_keys()
    mode: "encrypt" uses keys in order 1->16
          "decrypt" uses keys in reverse order 16->1
    """
    keys = round_keys if mode == "encrypt" else round_keys[::-1]

    # Initial Permutation
    block = permute(block64_bits, IP)
    L, R = block[:32], block[32:]

    # 16 Feistel rounds
    for i in range(16):
        L, R = des_round(L, R, keys[i])

    # Swap one final time (R16 || L16), then apply Final Permutation
    pre_output = R + L
    output = permute(pre_output, FP)
    return output


# STEP 5: TEXT <-> BIT CONVERSION + PADDING (so we can handle
#          arbitrary user text, not just exactly 8 bytes)
def text_to_bits(text):
    bits = []
    for byte in text.encode('utf-8'):
        bits.extend([int(b) for b in format(byte, '08b')])
    return bits


def bits_to_text(bits):
    chars = []
    for i in range(0, len(bits), 8):
        byte_bits = bits[i:i + 8]
        byte_val = int(''.join(map(str, byte_bits)), 2)
        chars.append(byte_val)
    return bytes(chars).decode('utf-8', errors='ignore')


def pad(bits):
    """PKCS#7-style padding to a multiple of 64 bits (8 bytes)."""
    total_bytes = len(bits) // 8
    pad_len = 8 - (total_bytes % 8)
    if pad_len == 0:
        pad_len = 8
    pad_bits = []
    for _ in range(pad_len):
        pad_bits.extend([int(b) for b in format(pad_len, '08b')])
    return bits + pad_bits


def unpad(bits):
    """Remove PKCS#7 padding, but raise an error if padding is invalid."""
    if len(bits) < 8:
        raise ValueError("Data too short to contain valid padding.")

    # Read the last byte to get the padding length
    last_byte_bits = bits[-8:]
    pad_len = int(''.join(map(str, last_byte_bits)), 2)

    # Padding length must be between 1 and 8 bytes
    if pad_len < 1 or pad_len > 8:
        raise ValueError(f"Invalid padding length ({pad_len}). Wrong key or corrupted ciphertext.")

    # Verify every padding byte equals pad_len (PKCS#7 rule)
    expected_pad_byte_bits = [int(b) for b in format(pad_len, '08b')]
    for i in range(1, pad_len + 1):
        byte_start = len(bits) - i * 8
        byte_end = len(bits) - (i - 1) * 8
        if bits[byte_start:byte_end] != expected_pad_byte_bits:
            raise ValueError(f"Invalid padding bytes. Wrong key or corrupted ciphertext.")

    # All checks passed — strip the padding
    return bits[:-(pad_len * 8)]


def bits_to_hex(bits):
    val = int(''.join(map(str, bits)), 2)
    return format(val, f'0{len(bits) // 4}x')


# STEP 6: HIGH-LEVEL ENCRYPT / DECRYPT (handles multi-block text)
def des_encrypt(plaintext, key_text):
    key_bits = text_to_bits(key_text)[:64]
    key_bits += [0] * (64 - len(key_bits))          # pad key to 64 bits
    round_keys = generate_keys(key_bits)

    plain_bits = pad(text_to_bits(plaintext))
    cipher_bits = []
    for i in range(0, len(plain_bits), 64):
        block = plain_bits[i:i + 64]
        cipher_bits.extend(process_block(block, round_keys, mode="encrypt"))

    return cipher_bits, bits_to_hex(cipher_bits)


def des_decrypt(cipher_bits, key_text):
    key_bits = text_to_bits(key_text)[:64]
    key_bits += [0] * (64 - len(key_bits))
    round_keys = generate_keys(key_bits)

    plain_bits = []
    for i in range(0, len(cipher_bits), 64):
        block = cipher_bits[i:i + 64]
        plain_bits.extend(process_block(block, round_keys, mode="decrypt"))

    return bits_to_text(unpad(plain_bits))   # Now raises ValueError if padding is invalid


# STEP 7: MAIN — TAKES USER INPUT
def main():
    print("=== DES Encryption/Decryption (from scratch) ===")
    print("\n[1] Encrypt plaintext")
    print("[2] Decrypt existing ciphertext")
    choice = input("\nChoose an option (1 or 2): ").strip()

    key_text = input("Enter an 8-character key (e.g. 'mysecret'): ")
    if len(key_text) == 0:
        print("Key cannot be empty.")
        return

    if choice == "1":
        plaintext = input("Enter plaintext to encrypt: ")
        cipher_bits, cipher_hex = des_encrypt(plaintext, key_text)

        print("\n" + "=" * 40)
        print("Ciphertext (hex):", cipher_hex)

        # Optional verification
        try:
            decrypted_text = des_decrypt(cipher_bits, key_text)
            print("Verification decrypted :", decrypted_text)
            if decrypted_text == plaintext:
                print("[OK] Encryption verified successfully.")
            else:
                print("[FAIL] Mismatch - check implementation.")
        except ValueError as e:
            print(f"[FAIL] Verification error: {e}")
        print("=" * 40)

    elif choice == "2":
        cipher_hex = input("Enter ciphertext (hex) to decrypt: ").replace(" ", "").replace("\n", "")
        try:
            if len(cipher_hex) % 2 != 0:
                cipher_hex = "0" + cipher_hex

            cipher_bits = []
            for i in range(0, len(cipher_hex), 2):
                byte_val = int(cipher_hex[i:i+2], 16)
                cipher_bits.extend([int(b) for b in format(byte_val, '08b')])

            decrypted_text = des_decrypt(cipher_bits, key_text)

            print("\n" + "=" * 40)
            print("Decrypted plaintext:", decrypted_text)
            print("=" * 40)

        except ValueError as e:
            print("\n" + "=" * 40)
            print(f"[ERROR] {e}")
            print("This usually means the key is incorrect or the ciphertext is corrupted.")
            print("=" * 40)
        except Exception as e:
            print("\n" + "=" * 40)
            print(f"[ERROR] Unexpected error: {e}")
            print("=" * 40)

    else:
        print("Invalid choice. Please enter 1 or 2.")


if __name__ == "__main__":
    main()