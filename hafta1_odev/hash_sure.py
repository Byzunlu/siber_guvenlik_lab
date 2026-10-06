# Kurulum: pip install argon2-cffi
import hashlib
import time
from argon2 import PasswordHasher

parola = b"benim-parolam-123"

# ---------- SHA-256 ----------
# Çok hızlı olduğu için tek ölçüm yetmez, 100.000 kez çalıştırıp ortalama alıyoruz
tekrar_sha = 100_000
baslangic = time.perf_counter()
for _ in range(tekrar_sha):
    hashlib.sha256(parola).digest()
toplam = time.perf_counter() - baslangic
sha_ort = toplam / tekrar_sha

# ---------- Argon2id ----------
# PasswordHasher varsayılan olarak Argon2id kullanır
ph = PasswordHasher()
tekrar_argon = 10
baslangic = time.perf_counter()
for _ in range(tekrar_argon):
    ph.hash(parola.decode())
toplam = time.perf_counter() - baslangic
argon_ort = toplam / tekrar_argon

# ---------- Sonuçlar ----------
print("=== Süre ölçümü (kendi bilgisayarınızda) ===")
print(f"SHA-256  : {sha_ort * 1e6:.3f} mikrosaniye / hash")
print(f"Argon2id : {argon_ort * 1000:.1f} milisaniye / hash")
print()
print(f"Argon2id, SHA-256'dan yaklaşık {argon_ort / sha_ort:,.0f} kat daha yavaş.")
print()
print("=== Saldırgan saniyede kaç parola deneyebilir? (tek çekirdek) ===")
print(f"SHA-256  : yaklaşık {1 / sha_ort:,.0f} deneme/saniye")
print(f"Argon2id : yaklaşık {1 / argon_ort:,.1f} deneme/saniye")
print()
print("Argon2id ayarları:")
print(f"  time_cost={ph.time_cost}, memory_cost={ph.memory_cost} KiB "
      f"({ph.memory_cost // 1024} MB), parallelism={ph.parallelism}")
