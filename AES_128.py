import sys

# ====================== AES CONSTANTS ======================

# AES S-Box (16x16)
SBOX = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]

# Round Constants for Key Expansion
RCON = [
    0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36
]


# ====================== UTILITY FUNCTIONS ======================

def string_to_bytes(text):
    """Convert string to bytes list (ASCII values)"""
    bytes_list = []
    for char in text:
        bytes_list.append(ord(char))
    # Pad with zeros if needed
    while len(bytes_list) < 16:
        bytes_list.append(0)
    return bytes_list[:16]


def bytes_to_hex(bytes_list):
    """Convert bytes list to hex string"""
    return ''.join(f'{b:02x}' for b in bytes_list)


def hex_to_bytes(hex_string):
    """Convert hex string to bytes list"""
    hex_string = hex_string.replace(' ', '').replace('0x', '')
    bytes_list = []
    for i in range(0, min(len(hex_string), 32), 2):
        if i + 1 < len(hex_string):
            bytes_list.append(int(hex_string[i:i+2], 16))
    while len(bytes_list) < 16:
        bytes_list.append(0)
    return bytes_list[:16]


def create_state(data):
    """Create 4x4 state matrix from 16 bytes (column-major order)"""
    # State Matrix
    state = []
    for col in range(4):
        column = []
        for row in range(4):
            column.append(data[row * 4 + col])
        state.append(column)
    return state


def flatten_state(state):
    """Flatten state matrix to 16 bytes (column-major order)"""
    flat = []
    for col in range(4):
        for row in range(4):
            flat.append(state[col][row])
    return flat


def print_state(state, label="State Matrix"):
    """Print state matrix in hex"""
    print(f"\n{label}:")
    for row in range(4):
        row_values = []
        for col in range(4):
            row_values.append(f"{state[col][row]:02x}")
        print("  " + " ".join(row_values))


def xor_bytes(b1, b2):
    """XOR two byte lists"""
    return [b1[i] ^ b2[i] for i in range(len(b1))]


# ====================== AES CORE FUNCTIONS ======================

def rot_word(word):
    """RotWord: rotate a 4-byte word left by 1 byte"""
    # RotWord
    return word[1:] + word[:1]


def sub_word(word):
    """SubWord: apply S-Box to each byte of a word"""
    # SubWord
    return [SBOX[byte] for byte in word]


def key_expansion(key):
    """Expand 16-byte key to 44 words (176 bytes) for 11 rounds"""
    # Key Expansion
    # Initial key words (4 words of 4 bytes each)
    key_words = []
    for i in range(4):
        word = key[i*4:(i+1)*4]
        key_words.append(word)
    
    # Generate remaining 40 words (10 rounds * 4 words)
    for i in range(4, 44):
        temp = key_words[i-1].copy()
        
        if i % 4 == 0:
            # RotWord + SubWord + XOR with RCON
            temp = rot_word(temp)
            temp = sub_word(temp)
            temp[0] = temp[0] ^ RCON[(i//4) - 1]
        
        # XOR with word 4 positions back
        new_word = [key_words[i-4][j] ^ temp[j] for j in range(4)]
        key_words.append(new_word)
    
    # Convert words to round keys (each round key is 16 bytes)
    round_keys = []
    for round_num in range(11):
        round_key = []
        for word_idx in range(4):
            word = key_words[round_num * 4 + word_idx]
            round_key.extend(word)
        round_keys.append(round_key)
    
    return round_keys


def add_round_key(state, round_key):
    """Add round key to state (XOR each byte)"""
    # AddRoundKey
    new_state = []
    for col in range(4):
        column = []
        for row in range(4):
            column.append(state[col][row] ^ round_key[col * 4 + row])
        new_state.append(column)
    return new_state


def sub_bytes(state):
    """Apply S-Box substitution to each byte of state"""
    # SubBytes
    new_state = []
    for col in range(4):
        column = []
        for row in range(4):
            column.append(SBOX[state[col][row]])
        new_state.append(column)
    return new_state


def shift_rows(state):
    """Shift rows left by row index (0, 1, 2, 3)"""
    # ShiftRows
    new_state = [[], [], [], []]
    for col in range(4):
        for row in range(4):
            new_state[col].append(state[(col + row) % 4][row])
    return new_state


def gmul(a, b):
    """Galois Field multiplication in GF(2^8)"""
    # Galois Field GF(2^8) Multiplication
    result = 0
    for i in range(8):
        if b & 1:
            result = result ^ a
        carry = a & 0x80
        a = (a << 1) & 0xFF
        if carry:
            a = a ^ 0x1B
        b = b >> 1
    return result


def mix_single_column(column):
    """Mix one column of state (4 bytes)"""
    # MixColumns - Single Column
    a0, a1, a2, a3 = column[0], column[1], column[2], column[3]
    
    b0 = gmul(a0, 2) ^ gmul(a1, 3) ^ gmul(a2, 1) ^ gmul(a3, 1)
    b1 = gmul(a0, 1) ^ gmul(a1, 2) ^ gmul(a2, 3) ^ gmul(a3, 1)
    b2 = gmul(a0, 1) ^ gmul(a1, 1) ^ gmul(a2, 2) ^ gmul(a3, 3)
    b3 = gmul(a0, 3) ^ gmul(a1, 1) ^ gmul(a2, 1) ^ gmul(a3, 2)
    
    return [b0, b1, b2, b3]


def mix_columns(state):
    """Apply MixColumns to all columns of state"""
    # MixColumns
    new_state = []
    for col in range(4):
        mixed_column = mix_single_column(state[col])
        new_state.append(mixed_column)
    return new_state


def encrypt_round(state, round_key):
    """Perform one full encryption round: SubBytes, ShiftRows, MixColumns, AddRoundKey"""
    # SubBytes
    state = sub_bytes(state)
    # ShiftRows
    state = shift_rows(state)
    # MixColumns
    state = mix_columns(state)
    # AddRoundKey
    state = add_round_key(state, round_key)
    return state


def final_round(state, round_key):
    """Final round: SubBytes, ShiftRows, AddRoundKey (no MixColumns)"""
    # SubBytes
    state = sub_bytes(state)
    # ShiftRows
    state = shift_rows(state)
    # AddRoundKey
    state = add_round_key(state, round_key)
    return state


def aes_encrypt(plaintext_bytes, key_bytes):
    """Complete AES-128 encryption"""
    # Create state matrix from plaintext
    state = create_state(plaintext_bytes)
    
    print("\n" + "=" * 80)
    print("AES-128 ENCRYPTION PROCESS")
    print("=" * 80)
    print(f"Plaintext (hex): {bytes_to_hex(plaintext_bytes)}")
    print(f"Key (hex):       {bytes_to_hex(key_bytes)}")
    print_state(state, "Original State Matrix")
    
    # Key Expansion
    round_keys = key_expansion(key_bytes)
    
    print("\n" + "-" * 80)
    print("EXPANDED KEYS (Round 0 to Round 10)")
    print("-" * 80)
    for i, key in enumerate(round_keys):
        print(f"Round {i} Key: {bytes_to_hex(key)}")
    
    # Initial AddRoundKey (Round 0)
    print("\n" + "=" * 80)
    print("ROUND 0 - INITIAL ADDROUNDKEY")
    print("=" * 80)
    print_state(state, "State Before Round 0")
    state = add_round_key(state, round_keys[0])
    print_state(state, "After AddRoundKey (Round 0)")
    
    # Rounds 1 to 9 (full rounds with MixColumns)
    for round_num in range(1, 10):
        print("\n" + "=" * 80)
        print(f"ROUND {round_num}")
        print("=" * 80)
        print_state(state, f"State Before Round {round_num}")
        
        # Store state for printing intermediate steps
        state_before = state
        
        # SubBytes
        state = sub_bytes(state)
        print_state(state, "After SubBytes")
        
        # ShiftRows
        state = shift_rows(state)
        print_state(state, "After ShiftRows")
        
        # MixColumns
        state = mix_columns(state)
        print_state(state, "After MixColumns")
        
        # AddRoundKey
        print(f"Round Key {round_num}: {bytes_to_hex(round_keys[round_num])}")
        state = add_round_key(state, round_keys[round_num])
        print_state(state, "After AddRoundKey")
    
    # Final Round (Round 10 - no MixColumns)
    print("\n" + "=" * 80)
    print("FINAL ROUND (ROUND 10)")
    print("=" * 80)
    print_state(state, "State Before Final Round")
    
    # SubBytes
    state = sub_bytes(state)
    print_state(state, "After SubBytes")
    
    # ShiftRows
    state = shift_rows(state)
    print_state(state, "After ShiftRows")
    
    # Final AddRoundKey (no MixColumns)
    print(f"Round Key 10: {bytes_to_hex(round_keys[10])}")
    state = add_round_key(state, round_keys[10])
    print_state(state, "After Final AddRoundKey")
    
    # Flatten state to ciphertext
    ciphertext = flatten_state(state)
    
    print("\n" + "=" * 80)
    print("ENCRYPTION COMPLETE")
    print("=" * 80)
    print(f"Ciphertext (hex): {bytes_to_hex(ciphertext)}")
    print("=" * 80)
    
    return ciphertext


# ====================== MAIN EXECUTION ======================

def main():
    print("=" * 80)
    print("AES-128 (ADVANCED ENCRYPTION STANDARD) - EDUCATIONAL IMPLEMENTATION")
    print("=" * 80)
    
    # Get plaintext input
    print("\nEnter plaintext (16 bytes / 16 characters):")
    plaintext = input("Plaintext: ")
    
    # Handle input
    if len(plaintext) == 32 and all(c in '0123456789abcdefABCDEF' for c in plaintext):
        # Input is hex
        plaintext_bytes = hex_to_bytes(plaintext)
    else:
        # Input is string
        if len(plaintext) > 16:
            plaintext = plaintext[:16]
        plaintext_bytes = string_to_bytes(plaintext)
    
    # Get key input
    print("\nEnter 128-bit key (16 bytes / 16 characters):")
    key = input("Key: ")
    
    if len(key) == 32 and all(c in '0123456789abcdefABCDEF' for c in key):
        # Input is hex
        key_bytes = hex_to_bytes(key)
    else:
        # Input is string
        if len(key) > 16:
            key = key[:16]
        key_bytes = string_to_bytes(key)
    
    # Encrypt
    ciphertext = aes_encrypt(plaintext_bytes, key_bytes)
    
    print("\n" + "=" * 80)
    print("AES-128 ENCRYPTION COMPLETE")
    print("=" * 80)
    print(f"Plaintext:  {bytes_to_hex(plaintext_bytes)}")
    print(f"Key:        {bytes_to_hex(key_bytes)}")
    print(f"Ciphertext: {bytes_to_hex(ciphertext)}")
    print("=" * 80)


if __name__ == "__main__":
    main()