import json
import zlib

def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

# Message original (par exemple, celui qu'on a créé avec "alice")
original_json = json.dumps({"name": "alice", "admin": False}).encode()
original_tag = int.to_bytes(zlib.crc32(original_json), 4, 'big')
original_plaintext = original_json + original_tag

# Ton token chiffré copié depuis le challenge (en hex)
original_ciphertext = bytes.fromhex("...")  # <--- Mets ton token ici

# On récupère le keystream
keystream = xor(original_plaintext, original_ciphertext)

# Message malicieux
malicious_json = json.dumps({"name": "toto", "admin": True}).encode()
malicious_tag = int.to_bytes(zlib.crc32(malicious_json), 4, 'big')
malicious_plaintext = malicious_json + malicious_tag

# Rechiffrement avec le même keystream
malicious_ciphertext = xor(malicious_plaintext, keystream)
print("Use this token:")
print(malicious_ciphertext.hex())
