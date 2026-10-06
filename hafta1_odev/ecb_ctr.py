# Kurulum: pip install cryptography pillow
# Kullanım: python ecb_ctr.py resim.png
import os
import sys
from PIL import Image
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes



# 1) Görüntüyü aç, RGB'ye çevir, ham piksel baytlarını al
img = Image.open("resim.jpg").convert("RGB")
boyut = img.size
ham = img.tobytes()

anahtar = os.urandom(16)  # AES-128


def baytlardan_resim(veri):
    # Şifreli baytları (orijinal uzunluğa kırparak) tekrar görüntü yap
    return Image.frombytes("RGB", boyut, veri[: len(ham)])


# 2) ECB: blok boyutu 16 bayt olmalı, bu yüzden sıfırlarla tamamla
dolgu = (-len(ham)) % 16
ecb = Cipher(algorithms.AES(anahtar), modes.ECB()).encryptor()
ecb_sifreli = ecb.update(ham + b"\x00" * dolgu) + ecb.finalize()

# 3) CTR: dolgu gerekmez, nonce 16 bayt
nonce = os.urandom(16)
ctr = Cipher(algorithms.AES(anahtar), modes.CTR(nonce)).encryptor()
ctr_sifreli = ctr.update(ham) + ctr.finalize()

# 4) Üç görüntüyü yan yana yapıştır: orijinal | ECB | CTR
w, h = boyut
sonuc = Image.new("RGB", (w * 3, h), "white")
sonuc.paste(img, (0, 0))
sonuc.paste(baytlardan_resim(ecb_sifreli), (w, 0))
sonuc.paste(baytlardan_resim(ctr_sifreli), (w * 2, 0))
sonuc.save("karsilastirma.png")
print("Kaydedildi: karsilastirma.png (orijinal | ECB | CTR)")
