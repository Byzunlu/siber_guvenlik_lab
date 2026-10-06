# Hafta 2 · Ek Görev (Kali): Parola Kırma

## Sonuçlar

| Özet | Kırma süresi | Benchmark hızı |
|---|---|---|
| MD5 | ~6 sn (8/8) | 175,1 MH/s |
| SHA-256 | ~6 sn (8/8) | 45.631,4 kH/s (~45,6 MH/s) |
| bcrypt | ~4-25 sn (8/8) | 1.583 H/s |

**Kırılan parolalar:** `123456`, `passw0rd`, `monkey`, `trustno1`, `welcome`, `ankara06`, `istanbul34`, `besiktas`

## Sorular ve cevaplar

**1) Hangi özet anında kırıldı, hangisi yavaştı, neden?**
MD5 ve SHA-256 saniyeler içinde (8/8) kırıldı; bcrypt aynı sözlükte belirgin şekilde daha yavaştı. Benchmark'a göre MD5 saniyede ~175 milyon, SHA-256 ~45,6 milyon deneme yapabiliyor; bcrypt ise sadece ~1.583. Bu, MD5'in bcrypt'ten ~110.000 kat, SHA-256'nın ~28.800 kat daha hızlı denenebildiğini gösteriyor — bcrypt kasıtlı olarak yavaş tasarlandığı için fark bu kadar büyük.

**2) MD5 ile SHA-256 arasında kırma kolaylığı açısından fark var mıydı? SHA-256 neden yetersiz?**
Pratikte fark yok — ikisi de aynı 8 parolayı anında kırdı (benchmark'taki 3,8x hız farkı saldırgan için önemsiz). SHA-256'nın gücü çarpışma direnci gibi kriptografik özelliklerden gelir, veri bütünlüğü için tasarlanmıştır ve kasıtlı olarak hızlıdır. Parola saklamada istenen ise yavaşlık; SHA-256 tuzsuz ve tek adımda hesaplandığından MD5 kadar hızlı denenebiliyor, bu yüzden parola saklama için yetersiz.

**3) bcrypt'in yavaşlığı kullanıcıya ve saldırgana ne kadar zaman kaybettirir? Bu neden iyi bir denge?**
Kullanıcı girişte sadece 1 hash hesaplatır — 1.583 H/s hızında bu milisaniyeler sürer, fark edilmez. Saldırgan ise milyonlarca deneme yapmak zorunda; bizim testimizde 28 kelimelik mini sözlük bile MD5'te anında biterken bcrypt'te saniyelerce sürdü. Büyük gerçek sözlüklerde (rockyou.txt gibi) bu fark saatlere/günlere çıkar. Maliyet tek seferlik kullanıcıya göre ihmal edilebilir, milyonlarca tekrar yapan saldırgana göre ise katlanarak büyür — bu yüzden iyi bir denge sağlar.

**4) İki kullanıcının MD5 özeti aynı çıkarsa bu ne anlama gelir? Tuz bunu nasıl önler?**
MD5 tuzsuz ve deterministiktir, aynı parola her zaman aynı hash'i üretir. İki kullanıcının hash'i aynıysa, aynı parolayı kullandıkları anlamına gelir — biri kırılınca diğeri de otomatik olarak açığa çıkar. Tuz, her kullanıcı için rastgele ve benzersiz bir değer ekleyerek aynı parolaların da farklı hash'ler üretmesini sağlar; böylece saldırgan ortak parolaları tespit edemez ve toplu/rainbow-table saldırıları işe yaramaz.

## Ekran görüntüleri

- `1.jpeg` — MD5 kırma sonucu (Adım 1)
- `2.jpeg` — SHA-256 kırma sonucu (Adım 2)
- `3.jpeg` — bcrypt kırma sonucu (Adım 3)
