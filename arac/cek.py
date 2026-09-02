#!/usr/bin/env python3
"""Açık kaynaklardan ham atasözü listesini indirir → veri/ham_liste.json
    python3 arac/cek.py
Kaynaklar: Abdullah-V/Turkce-Atasozleri-icin-API + futurk/turkce-atasozleri-deyimler
"""
import json, csv, re, io, zipfile, urllib.request, pathlib
csv.field_size_limit(10**7)
kok = pathlib.Path(__file__).resolve().parent.parent
Z = lambda u: zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(u, timeout=60).read()))

a = Z("https://codeload.github.com/Abdullah-V/Turkce-Atasozleri-icin-API/zip/refs/heads/master")
d = json.loads(a.read([n for n in a.namelist() if n.endswith("DATA.json")][0]))["data"]
liste = {s.strip() for h in d for s in d[h] if s.strip()}

b = Z("https://codeload.github.com/futurk/turkce-atasozleri-deyimler/zip/refs/heads/main")
raw = b.read([n for n in b.namelist() if n.endswith("atasozleri_ham.csv")][0]).decode()
anlam = {}
for r in csv.DictReader(io.StringIO(raw)):
    w = r["wikitext"]
    if "===Atasözü===" not in w and "===Deyim===" not in w: continue
    m = [re.sub(r"\{\{[^}]*\}\}|\[\[|\]\]|''", "", x).strip()
         for x in re.findall(r"^:\[\d+\]\s*(.+)$", w, re.M)]
    anlam[r["title"].strip()] = {"tur": "deyim" if "===Deyim===" in w else "atasözü",
                                 "anlam": [x for x in m if len(x) > 8][:2]}

hepsi = {s: {"s": s, "tur": "atasözü", "anlam": []} for s in liste}
for t, v in anlam.items():
    if t in hepsi: hepsi[t]["anlam"] = v["anlam"]
    else: hepsi[t] = {"s": t, "tur": v["tur"], "anlam": v["anlam"]}

kayit = sorted(hepsi.values(), key=lambda x: x["s"])
json.dump({"sayi": len(kayit), "kayitlar": kayit},
          open(kok/"veri/ham_liste.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print(f"{len(kayit)} kayıt — {sum(1 for k in kayit if k['anlam'])} tanesinin anlamı var")
