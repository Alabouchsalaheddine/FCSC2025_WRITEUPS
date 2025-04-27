# Analyse mémoire - Pour commencer (1/2)


## Challenge Statement

You are preparing to analyze a memory dump and you are noting some information about the machine before diving into the analysis:

- **username**
- **machine name**
- **non-local IPv4 address of the machine**

The flag is in the format:  
`FCSC{<username>:<machine name>:<IPv4 address>}`

Where:
- `<username>` is the name of the user using the machine,
- `<machine name>` is the name of the analyzed machine,
- `<IPv4 address>` is the non-local IPv4 address of the machine.

For example:  
`FCSC{Arthur:Computer-of-rct:192.168.1.150}`

Warning: For this challenge, you only have 10 submission attempts.

---

## Solution



### ✅ **Étape 1 : Installer Volatility**
Le plus simple est de l’installer via `pip` (Volatility 3 recommandé) :

```bash
pip install volatility3
```

---

### ✅ **Étape 2 : Identifier le profil**
Tu dois identifier l’OS et le type de dump. Par exemple, si c’est un dump Windows, il faut détecter la version (Windows 10, 11, etc.) :

```bash
vol -f chemin/vers/fichier.dmp windows.info
```

Cela te donnera des infos utiles comme le nom de l'utilisateur, l'OS, la version, etc.

---

### ✅ **Étape 3 : Récupérer le nom de l'utilisateur**

Utilise ce plugin :

```bash
vol -f chemin/vers/fichier.dmp windows.sessions
```

Ou :

```bash
vol -f chemin/vers/fichier.dmp windows.getusersids
```

Tu verras des chemins comme `C:\Users\<nom_utilisateur>`.

---

### ✅ **Étape 4 : Récupérer le nom de la machine**

Tu peux essayer :

```bash
vol -f chemin/vers/fichier.dmp windows.registry.printkey --key "HKLM\SYSTEM\CurrentControlSet\Control\ComputerName\ComputerName"
```

Cela te donnera le `ComputerName`.

---

### ✅ **Étape 5 : Trouver l’adresse IPv4**

Ce plugin donne les connexions réseau :

```bash
vol -f chemin/vers/fichier.dmp windows.netscan
```

Ou :

```bash
vol -f chemin/vers/fichier.dmp windows.netstat
```

Cherche une adresse **non locale** (différente de 127.0.0.1 ou 169.254.x.x).

---

### 🏁 **Format final du flag**

Une fois que tu as :

- `NomUtilisateur`
- `NomMachine`
- `AdresseIPv4`

Tu les mets dans le format :

```
FCSC{NomUtilisateur:NomMachine:AdresseIPv4}
```


---

## Flag

```
FCSC{userfcsc-10:DESKTOP-JV996VQ:10.0.2.15}
```
