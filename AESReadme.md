# AES-128 Encryption from Scratch

This project is a simple educational implementation of **AES-128 (Advanced Encryption Standard)** in Python.

The main purpose of this project is to understand how AES encryption works internally instead of using a ready-made cryptography library. The implementation includes the AES S-Box, key expansion, state matrix operations, SubBytes, ShiftRows, MixColumns, AddRoundKey, and the complete AES-128 encryption process.

## What is AES?

AES (Advanced Encryption Standard) is a symmetric block cipher used to encrypt data.

AES-128 works with:

* 128-bit plaintext blocks
* 128-bit keys
* 10 encryption rounds
* 16-byte state matrix

In this implementation, both the plaintext and key are handled as 16 bytes.

The encryption process can be summarized as:

```text
Plaintext
   ↓
Create State Matrix
   ↓
Key Expansion
   ↓
Initial AddRoundKey
   ↓
Rounds 1–9
   ├── SubBytes
   ├── ShiftRows
   ├── MixColumns
   └── AddRoundKey
   ↓
Final Round
   ├── SubBytes
   ├── ShiftRows
   └── AddRoundKey
   ↓
Ciphertext
```

## Features

* AES-128 encryption implemented from scratch
* Standard AES S-Box
* AES RCON values
* 128-bit key expansion
* 11 round keys
* State matrix representation
* SubBytes transformation
* ShiftRows transformation
* MixColumns transformation
* AddRoundKey transformation
* Galois Field multiplication
* Plaintext and key input as normal text or hexadecimal
* Detailed output of intermediate encryption steps
* Final ciphertext displayed in hexadecimal

## How the Code Works

### 1. AES Constants

The program starts with the standard AES S-Box and round constants.

The S-Box is used during the SubBytes transformation and also during key expansion. The RCON values are used when generating new words during the key expansion process.

```python
SBOX = [...]
RCON = [...]
```

### 2. Converting Text to Bytes

The `string_to_bytes()` function converts each character into its corresponding byte value.

Since AES-128 works with exactly 16 bytes, shorter input is filled with `0` values and input longer than 16 bytes is truncated.

```python
def string_to_bytes(text):
    bytes_list = []

    for char in text:
        bytes_list.append(ord(char))

    while len(bytes_list) < 16:
        bytes_list.append(0)

    return bytes_list[:16]
```

The program also contains functions for converting between byte lists and hexadecimal strings.

```python
bytes_to_hex()
hex_to_bytes()
```

### 3. State Matrix

AES internally works with a 4×4 byte matrix called the **State**.

The program converts the 16-byte input into this state using `create_state()`.

The implementation follows the AES column-major representation.

```text
16 bytes

a0 a1 a2 a3
a4 a5 a6 a7
a8 a9 aa ab
ac ad ae af
```

The state is stored internally as four columns, each containing four bytes.

The `flatten_state()` function converts the state back into a 16-byte list after encryption.

### 4. Key Expansion

AES-128 does not use the original key directly in every round.

Instead, the 16-byte key is expanded into **44 words**, which are then grouped into **11 round keys**.

The key expansion uses three main operations:

* RotWord
* SubWord
* RCON

The implementation is handled by:

```python
def key_expansion(key):
```

The first four words come directly from the original 16-byte key. The remaining words are generated using XOR operations and the AES key schedule.

The result is:

```text
Original Key
     ↓
44 Words
     ↓
11 Round Keys
```

Each round key contains 16 bytes.

### 5. AddRoundKey

AddRoundKey performs a byte-by-byte XOR between the current state and the round key.

```python
state[col][row] ^ round_key[col * 4 + row]
```

This operation is performed before the first round and again at the end of every encryption round.

### 6. SubBytes

SubBytes replaces every byte in the state with another byte using the AES S-Box.

For example, if a byte has a value of:

```text
0x53
```

the corresponding value is looked up in the AES S-Box.

The implementation is:

```python
def sub_bytes(state):
```

It applies the S-Box to all 16 bytes in the state.

### 7. ShiftRows

ShiftRows rearranges the bytes in the state matrix.

The first row is not shifted.

The second row is shifted by one position.

The third row is shifted by two positions.

The fourth row is shifted by three positions.

This creates diffusion between the columns of the state.

The implementation is:

```python
def shift_rows(state):
```

and uses the row index to determine how far each row is shifted.

### 8. MixColumns

MixColumns operates on each column of the state.

Each column contains four bytes, and those bytes are mathematically combined using multiplication in the finite field:

```text
GF(2^8)
```

The program implements the required finite-field multiplication through:

```python
def gmul(a, b):
```

Then `mix_single_column()` applies the AES MixColumns transformation to one column, while `mix_columns()` applies it to all four columns.

The transformation can be represented as:

```text
[b0]   [02 03 01 01]   [a0]
[b1] = [01 02 03 01] × [a1]
[b2]   [01 01 02 03]   [a2]
[b3]   [03 01 01 02]   [a3]
```

### 9. AES Encryption Round

Rounds 1 through 9 contain four operations:

```text
SubBytes
ShiftRows
MixColumns
AddRoundKey
```

The program has an `encrypt_round()` function that performs these operations in order.

### 10. Final Round

The tenth and final AES round is slightly different.

It performs:

```text
SubBytes
ShiftRows
AddRoundKey
```

**MixColumns is not performed in the final round.**

This is implemented in:

```python
def final_round(state, round_key):
```

## Main Encryption Process

The complete AES-128 encryption is handled by:

```python
def aes_encrypt(plaintext_bytes, key_bytes):
```

The function:

1. Creates the initial state matrix
2. Expands the key
3. Performs the initial AddRoundKey
4. Runs rounds 1–9
5. Runs the final round
6. Converts the final state into ciphertext
7. Displays the ciphertext in hexadecimal

The program also prints the state after each major transformation, making it easier to follow the AES algorithm step by step.

## Input

The program accepts both normal text and hexadecimal input.

For plaintext, you can enter:

```text
Hello AES World!
```

or a 32-character hexadecimal value such as:

```text
00112233445566778899aabbccddeeff
```

The same approach is used for the 128-bit key.

If normal text is entered, the program converts it into bytes.

If a 32-character hexadecimal string is entered, it is converted directly into bytes.

## Running the Program

Make sure Python 3 is installed.

Then run:

```bash
python aes.py
```

The program will ask for the plaintext:

```text
Enter plaintext (16 bytes / 16 characters):
Plaintext:
```

Then enter the 128-bit key:

```text
Enter 128-bit key (16 bytes / 16 characters):
Key:
```

After that, the program performs AES-128 encryption and displays the intermediate steps and final ciphertext.

## Example

A simple example could be:

```text
Plaintext:  Hello AES World!
Key:        ThisIsMyAESKey12
```

The program converts both values into hexadecimal and processes them through the AES encryption steps.

The final output contains:

```text
Plaintext:  ...
Key:        ...
Ciphertext: ...
```

The exact ciphertext depends on the exact 16-byte plaintext and key provided.

## Functions Used

| Function              | Purpose                                  |
| --------------------- | ---------------------------------------- |
| `string_to_bytes()`   | Converts text into a 16-byte list        |
| `bytes_to_hex()`      | Converts bytes into hexadecimal          |
| `hex_to_bytes()`      | Converts hexadecimal into bytes          |
| `create_state()`      | Creates the AES state matrix             |
| `flatten_state()`     | Converts the state back into bytes       |
| `print_state()`       | Displays the state matrix                |
| `xor_bytes()`         | Performs XOR between byte lists          |
| `rot_word()`          | Rotates a 4-byte word                    |
| `sub_word()`          | Applies the AES S-Box to a word          |
| `key_expansion()`     | Generates the AES round keys             |
| `add_round_key()`     | Performs the AddRoundKey operation       |
| `sub_bytes()`         | Performs the SubBytes transformation     |
| `shift_rows()`        | Performs the ShiftRows transformation    |
| `gmul()`              | Performs GF(2^8) multiplication          |
| `mix_single_column()` | Mixes one state column                   |
| `mix_columns()`       | Performs MixColumns                      |
| `encrypt_round()`     | Performs a normal AES round              |
| `final_round()`       | Performs the final AES round             |
| `aes_encrypt()`       | Performs complete AES-128 encryption     |
| `main()`              | Handles user input and program execution |

## Project Structure

```text
AES-128/
│
├── aes.py
└── README.md
```

## Important Note

This is an **educational implementation** of AES-128. The purpose is to understand the internal steps of AES and how the different transformations work.

For real applications, it is better to use a well-tested cryptographic library instead of implementing encryption manually.

## What I Learned From This Project

This project helps demonstrate several important concepts in cryptography and programming:

* How AES-128 encryption works
* How a state matrix is used
* How AES keys are expanded
* How S-Boxes provide substitution
* How ShiftRows provides diffusion
* How MixColumns works in GF(2^8)
* How XOR is used in cryptographic algorithms
* How multiple encryption rounds work together
* How hexadecimal and byte representations are handled in Python

## Author

**Mushahidul Islam**

Computer Science & Engineering Student
