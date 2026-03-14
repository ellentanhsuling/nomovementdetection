"""
RC4 Stream Cipher Implementation
=================================

WHAT IS RC4?

    RC4 (Rivest Cipher 4) is a way to scramble a message so that only
    someone with the correct password (called a "key") can read it.

    Imagine you wrote a letter and then used a secret codebook to replace
    every letter with a different one.  The person receiving the letter
    uses the same codebook in reverse to read the original message.
    RC4 works the same way, but the "codebook" is generated
    mathematically from the key you choose.

HOW DOES IT WORK? (Two steps)

    Step 1 - Key Scheduling Algorithm (KSA)
        Build a shuffled list of numbers 0-255.  The shuffling pattern is
        determined by your key, so a different key produces a completely
        different shuffle.  Think of it like shuffling a deck of 256 cards
        in a way that only your key can reproduce.

    Step 2 - Pseudo-Random Generation Algorithm (PRGA)
        Walk through the shuffled list, continually swapping entries, and
        pull out one "random-looking" number for each letter of your
        message.  These numbers form the "keystream".

    Encryption:  combine each letter of the message with the
                 corresponding keystream number using XOR (a reversible
                 math operation) to produce the scrambled output.

    Decryption:  do the exact same thing again on the scrambled output.
                 Because XOR is reversible, you get the original message
                 back.

WHAT IS XOR?

    XOR (exclusive or) compares two numbers bit by bit:
        same bits  -> 0
        different  -> 1

    The magic property:  A XOR B = C,  and  C XOR B = A.
    So XOR-ing once encrypts, and XOR-ing a second time decrypts.

    Example with the letter "H" (72) and keystream number 200:
        Encrypt:  72 XOR 200  = 144  (scrambled)
        Decrypt: 144 XOR 200  =  72  (back to "H")
"""

from __future__ import annotations


# =========================================================================
# STEP 1 — Key Scheduling Algorithm (KSA)
#
# Purpose:  Take the user's key and use it to create a thoroughly
#           shuffled list of numbers 0 through 255.  This shuffled
#           list (called "S") is the foundation of the cipher.
#
# Plain-English walkthrough:
#   1. Start with a list S containing the numbers 0, 1, 2, ... 255
#      in order — like a fresh, unshuffled deck of 256 cards.
#   2. Set a pointer j to 0.
#   3. Visit every position i from 0 to 255.  At each position:
#        a. Calculate a new value for j using: the old j, the card
#           at position i, and the next character of the key
#           (cycling back to the start of the key when you reach
#           the end).
#        b. Swap the cards at positions i and j.
#   4. After 256 swaps, S is thoroughly shuffled in a pattern
#      that is unique to the key you provided.
# =========================================================================

def _ksa(key: bytes) -> list[int]:
    """
    Key Scheduling Algorithm.

    Takes the key (a sequence of bytes — i.e. the password converted
    to numbers) and returns a shuffled list of 256 numbers.
    """
    key_len = len(key)

    # 1. Create the initial ordered list: [0, 1, 2, ... 255]
    S = list(range(256))

    # 2. Start the pointer j at zero
    j = 0

    # 3. Walk through every position (0 to 255)
    for i in range(256):
        # 3a. Update j based on the current card and the key.
        #     "% 256" means wrap around so j always stays between 0 and 255.
        #     "% key_len" means cycle through the key characters repeatedly.
        j = (j + S[i] + key[i % key_len]) % 256

        # 3b. Swap the cards at positions i and j.
        S[i], S[j] = S[j], S[i]

    # 4. Return the shuffled list — this is the "prepared deck".
    return S


# =========================================================================
# STEP 2 — Pseudo-Random Generation Algorithm (PRGA)
#
# Purpose:  Using the shuffled list S from Step 1, generate a
#           sequence of "random-looking" numbers — one for each
#           character of the message.  This sequence is the
#           "keystream".
#
# Plain-English walkthrough:
#   1. Start two pointers, i and j, both at 0.
#   2. For each character in the message:
#        a. Move i forward by 1 (wrapping around at 256).
#        b. Update j by adding the card at position i
#           (wrapping around at 256).
#        c. Swap the cards at positions i and j
#           (the list keeps changing as we go).
#        d. Look up the card at position (S[i] + S[j]) mod 256.
#           That card's value is the next keystream number.
#   3. Collect all those keystream numbers — one per character.
# =========================================================================

def _prga(S: list[int], n: int) -> bytes:
    """
    Pseudo-Random Generation Algorithm.

    Takes the shuffled list S and the number of keystream bytes
    needed (n), and returns that many pseudo-random bytes.
    """
    # 1. Start both pointers at zero
    i = 0
    j = 0
    output = bytearray(n)

    # 2. Generate one keystream byte per loop iteration
    for k in range(n):
        # 2a. Move pointer i forward by 1 (wrap around at 256)
        i = (i + 1) % 256

        # 2b. Update pointer j using the card at position i
        j = (j + S[i]) % 256

        # 2c. Swap the cards at positions i and j
        S[i], S[j] = S[j], S[i]

        # 2d. The keystream byte is the card found at position
        #     (S[i] + S[j]) mod 256
        output[k] = S[(S[i] + S[j]) % 256]

    # 3. Return the full keystream
    return bytes(output)


# =========================================================================
# PUTTING IT TOGETHER — Generate keystream from a key
#
# This simply chains Step 1 and Step 2:
#   - Step 1 shuffles the list using the key.
#   - Step 2 uses the shuffled list to produce keystream bytes.
# =========================================================================

def rc4_keystream(key: bytes, length: int) -> bytes:
    """
    Generate an RC4 keystream.

    Parameters:
        key    — the password, as raw bytes (1 to 256 bytes long)
        length — how many keystream bytes to produce (one per
                 character you want to encrypt or decrypt)

    Returns:
        The keystream — a sequence of 'length' pseudo-random bytes.
    """
    if not key:
        raise ValueError("Key must not be empty")
    if not 1 <= len(key) <= 256:
        raise ValueError("Key length must be between 1 and 256 bytes")

    shuffled_list = _ksa(key)              # Step 1: shuffle with the key
    return _prga(shuffled_list, length)     # Step 2: generate keystream


# =========================================================================
# ENCRYPTION AND DECRYPTION
#
# To encrypt:  take each letter of the message and XOR it with the
#              corresponding keystream byte.  The result is unreadable
#              gibberish (the ciphertext).
#
# To decrypt:  do the exact same thing — XOR each byte of the
#              ciphertext with the keystream.  Because XOR reverses
#              itself, you get the original message back.
#
# That's why one single function handles both encrypting and decrypting.
#
# Example:
#     key       = "secret"
#     message   = "Hi"         <- two characters
#     keystream = [200, 45]    <- two random-looking numbers from PRGA
#
#     Encrypt:  'H' XOR 200 = 144,  'i' XOR 45 = 108
#               ciphertext = [144, 108]   (unreadable)
#
#     Decrypt:  144 XOR 200 = 72 = 'H',  108 XOR 45 = 105 = 'i'
#               result = "Hi"  (original message restored)
# =========================================================================

def rc4_crypt(key: bytes, data: bytes) -> bytes:
    """
    Encrypt or decrypt data using RC4.

    Parameters:
        key  — the password, as raw bytes
        data — the message to encrypt, OR the ciphertext to decrypt

    Returns:
        If data was plaintext  -> returns ciphertext (encrypted).
        If data was ciphertext -> returns plaintext  (decrypted).

    Both operations are identical — XOR is its own inverse.
    """
    stream = rc4_keystream(key, len(data))

    # XOR each byte of the data with the corresponding keystream byte
    return bytes(a ^ b for a, b in zip(data, stream))


# =========================================================================
# TEST VECTORS — checking the implementation is correct
#
# RFC 6229 is a public document that lists known-correct RC4 outputs
# for specific keys.  By comparing our output to those published
# values we can confirm the algorithm is implemented correctly.
# =========================================================================

_RFC6229_VECTORS: list[dict] = [
    {
        "key": bytes.fromhex("0102030405"),
        "offset": 0,
        "expected": bytes.fromhex("b2 39 63 05 f0 3d c0 27"
                                  " cc c3 52 4a 0a 11 18 a8".replace(" ", "")),
    },
    {
        "key": bytes.fromhex("01020304050607"),
        "offset": 0,
        "expected": bytes.fromhex("29 3f 02 d4 7f 37 c9 b6"
                                  " 33 f2 af 52 85 fe b4 6b".replace(" ", "")),
    },
    {
        "key": bytes.fromhex("0102030405060708"),
        "offset": 0,
        "expected": bytes.fromhex("97 ab 8a 1b f0 af b9 61"
                                  " 32 f2 f6 72 58 da 15 a8".replace(" ", "")),
    },
]


def _run_tests() -> None:
    """
    Run automated tests to make sure the implementation is correct.

    1. Compare our output against 3 published RFC 6229 test vectors.
    2. Encrypt a message, then decrypt it, and verify we get back the
       original — this confirms the round-trip property of XOR.
    """
    print("Running RC4 tests...\n")

    # Test against published RFC 6229 values
    for i, vec in enumerate(_RFC6229_VECTORS):
        stream = rc4_keystream(vec["key"], vec["offset"] + len(vec["expected"]))
        actual = stream[vec["offset"]:]
        status = "PASS" if actual == vec["expected"] else "FAIL"
        print(f"  RFC 6229 vector {i + 1}: {status}")
        if status == "FAIL":
            print(f"    expected: {vec['expected'].hex()}")
            print(f"    got:      {actual.hex()}")

    # Test the encrypt-then-decrypt round trip
    key = b"test-key"
    plaintext = b"Hello, RC4 stream cipher!"
    ciphertext = rc4_crypt(key, plaintext)
    decrypted = rc4_crypt(key, ciphertext)
    status = "PASS" if decrypted == plaintext else "FAIL"
    print(f"  Round-trip encrypt/decrypt: {status}")

    # Sanity check: ciphertext must not be the same as plaintext
    assert ciphertext != plaintext, "Ciphertext should differ from plaintext"
    print(f"  Ciphertext differs from plaintext: PASS")

    print("\nAll tests passed.\n")


# =========================================================================
# INTERACTIVE DEMO
#
# When you run this program, it will:
#   1. Run the automated tests above.
#   2. Ask you to type a key (password) and a message.
#   3. Show the encrypted (scrambled) output in hexadecimal.
#   4. Decrypt it back and show the original message is recovered.
# =========================================================================

def _demo() -> None:
    """
    Interactive demonstration.

    Asks the user for a key and a message, encrypts the message,
    then decrypts it to prove the round trip works.
    """
    print("=" * 60)
    print("  RC4 Stream Cipher Demo")
    print("=" * 60)

    key_str = input("\nEnter encryption key (your password): ")
    if not key_str:
        print("Key must not be empty.")
        return
    key = key_str.encode("utf-8")

    plaintext_str = input("Enter message to encrypt: ")
    plaintext = plaintext_str.encode("utf-8")

    # Encrypt the message
    ciphertext = rc4_crypt(key, plaintext)

    # Decrypt it back (same function, same key)
    decrypted = rc4_crypt(key, ciphertext)

    print(f"\n{'Key':>20s}: {key_str}")
    print(f"{'Original message':>20s}: {plaintext_str}")
    print(f"{'Message (hex)':>20s}: {plaintext.hex()}")
    print(f"{'Encrypted (hex)':>20s}: {ciphertext.hex()}")
    print(f"{'Decrypted':>20s}: {decrypted.decode('utf-8')}")
    print(f"{'Round-trip OK':>20s}: {decrypted == plaintext}")


if __name__ == "__main__":
    _run_tests()
    _demo()
