#!/usr/bin/env python3
"""taranan.jsonl → veri/atasozleri.json içine ekler (id atar, tekrarı atlar)."""
import json, pathlib
kok = pathlib.Path(__file__).resolve().parent.parent
d = json.load(open(kok/"veri/atasozleri.json", encoding="utf-8"))
var = {r["s"] for r in d["kayitlar"]}
n = max(int(r["id"][1:]) for r in d["kayitlar"])
mek = set(d["mekanizmalar"]); ekli = atlanan = 0
yol = kok/"veri/taranan.jsonl"
if not yol.exists(): raise SystemExit("veri/taranan.jsonl yok — önce arac/tara.py çalıştır")
for satir in open(yol, encoding="utf-8"):
    try: r = json.loads(satir)
    except Exception: continue
    if r["s"] in var: atlanan += 1; continue
    if r.get("m") not in mek and r.get("m") != "?": atlanan += 1; continue
    n += 1
    d["kayitlar"].append({"id": f"A{n:03d}", "s": r["s"], "k": r["k"], "p": r["p"],
                          "z": r["z"], "m": r["m"], "i": r["i"], "f": r["f"]})
    var.add(r["s"]); ekli += 1
json.dump(d, open(kok/"veri/atasozleri.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print(f"{ekli} eklendi, {atlanan} atlandı → toplam {len(d['kayitlar'])}")
