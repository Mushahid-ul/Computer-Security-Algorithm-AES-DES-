# Get inputs
key = input("Enter_key: ")
msg = input("Enter message: ")
mode = input("Encrypt (E) or Decrypt (D)? ").upper()

# Keep original case of message
original_case = [char.isupper() for char in msg]

# Convert to uppercase for matrix processing
key_proc = key.upper().replace("J", "I")
msg_proc = msg.upper().replace("J", "I")

# Create matrix
alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
matrix_chars = []

# Add key chars
for char in key_proc:
    if char not in matrix_chars and char in alphabet:
        matrix_chars.append(char)

# Add remaining alphabet
for char in alphabet:
    if char not in matrix_chars:
        matrix_chars.append(char)

# Make 5x5 matrix
matrix = []
for i in range(0, 25, 5):
    matrix.append(matrix_chars[i:i+5])

print("\nPlayfair Matrix:")
for row in matrix:
    print(' '.join(row))

# Clean message
clean_msg = ""
for char in msg_proc:
    if char.isalpha():
        clean_msg += char

# Make pairs
pairs = []
i = 0
while i < len(clean_msg):
    if i == len(clean_msg) - 1:
        pairs.append(clean_msg[i] + "X")
        break
    if mode == 'E' and clean_msg[i] == clean_msg[i+1]:
        pairs.append(clean_msg[i] + "X")
        i += 1
    else:
        pairs.append(clean_msg[i] + clean_msg[i+1])
        i += 2

print(f"\nPairs: {pairs}")

# Process pairs
result = ""
shift = 1 if mode == 'E' else -1

for pair in pairs:
    r1 = c1 = r2 = c2 = -1
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == pair[0]:
                r1, c1 = row, col
            if matrix[row][col] == pair[1]:
                r2, c2 = row, col
    
    if r1 == r2:
        first = matrix[r1][(c1 + shift) % 5]
        second = matrix[r2][(c2 + shift) % 5]
    elif c1 == c2:
        first = matrix[(r1 + shift) % 5][c1]
        second = matrix[(r2 + shift) % 5][c2]
    else:
        first = matrix[r1][c2]
        second = matrix[r2][c1]

    result += first + second

# Restore original case
final_result = ""
letter_index = 0
for char in msg:
    if char.isalpha():
        if char.isupper():
            final_result += result[letter_index].upper()
        else:
            final_result += result[letter_index].lower()
        letter_index += 1
    else:
        final_result += char

print(f"\nResult: {final_result}")