# Lovable promptu

Aşağıdakini olduğu gibi yapıştır. Önce iki CSV'yi yükle: `veri.csv` ve `yollar.csv`.

---

Sana iki CSV yükledim. Bunlar tek doğruluk kaynağıdır; içerik uydurma, yalnızca
bu tablolardan seç ve birleştir.

**veri.csv** — 239 satır. `tur` sütunu sekiz değer alır: atasözü, deyim,
çıkmaz, trend kelime, yunan mitosu, yunan tanrısı, başka mitoloji, dünya atasözü. Sütunlar: id, tur, metin, anlam_ekseni, iskelet,
mekanizma, kutup, yon, yasanmislik, celisen, ayirt_edici_soru.

**yollar.csv** — 152 satır. Her çıkmazın dört çıkış yolu.
Sütunlar: cikmaz_id, cikmaz, yol, ne, ise_yarar, yetmez.

**vakalar.csv** — 36 satır, 27'si iş hayatından. Başkasının çıkmazı havuzu.
Sütunlar: id, alan, durum, yon_A, A_bedel, yon_B, B_bedel, ayirt_edici_soru, cikmaz_id.
Bu tablo ikinci giriş kapısıdır: "Şu an bir derdim yok, başkasınınkine bakayım"
diyen kullanıcı buradan girer. Vakayı okur, A veya B seçer, sonra o vakanın
`ayirt_edici_soru`sunu görür. Seçimi `cikmaz_id` üzerinden kendi kaydına bağlanır —
aynı çıkmaza kendi hikâyesiyle girdiğinde ona daha önce ne seçtiğini hatırlat.

Next.js + Tailwind, koyu değil **sıcak açık** tema (kağıt beyazı zemin,
koyu mürekkep metin, tek vurgu rengi kiremit). Tek sütun, telefon genişliği,
büyük tipografi, az eleman.

## Akış — dört kademe

**10 · Kişinin getirdiği**
Boş bir ekran. Tek başlık: "Ne oluyor?" Altında yazma alanı.
Altında küçük gri yazıyla üç gerçek cümle örnek olarak — tıklayınca kutuya düşer.
Menü, kategori listesi, kapı ızgarası **yok**. Ekranda bundan başka bir şey olmayacak.

**20 · Bağlamsal soru**

Kullanıcı hiçbir zaman tablodaki kelimeleri kullanmayacak. "Toplantılardan
vakit kalmıyor" cümlesi hiçbir atasözüne kelime olarak benzemez. Bu yüzden
**kelime eşleştirmesi yapma.** Anlam eşleştirmesi yap ve şu sırayı izle:

1. Kullanıcının cümlesini oku ve içindeki durumu tek bir soyut cümleye indir:
   kim, neye karşı, hangi iki şey arasında sıkışmış. Bu senin çalışma
   iskeletin — kullanıcıya gösterme.
2. Bu iskeleti `veri.csv`'nin **`iskelet`** ve **`anlam_ekseni`** sütunlarıyla
   anlamsal yakınlığa göre karşılaştır. `metin` sütununa bakma; orada
   somut imgeler var ve kullanıcının cümlesiyle benzeşmezler.
3. Çıkan en yakın satırların `mekanizma` değerini al. Bu alan 17 değerlik
   **kapalı bir listedir**; yeni değer uydurma, mutlaka listedekilerden birine
   düşür. Serbest yorum girişte, disiplin burada.
4. O mekanizmaya sahip `tur = çıkmaz` satırlarından en yakın üçünü seç.

Kullanıcıya sor: "Şunlardan hangisine daha yakın?"
Üç seçenek + "Hiçbiri, kendim yazayım".
Seçenek metinleri `anlam_ekseni` sütunundan gelsin — çıkmazın `metin`
sütunundaki iç etiketini **asla gösterme**.

Hiçbir satır yeterince yakın değilse bunu gizleme. "Bunu haritamda bir yere
koyamadım, kendi cümlenle devam edelim" de ve kullanıcının kendi yazdığıyla
ilerle. Zorla eşleştirme yapma.

**30 · Fifth Eye — ayırt edici soru**
Seçilen çıkmazın `ayirt_edici_soru` sütunundaki soruyu tam olarak göster.
Tek soru. Değiştirme, yeniden yazma, ekleme yapma.
İki ya da üç cevap seçeneği sun.

Ardından `yollar.csv`'den o çıkmazın dört yolunu göster. Her yolda üç satır:
ne yapılır · işe yarar · **yetmez**.
`yetmez` satırını atlamak yasak; o satır ürünün karakteri.
Beşinci seçenek her zaman: "Bunların hiçbiri değil — kendi yolumu yazacağım".

**40 · Yaşanmış deneyim — dilini kullanıcı seçer**
Yol seçildikten sonra sor: "Bunu hangi dilden okumak istersin?"
Yedi düğme, ikişerli ızgara: Atasözü · Deyim · Trend kelime · Yunan mitosu ·
Yunan tanrısı · Başka mitoloji · Dünya atasözü. Altında ayrıca: Kendi cümlem.

Basılan düğmeye göre `veri.csv`'den **aynı `mekanizma` değerine sahip** ve o
`tur`daki en yakın satırı getir. Bağlantı buradan kurulur: kişinin cümlesi →
iskelet → mekanizma → bütün diller. Aynı mekanizmada o türde satır yoksa,
en yakın mekanizmadan getir ve "tam karşılığı yok, buna yakın olan şu" de. Ekrana `metin` ve `iskelet` sütunlarını bas.
Atasözü seçilirse, varsa `celisen` sütunundaki zıt sözü de göster ve altına
yaz: "Bu ikisi çelişmiyor, farklı koşullarda doğru."

## Kesin kurallar

- Yüzde, skor, sıralama, rozet, seviye, günlük seri **yok**.
  "3 kişiden 2'si" denebilir, "%67" denemez.
- İç etiketler kullanıcıya gösterilmez: çıkmaz adı, mekanizma, kutup, katman.
  Kullanıcı yalnızca kendi cümlesini ve tablodan gelen metni görür.
- Teşhis dili yok. "Sen şusun", "şu tipsin", "hapsolmuşsun" gibi cümleler kurma.
- Tabloda olmayan atasözü, mitos ya da trend kelime **uydurma**. Kullanıcının
  cümlesini serbestçe yorumla, ama gösterdiğin her metin tablodan gelsin.
- `mekanizma` alanına listede olmayan değer yazma.
- Şarkı sözü gösterme. Telifli.
- Reddit, Ekşi ya da başka kullanıcı içeriği kazıma. Havuz kullanıcıların
  kendi yazdıklarıyla büyür.
- Bir ekranda bir soru. Asla iki soru aynı anda sorulmaz.
- Sonsuz akış, öneri listesi, bildirim yok.
- Espri yalnızca `modern_deyim` kartında. Başka hiçbir ekranda mizah yok.

## Bugünün deyimi

Kullanıcı yolunu seçtikten **sonra**, seçtiği dilin altında o çıkmazın
`modern_deyim` sütunundaki cümlesini göster. Kart biçiminde, tek satır,
büyük punto, süssüz. Üstünde küçük gri yazıyla: "bugünün deyimi".

Bu tek eğlenceli andır ve yeri kesindir. Vaka ekranında, bağlam sorusunda
ya da ayırt edici soruda **asla** espri yapma; kişi o an derdinin içinde
ve hafiflik hafife alma gibi durur. Gerilim çözüldükten sonra gülümsetmek
ekranı insanlaştırır, öncesinde ise güveni bitirir.

Deyimin altında tek düğme: "Bu benim" — basılırsa kullanıcının defterine
kaydedilir. Puan, rozet, paylaşım sayacı yok.

## Son ekran

Seçim yapıldıktan sonra: "On gün sonra soracağız: ne yaptın, ne oldu?"
Altında "Benim Alanım" düğmesi — kullanıcının geçmiş kayıtlarını listeler.
Her kayıtta kendi yazdığı cümle, seçtiği yol ve tarih görünür.
