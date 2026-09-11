"""Ham hikâyeleri kütüphaneye ekler.

    python3 arac/hikaye_ekle.py veri/ham_hikayeler.txt

Girdi dosyası: hikâyeler arasında boş satır. Satır başında `kaynak: ...`
varsa kaynak olarak alınır (eksi, reddit, kullanici, donus). Her hikâye
Claude'a prompt/02-hikaye.md ile okutulur, çıkan JSON `veri/hikayeler.json`
içindeki `kayitlar`a eklenir. Kesilirse kaldığı yerden devam eder (ham metnin
hash'i id olur, tekrar eklenmez).
"""
import hashlib, json, os, sys, time
import anthropic

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROMPT = open(os.path.join(KOK, "prompt", "02-hikaye.md"), encoding="utf-8").read()
CIKMAZ = json.load(open(os.path.join(KOK, "cikmaz", "cikmazlar.json"), encoding="utf-8"))
HEDEF = os.path.join(KOK, "veri", "hikayeler.json")

def kutuphane_ozeti():
    return "\n".join(f"{r['id']} | {r['ad']} | {r['iskelet']}" for r in CIKMAZ["kayitlar"])

def oku(yol):
    blok, kaynak = [], "bilinmiyor"
    for satir in open(yol, encoding="utf-8").read().split("\n") + [""]:
        if satir.strip() == "":
            if blok:
                yield kaynak, "\n".join(blok).strip()
                blok, kaynak = [], "bilinmiyor"
            continue
        if satir.startswith("kaynak:") and not blok:
            kaynak = satir.split(":", 1)[1].strip(); continue
        blok.append(satir)

def yukle():
    if os.path.exists(HEDEF):
        return json.load(open(HEDEF, encoding="utf-8"))
    return {"surum": "0.1", "not": "Hikâyeler iskeletiyle saklanır. Ham metin `ham` alanında, aramada kullanılmaz; arama iskelet üzerinden yapılır.", "kayitlar": []}

def main(yol):
    istemci = anthropic.Anthropic()
    veri = yukle(); var = {r["id"] for r in veri["kayitlar"]}
    sistem = PROMPT + "\n\n## Çıkmaz kütüphanesi\n" + kutuphane_ozeti()
    for kaynak, ham in oku(yol):
        hid = "H" + hashlib.sha1(ham.encode()).hexdigest()[:8]
        if hid in var: continue
        for deneme in range(3):
            try:
                c = istemci.messages.create(model="claude-sonnet-4-6", max_tokens=600, system=sistem,
                                            messages=[{"role": "user", "content": ham}])
                metin = c.content[0].text.replace("```json", "").replace("```", "").strip()
                k = json.loads(metin); break
            except Exception as e:
                print("hata", hid, e); time.sleep(2)
        else:
            continue
        k.update({"id": hid, "kaynak": kaynak, "ham": ham})
        veri["kayitlar"].append(k); var.add(hid)
        json.dump(veri, open(HEDEF, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(hid, k.get("m"), k.get("cikmaz"), "|", k.get("i", "")[:70])
    print("toplam", len(veri["kayitlar"]))

if __name__ == "__main__":
    main(sys.argv[1])
