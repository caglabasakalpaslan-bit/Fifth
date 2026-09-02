#!/usr/bin/env python3
"""Veriyi şablona gömüp tek dosyalık haritayı üretir.
    python3 arac/olustur.py
"""
import json, pathlib
kok = pathlib.Path(__file__).resolve().parent.parent
d = json.load(open(kok/"veri/atasozleri.json", encoding="utf-8"))
n = len(d["kayitlar"])
cift = sum(len(r.get("c", [])) for r in d["kayitlar"]) // 2
birlesim = len({tuple(sorted(r["k"])) for r in d["kayitlar"]})
foot = (f"Z ekseni 0 ise söz söylenince anlaşılır, 1 ise ancak yaşayan bilir. "
        f"{n} sözde {cift} çelişki çifti var; her biri iki koşulu ayıran bir "
        f"soru barındırır. Kutuplar birbirinin zıddı değil üst üste binen "
        f"alanlar olduğu için 36 olası ikiliden {birlesim} tanesi kullanılmış.")
html = open(kok/"arac/sablon.html", encoding="utf-8").read()
html = (html.replace("__DATA__", json.dumps(d, ensure_ascii=False))
            .replace("__N__", str(n)).replace("__FOOT__", foot))
(kok/"cikti").mkdir(exist_ok=True)
open(kok/"cikti/harita.html", "w", encoding="utf-8").write(html)
m = open(kok/"arac/motor_sablonu.html", encoding="utf-8").read()
open(kok/"cikti/motor.html", "w", encoding="utf-8").write(
    m.replace("__DATA__", json.dumps(d, ensure_ascii=False)))
print("cikti/motor.html yazıldı")
print(f"cikti/harita.html yazıldı — {n} kayıt, {cift} çelişki çifti")
