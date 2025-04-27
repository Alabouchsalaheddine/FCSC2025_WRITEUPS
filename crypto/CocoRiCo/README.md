# CocoRiCo


## Solution


Ce challenge est un CTF de type **crypto AEAD mal utilisé**. Voici les points clés et comment l'exploiter pour générer un **token admin "toto" valide** :

---

## 🔍 Analyse de la vulnérabilité

1. **Chiffrement utilisé : AES en mode OFB (stream cipher)** :
   - Le mode OFB est un **mode de chiffrement par flot**, donc **symétrique** : même entrée + même IV + même clé = même flux chiffrant.
   - Il **ne fournit pas d'authenticité** à lui seul. C'est pourquoi le challenge ajoute un **tag CRC32** comme "authentification".

2. **"Authentification" maison avec `crc32`** :
   - Le message est **concaténé avec son `crc32`** (4 octets), puis chiffré.
   - À la déchiffre, le système **vérifie uniquement le CRC32 du message déchiffré**.

3. **La faiblesse** :
   - Le chiffrement est **réversible** si on a un **message chiffré valide** : on peut extraire le keystream.
   - Il n’y a **aucune vérification sérieuse d’intégrité**, le CRC32 est trop faible et pas secret.

---

## 🧨 Objectif de l’attaque

Tu veux générer un **token chiffré valide** pour ce JSON :

```json
{
  "name": "toto",
  "admin": true
}
```

Mais comme le code interdit de créer un tel token via la commande `new`, il faut :
- Créer un **token légitime** avec un nom et `admin: false`
- **Modifier le contenu déchiffré**
- **Recoder le tag CRC32**
- **Rechiffrer avec le même keystream**

---

## 💥 Étapes de l’attaque

### 1. Obtiens un token valide

Lance le programme et choisis :
```
1. Login
Are you new ? y
Name: alice
```

Tu obtiens un token comme :
```
4ed8f4d1a3... (en hex)
```

Convertis-le en bytes : `bytes.fromhex(...)`

### 2. Déchiffre ce token

Puisque tu as le token chiffré et tu connais le message original (`{"name": "alice", "admin": false}`), tu peux :
- En déduire le **keystream** : `keystream = ciphertext XOR plaintext`
- Puis **chiffrer ton message modifié avec ce même keystream**.

### 3. Forge ton token admin

#### a. Crée le JSON malicieux :
```python
d = json.dumps({"name": "toto", "admin": True}).encode()
```

#### b. Calcule son CRC32 :
```python
tag = int.to_bytes(zlib.crc32(d), 4, 'big')
payload = d + tag
```

#### c. Applique le keystream :
```python
new_ciphertext = bytes([a ^ b for a, b in zip(payload, keystream)])
```

Puis convertis en hex et colle-le comme token pour login.

---

## 🧪 Code d’exploitation complet

Voici un script d'exploitation :

```python
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
```



Interaction avec le serveur :

```
(my_env) salaheddinealabouch@Salah-Eddines-MacBook-Pro fcsc_2025 % nc chall.fcsc.fr 2150
0. Quit
1. Login
2. Logout
3. TODO
>>> 1
Are you new ? (y/n) y
Name: alice
Welcome alice. Here is your token:
c368d3700f19c47e1d2a282b3823a7641117c1a7f317fe61ba4385518625fe32bf6e4bf52e
This challenge is still under active developement, please come back in a few weeks to try it out!
0. Quit
1. Login
2. Logout
3. TODO
>>> 1
Are you new ? (y/n) n
Token: c368d3700f19c47e1d2a3d28252fe06a1d1582a2fa13f92da259d145922cf07f8282d2
Congrats! Here is your flag:
FCSC{56e8ee27c9039b13a2b896da9a95a266cadd9a6e06e6d1f140f3df6cbed6332c}
0. Quit
1. Login
2. Logout
3. TODO
>>> 
```

---

## ✅ Conclusion

Ce challenge illustre une **mauvaise implémentation de l'authentification** : utiliser `crc32` pour vérifier l'intégrité n'est **pas sécurisé**, surtout combiné à un **chiffrement par flot** réversible. Tu peux donc forger n’importe quel message, y compris un token `admin`.


---

## Flag

FCSC{56e8ee27c9039b13a2b896da9a95a266cadd9a6e06e6d1f140f3df6cbed6332c}

---
```