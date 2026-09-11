"""Cümleden en yakın hikâyeleri ve çıkmazı bulur.

    python3 arac/bul.py "cevabı bildiğim için sormuyorum artık"

Akış: cümle → Claude iskeleti çıkarır (02-hikaye.md ile) → iskelet gömülür →
kosinüs ile en yakın 5 hikâye ve 2 çıkmaz. Mekanizma (m) tutuyorsa +0.1.
Puanı 0.75'in altındakiler gösterilmez; boş sonuç bir bulgudur.
"""
import json, os, sys
import numpy as np
import anthropic
from gom import gom

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ESIK = 0.75

def iskelet_cikar(cumle):
    prompt = open(os.path.join(KOK, "prompt", "02-hikaye.md"), encoding="utf-8").read()
    c = anthropic.Anthropic().messages.create(model="claude-sonnet-4-6", max_tokens=400, system=prompt,
                                              messages=[{"role": "user", "content": cumle}])
    return json.loads(c.content[0].text.replace("```json", "").replace("```", "").strip())

def bul(cumle, k=5):
    g = np.load(os.path.join(KOK, "veri", "gomme.npz"))
    h = {r["id"]: r for r in json.load(open(os.path.join(KOK, "veri", "hikayeler.json"), encoding="utf-8"))["kayitlar"]}
    c = {r["id"]: r for r in json.load(open(os.path.join(KOK, "cikmaz", "cikmazlar.json"), encoding="utf-8"))["kayitlar"]}
    q = iskelet_cikar(cumle)
    v = gom([q["i"]], tur="query")[0]
    def sirala(ids, vs, kaynak):
        p = vs @ v
        p = p + np.array([0.1 if kaynak[i].get("m") == q.get("m") else 0 for i in ids])
        sira = np.argsort(-p)
        return [(ids[i], float(p[i])) for i in sira if p[i] >= ESIK]
    return q, sirala(g["h_id"], g["h_v"], h)[:k], sirala(g["c_id"], g["c_v"], c)[:2]

if __name__ == "__main__":
    q, hik, cik = bul(" ".join(sys.argv[1:]))
    print("iskelet:", q["i"]); print("mekanizma:", q.get("m"))
    print("\nçıkmaz adayları:"); [print(f"  {i}  {p:.2f}") for i, p in cik] or print("  yok — kütüphanenin boşluğu")
    print("\nbenzer hikâyeler:"); [print(f"  {i}  {p:.2f}") for i, p in hik] or print("  yok")
