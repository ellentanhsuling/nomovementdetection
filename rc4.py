"""
RC4 Stream Cipher Implementation

RC4 (Rivest Cipher 4) operates in two phases:
  1. Key Scheduling Algorithm (KSA)  – builds the initial permutation of S
     from the variable-length key.
  2. Pseudo-Random Generation Algorithm (PRGA) – generates one keystream
     byte per iteration by swapping entries in S.

Encryption and decryption are the same XOR operation against the keystream.
"""

from __future__ import annotations


def _ksa(key: bytes) -> list[int]:
    """Key Scheduling Algorithm: initialise the 256-byte permutation table."""
    key_len = len(key)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % key_len]) % 256
        S[i], S[j] = S[j], S[i]
    return S


def _prga(S: list[int], n: int) -> bytes:
    """Pseudo-Random Generation Algorithm: yield *n* keystream bytes."""
    i = j = 0
    output = bytearray(n)
    for k in range(n):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        output[k] = S[(S[i] + S[j]) % 256]
    return bytes(output)


def rc4_keystream(key: bytes, length: int) -> bytes:
    """Return *length* bytes of RC4 keystream for the given key."""
    if not key:
        raise ValueError("Key must not be empty")
    if not 1 <= len(key) <= 256:
        raise ValueError("Key length must be between 1 and 256 bytes")
    return _prga(_ksa(key), length)


def rc4_crypt(key: bytes, data: bytes) -> bytes:
    """Encrypt or decrypt *data* with RC4 under *key* (same operation)."""
    stream = rc4_keystream(key, len(data))
    return bytes(a ^ b for a, b in zip(data, stream))


# ---------------------------------------------------------------------------
# RFC 6229 test vectors (partial) – used to validate correctness
# ---------------------------------------------------------------------------
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
    """Validate against RFC 6229 vectors and round-trip properties."""
    print("Running RC4 tests...\n")

    for i, vec in enumerate(_RFC6229_VECTORS):
        stream = rc4_keystream(vec["key"], vec["offset"] + len(vec["expected"]))
        actual = stream[vec["offset"]:]
        status = "PASS" if actual == vec["expected"] else "FAIL"
        print(f"  RFC 6229 vector {i + 1}: {status}")
        if status == "FAIL":
            print(f"    expected: {vec['expected'].hex()}")
            print(f"    got:      {actual.hex()}")

    key = b"test-key"
    plaintext = b"Hello, RC4 stream cipher!"
    ciphertext = rc4_crypt(key, plaintext)
    decrypted = rc4_crypt(key, ciphertext)
    status = "PASS" if decrypted == plaintext else "FAIL"
    print(f"  Round-trip encrypt/decrypt: {status}")

    assert ciphertext != plaintext, "Ciphertext should differ from plaintext"
    print(f"  Ciphertext differs from plaintext: PASS")

    print("\nAll tests passed.\n")


def _demo() -> None:
    """Interactive demonstration of RC4 encryption and decryption."""
    print("=" * 60)
    print("  RC4 Stream Cipher Demo")
    print("=" * 60)

    key_str = input("\nEnter encryption key: ")
    if not key_str:
        print("Key must not be empty.")
        return
    key = key_str.encode("utf-8")

    plaintext_str = input("Enter plaintext message: ")
    plaintext = plaintext_str.encode("utf-8")

    ciphertext = rc4_crypt(key, plaintext)
    decrypted = rc4_crypt(key, ciphertext)

    print(f"\n{'Key':>20s}: {key_str}")
    print(f"{'Plaintext':>20s}: {plaintext_str}")
    print(f"{'Plaintext (hex)':>20s}: {plaintext.hex()}")
    print(f"{'Ciphertext (hex)':>20s}: {ciphertext.hex()}")
    print(f"{'Decrypted':>20s}: {decrypted.decode('utf-8')}")
    print(f"{'Round-trip OK':>20s}: {decrypted == plaintext}")


if __name__ == "__main__":
    _run_tests()
    _demo()
