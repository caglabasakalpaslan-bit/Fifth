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

## Ters yön: cümle → ayırt edici soru

`cikti/motor.html` bir sıkışma cümlesini alır ve tek bir soru döndürür.

Mantık: cümleye uyum puanı tüm sözlere verilir, sonra **çelişki çiftlerine**
bakılır. İki tarafı da yüksek puan alan çift, sistemin gerçekten bilmediği
yerdir; sorulacak en bilgilendirici soru o çiftin sorusudur. Soru ezberden
gelmez, belirsizliğin ölçülmesinden doğar.

Yerleştirme katmanı şu an sözlük tabanlıdır ve bir vekildir. Türkçe eklemeli
olduğu için kök eşleşmesi yanılır ("geçen sefer" içindeki *geç* kelimesi
zamanlamaya takılır); bu yüzden sözlük öbek bazlıdır ve yine de kırılgandır.
Üretimde yerleştirmeyi `prompt/01-siniflandirici.md` ile aynı şemayı kullanan
bir dil modeli yapmalıdır. Çelişki-belirsizlik mantığı ise modelden bağımsızdır
ve olduğu gibi kalır.

Motor uydurma deyim üretmez. Hangi iskeletin giydirileceğini gösterir;
giydirmeyi dil modeli yapar.

## Ham liste

    python3 arac/cek.py        # → veri/ham_liste.json (3116 kayıt)

İki açık kaynak birleştirilir; 2271 kaydın TDK/Wiktionary anlamı da gelir.
Sınıflandırıcıya sözü *anlamıyla birlikte* vermek doğruluğu belirgin artırır.

## Çıkmaz

Çıkmaz, bir çelişki çiftinin tek kişide aynı anda yaşanmasıdır. "Gitmek mi
kalmak mı", FOMO/FOBO, "ya konuşsam olmuyor sussam gönlüm razı değil" — hepsi
iki yönün de kapalı olduğu durumlar. Atasözü tek yön gösterir; çıkmaz iki yönü
birden tutar.

Bunun sonucu: **çıkmaz, beşinci soruya cevap verilemeyen yerdir.** Cevap
verilebiliyorsa o bir karardır, çıkmaz değil. Ürünün işi çıkmazı karara
çevirmektir.

## Çıkmaz kütüphanesi

`cikmaz/cikmazlar.json` — asıl varlık. Atasözü tek yön gösterir, çıkmaz iki
yönü birden tutar. Her kayıt iki kapalı yönü, her birinin maliyetini, ortak
iskeleti ve aralarında karar verdiren soruyu taşır.

`durum: acik` olanların çıkışı henüz adlandırılmamıştır. Ürünün işi kişiyi
`acik`ten `cozulmus`e taşımaktır.

## Tarama

    export ANTHROPIC_API_KEY=sk-...
    pip install anthropic
    python3 arac/tara.py --adet 200 --iki    # 200 söz, her biri iki kez okunur
    python3 arac/birlestir.py                # taranan.jsonl → atasozleri.json
    python3 arac/dogrula.py veri/atasozleri.json

`--iki` her sözü iki ayrı çağrıda okur ve p/z farkı 0.2'yi geçenleri
`veri/celiskili.jsonl` dosyasına ayırır. Güvenilirlik ölçüsü budur: modele
değil, iki bağımsız okumanın uyuşmasına güvenilir.

Tarama kesilirse kaldığı yerden devam eder. Küçük partilerle başla (`--adet 50`),
çıktıyı gözle, sonra büyüt.

## Akış: kapıdan çıkışa

1. **Giriş** — adlandırılmış çıkmaz kapısı ya da serbest anlatı
2. **Onay** — "şuna benziyor mu?" Kişi hayır diyebilmeli.
3. **Ayrım** — beşinci soru, hangi tarafta olduğunu belirler
4. **Yollar** — 3-4 bilinen çıkış; her biri *ne zaman yetmediğini* de söyler
5. **Beşinci seçenek** — "benimki bunların hiçbiri değil", kişi kendi yolunu yazar
6. **Dönüş** — sonra: "ne yaptın, ne oldu?"

Adım 6 ürünün kendisidir. Dönüş olmadan `yollar` hiç dolmaz.

`kaynak: kutuphane` olan yollar derlenmiştir; arayüzde "bilinen yollar" diye
gösterilir. `kaynak: donus` olanlar gerçek kullanıcı dönüşünden gelir ve
"3 kişi bunu denedi" diye gösterilebilir. Uydurma yüzde kullanılmaz.
