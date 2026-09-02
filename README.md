# Atasözü atlası

Atasözlerini kelime yüzeyinden çözüp alan-bağımsız iskeletlerine indiren ve
üç koordinata oturtan çalışma seti.

## Koordinatlar

- **Kutup** — imgenin geldiği alan. 8 tane, birbirinin zıddı değil; bir söz
  en fazla ikisine dokunur.
- **p** — polarite, −1 (kıs/çekil) ile +1 (aç/başla) arası.
- **z** — deneyim gerekliliği, 0 (söylenince anlaşılır) ile 1 (ancak yaşayan
  bilir) arası.
- **m** — mekanizma, 17'lik kapalı liste.
- **i** — iskelet: sözün somut isim içermeyen hali. Asıl ürün budur.

## Akış

    python3 arac/dogrula.py veri/atasozleri.json   # denetle + kapsama raporu
    python3 arac/olustur.py                        # cikti/harita.html üret

## Taramayı büyütmek

1. `prompt/01-siniflandirici.md` promptuyla yeni atasözlerini sınıflandır.
2. Çıkan JSON satırlarını `veri/atasozleri.json` içindeki `kayitlar`a ekle.
3. `dogrula.py` çalıştır. Somut isim uyarısı gelen iskeletleri elle düzelt;
   bu uyarı bir kural değil, dikkat çağrısıdır.
4. Kapsama raporundaki boş hücrelere denk gelen atasözlerini kasten ara.
   Set büyürken temsil dengesini korumak, sayıyı büyütmekten önemlidir.

## Kalite kapısı

İskeletin bilgi kaybedip kaybetmediğini ölçmek için: iskeleti tek başına temiz
bir modele ver, "bundan bir atasözü üret" de. Üçüncü bir model üretileni
orijinaliyle eşleştirebiliyorsa iskelet sağlamdır. Eşleştiremiyorsa iskelet
fazla soyutlanmış ya da yanlış çıkarılmıştır; yeniden yaz.

## Çelişki çiftleri

`c` alanı, birbirini yalanlayan sözleri bağlar. "Acele işe şeytan karışır"
ile "Sona kalan dona kalır" ikisi de doğrudur — farklı koşullarda. İkisi
arasında karar veren soru, tanımı gereği ayırt edici bir sorudur. Bu alan
soru üretiminin kaynağıdır.
