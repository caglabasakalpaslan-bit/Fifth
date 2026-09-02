#!/usr/bin/env python3
"""Veri setini denetler ve kapsama raporu basar.

    python3 arac/dogrula.py veri/atasozleri.json
"""
import json, sys, re
from collections import Counter

KUTUP = {"MEKAN","ILISKI","ZIHIN","IS","DUYGU","PARA","BEDEN","ANLAM"}

# İskelette görülmemesi gereken somut isimler. Sızıntı testi bunun üzerinden.
SOMUT = """ateş kuş horoz yorgan göz diş kapı
deniz ağaç gül diken bal arı kedi köpek kurt koyun tavuk yumurta ekmek
çuval testi değirmen kervan deve balık soğan üzüm demir mum akçe altın
komşu terzi imam derviş aslan tilki saksağan minare fincan kahve karpuz
koltuk yastık ayı çorba tencere kapak""".split()


def kontrol(yol):
    d = json.load(open(yol, encoding="utf-8"))
    kayit = d["kayitlar"]
    mek = set(d["mekanizmalar"])
    hata, uyari = [], []
    gorulen = set()

    for r in kayit:
        rid = r.get("id", "?")

        for alan in ("id","s","k","p","z","m","i","f"):
            if alan not in r:
                hata.append(f"{rid}: '{alan}' alanı eksik")

        if rid in gorulen:
            hata.append(f"{rid}: id tekrar ediyor")
        gorulen.add(rid)

        k = r.get("k", [])
        if not 1 <= len(k) <= 2:
            hata.append(f"{rid}: kutup sayısı {len(k)}, 1 veya 2 olmalı")
        for p in k:
            if p not in KUTUP:
                hata.append(f"{rid}: bilinmeyen kutup '{p}'")

        p = r.get("p", 0)
        if not -1 <= p <= 1:
            hata.append(f"{rid}: p aralık dışı ({p})")
        z = r.get("z", 0)
        if not 0 <= z <= 1:
            hata.append(f"{rid}: z aralık dışı ({z})")

        m = r.get("m")
        if m not in mek and m != "?":
            hata.append(f"{rid}: bilinmeyen mekanizma '{m}'")
        if m == "?":
            uyari.append(f"{rid}: mekanizma atanmamış — elle bak")

        # Somut isim sızıntısı: iskelet alan-bağımsız olmalı
        isk = r.get("i", "").lower()
        for w in SOMUT:
            if re.search(rf"(?<![a-zçğıöşü]){w}(?![a-zçğıöşü])", isk):
                uyari.append(f"{rid}: iskelette somut isim geçiyor → '{w}'")

        if not r.get("i","").endswith("."):
            uyari.append(f"{rid}: iskelet cümle olarak bitmiyor")

        for c in r.get("c", []):
            if c not in {x["id"] for x in kayit}:
                hata.append(f"{rid}: çelişki hedefi yok '{c}'")

    # Zıt polarite: çelişen iki söz aynı yöne çağıramaz
    for r in kayit:
        for c in r.get("c", []):
            o = {x["id"]: x for x in kayit}[c]
            if (r["p"] > 0) == (o["p"] > 0) or abs(r["p"] - o["p"]) < 0.6:
                hata.append(f"{r['id']} ↔ {c}: çelişki değil, ikisi de aynı yöne "
                            f"çağırıyor ({r['p']:+} / {o['p']:+})")

    # Her çelişki çiftinin ayırt edici sorusu olmalı
    tanimli = {tuple(sorted((p["a"], p["b"]))) for p in d.get("ciftler", [])}
    for r in kayit:
        for c in r.get("c", []):
            if tuple(sorted((r["id"], c))) not in tanimli:
                uyari.append(f"{r['id']} ↔ {c}: ayırt edici soru yazılmamış")
    for p in d.get("ciftler", []):
        if not p.get("soru","").endswith("?"):
            hata.append(f"{p['a']}↔{p['b']}: soru alanı soru değil")

    # Karşılıklılık: çelişki tek yönlü kalmamalı
    idx = {r["id"]: r for r in kayit}
    for r in kayit:
        for c in r.get("c", []):
            if r["id"] not in idx[c].get("c", []):
                uyari.append(f"{r['id']} ↔ {c}: çelişki tek yönlü")

    print(f"{len(kayit)} kayıt okundu\n")
    if hata:
        print(f"HATA ({len(hata)})")
        for h in hata: print("  " + h)
        print()
    if uyari:
        print(f"UYARI ({len(uyari)})")
        for u in uyari[:30]: print("  " + u)
        if len(uyari) > 30: print(f"  ... ve {len(uyari)-30} tane daha")
        print()
    if not hata and not uyari:
        print("Temiz.\n")

    # ---- kapsama ----
    kc = Counter(p for r in kayit for p in r["k"])
    print("Kutup dağılımı")
    for p, n in kc.most_common():
        print(f"  {p:<8} {'█'*round(n/max(kc.values())*26):<26} {n}")

    mc = Counter(r["m"] for r in kayit)
    print("\nMekanizma dağılımı")
    for m, n in mc.most_common():
        print(f"  {m:<20} {'█'*round(n/max(mc.values())*20):<20} {n}")

    # Harita hangi bölgelerde boş?
    print("\nHarita yoğunluğu (satır: z yüksek → düşük, sütun: kıs → aç)")
    grid = [[0]*4 for _ in range(4)]
    for r in kayit:
        c = min(3, int((r["p"]+1)/2*4))
        s = 3 - min(3, int(r["z"]*4))
        grid[s][c] += 1
    etiket = ["z .75-1","z .50-.75","z .25-.50","z 0-.25"]
    print("           kıs      orta-    orta+     aç")
    for e, row in zip(etiket, grid):
        print(f"  {e:<10}" + "".join(f"{v:^9}" for v in row))
    bos = sum(1 for row in grid for v in row if v == 0)
    seyrek = sum(1 for row in grid for v in row if 0 < v <= 2)
    print(f"\n  boş hücre: {bos}/16   seyrek (≤2): {seyrek}/16")

    cift = sum(len(r.get("c", [])) for r in kayit) // 2
    print(f"\nÇelişki çifti: {cift}   ayırt edici soru: {len(d.get('ciftler', []))}")

    birlesim = Counter(tuple(sorted(r["k"])) for r in kayit)
    print(f"Kullanılan kutup birleşimi: {len(birlesim)} / 36 olası")

    return 1 if hata else 0


if __name__ == "__main__":
    sys.exit(kontrol(sys.argv[1] if len(sys.argv) > 1 else "veri/atasozleri.json"))
