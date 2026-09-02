#!/usr/bin/env python3
"""Ham listeyi sınıflandırır. Kesilirse kaldığı yerden devam eder.

    export ANTHROPIC_API_KEY=sk-...
    pip install anthropic
    python3 arac/tara.py --adet 200          # 200 tane işle, dur
    python3 arac/tara.py --adet 200 --iki    # her sözü iki kez oku, uyuşmazlığı işaretle
    python3 arac/tara.py                     # hepsini işle

Çıktı: veri/taranan.jsonl  (her satır bir kayıt, araya girilebilir)
Uyuşmazlık: veri/celiskili.jsonl (--iki modunda p/z farkı büyük olanlar)
"""
import json, os, sys, time, pathlib, argparse
from anthropic import Anthropic

kok = pathlib.Path(__file__).resolve().parent.parent
MODEL = "claude-sonnet-4-6"

ap = argparse.ArgumentParser()
ap.add_argument("--adet", type=int, default=0, help="kaç yeni kayıt işlensin (0 = hepsi)")
ap.add_argument("--iki", action="store_true", help="her sözü iki kez oku, tutarlılığı ölç")
ap.add_argument("--parti", type=int, default=8, help="tek istekte kaç söz")
a = ap.parse_args()

prompt = open(kok/"prompt/01-siniflandirici.md", encoding="utf-8").read()
ham = json.load(open(kok/"veri/ham_liste.json", encoding="utf-8"))["kayitlar"]

# Elle kodlanmış set zaten var, onları atla
elle = {r["s"] for r in json.load(open(kok/"veri/atasozleri.json", encoding="utf-8"))["kayitlar"]}
cikti = kok/"veri/taranan.jsonl"
bitmis = set()
if cikti.exists():
    for satir in open(cikti, encoding="utf-8"):
        try: bitmis.add(json.loads(satir)["s"])
        except Exception: pass

kalan = [k for k in ham if k["s"] not in elle and k["s"] not in bitmis]
if a.adet: kalan = kalan[:a.adet]
print(f"{len(bitmis)} bitmiş · {len(kalan)} işlenecek · model {MODEL}")
if not kalan: sys.exit(0)

ist = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

def oku(parti):
    """Bir parti sözü sınıflandır, JSON listesi döndür."""
    girdi = "\n".join(
        f"{i+1}. {k['s']}" + (f"   [anlamı: {k['anlam'][0][:160]}]" if k["anlam"] else "")
        for i, k in enumerate(parti))
    y = ist.messages.create(
        model=MODEL, max_tokens=4000,
        system=prompt + "\n\nSana numaralı bir liste verilecek. Her satır için bir JSON "
                        "nesnesi üret ve hepsini tek bir JSON dizisi içinde döndür. "
                        "Dizi dışında hiçbir şey yazma.",
        messages=[{"role": "user", "content": girdi}])
    m = "".join(b.text for b in y.content if b.type == "text").strip()
    m = m.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(m)

def yaz(yol, kayitlar):
    with open(yol, "a", encoding="utf-8") as f:
        for r in kayitlar:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

islenen = hata = celiski = 0
for i in range(0, len(kalan), a.parti):
    parti = kalan[i:i+a.parti]
    try:
        r1 = oku(parti)
        if a.iki:
            r2 = oku(parti)
            birlesik = []
            for x, y in zip(r1, r2):
                dp, dz = abs(x["p"]-y["p"]), abs(x["z"]-y["z"])
                x["tutarli"] = dp <= 0.2 and dz <= 0.2 and x["m"] == y["m"]
                if not x["tutarli"]:
                    x["ikinci"] = {"p": y["p"], "z": y["z"], "m": y["m"]}
                    celiski += 1
                    yaz(kok/"veri/celiskili.jsonl", [x])
                birlesik.append(x)
            r1 = birlesik
        yaz(cikti, r1)
        islenen += len(r1)
    except Exception as e:
        hata += len(parti)
        print(f"  parti atlandı: {type(e).__name__} {str(e)[:90]}")
        time.sleep(3)
    print(f"\r{islenen}/{len(kalan)}  hata {hata}" +
          (f"  uyuşmayan {celiski}" if a.iki else ""), end="", flush=True)

print(f"\n\nbitti → veri/taranan.jsonl")
if a.iki: print(f"uyuşmayanlar → veri/celiskili.jsonl (elle bak)")
print("sonra: python3 arac/birlestir.py && python3 arac/dogrula.py veri/atasozleri.json")
