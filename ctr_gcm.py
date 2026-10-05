import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag

mesaj = b"Tutar: 100 TL"
anahtar = os.urandom(16)

# ---------- BÖLÜM 1: CTR (doğrulama yok) ----------
print("=== CTR ===")
nonce = os.urandom(16)
sifreleyici = Cipher(algorithms.AES(anahtar), modes.CTR(nonce)).encryptor()
sifreli = sifreleyici.update(mesaj) + sifreleyici.finalize()
print("Orijinal mesaj :", mesaj.decode())
print("Şifreli (hex)  :", sifreli.hex())

# Saldırgan anahtarı bilmiyor. Sadece '1' harfinin 7. konumda olduğunu tahmin ediyor.
# Şifreli verinin o baytını (eski ^ yeni) ile XOR'layarak '1' -> '9' yapıyor.
konum = 7
degistirilmis = bytearray(sifreli)
degistirilmis[konum] ^= ord("1") ^ ord("9")
print("Değişmiş şifreli:", bytes(degistirilmis).hex())

# Alıcı normal şekilde çözüyor
cozucu = Cipher(algorithms.AES(anahtar), modes.CTR(nonce)).decryptor()
cozulen = cozucu.update(bytes(degistirilmis)) + cozucu.finalize()
print("Alıcının gördüğü:", cozulen.decode(), " <-- değişiklik fark edilmedi!")

# ---------- BÖLÜM 2: AES-GCM (doğrulama var) ----------
print("\n=== AES-GCM ===")
aes = AESGCM(AESGCM.generate_key(bit_length=128))
nonce = os.urandom(12)
sifreli = aes.encrypt(nonce, mesaj, None)  # sonunda 16 baytlık etiket (tag) var
print("Şifreli (hex)  :", sifreli.hex())

# Aynı saldırı: aynı konumdaki baytı değiştir
degistirilmis = bytearray(sifreli)
degistirilmis[konum] ^= ord("1") ^ ord("9")

try:
    aes.decrypt(nonce, bytes(degistirilmis), None)
    print("Çözüldü (olmaması gerekirdi)")
except InvalidTag:
    print("HATA: InvalidTag -> mesajın değiştirildiği tespit edildi!")

# Değişmemiş mesaj sorunsuz çözülüyor
print("Değişmemiş mesaj:", aes.decrypt(nonce, sifreli, None).decode())
