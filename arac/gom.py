"""İskeletleri gömer.

    pip install sentence-transformers
    python3 arac/gom.py

Hem hikâyelerin hem çıkmazların iskeletini aynı uzaya gömer; `veri/gomme.npz`
üretir. Ham metin gömülmez. Sebep: "sormuyorum artık" ile "size döneceğiz
modu" kelime olarak benzemez, iskelet olarak aynıdır. Türkçe ekler de bu
yüzden sorun olmaktan çıkar; iskelet zaten soyut ve temiz cümledir.

Model: intfloat/multilingual-e5-small (çok dilli, küçük, yerelde çalışır).
Barındırılmış istersen Voyage AI `voyage-multilingual-2` aynı işi görür;
tek değişecek yer `gom()` fonksiyonu.
"""
import json, os
import numpy as np

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_model = None

def gom(metinler, tur="passage"):
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer("intfloat/multilingual-e5-small")
    # e5 ailesi passage/query ön ekiyle çalışır
    return _model.encode([f"{tur}: {m}" for m in metinler], normalize_embeddings=True)

def main():
    h = json.load(open(os.path.join(KOK, "veri", "hikayeler.json"), encoding="utf-8"))["kayitlar"]
    c = json.load(open(os.path.join(KOK, "cikmaz", "cikmazlar.json"), encoding="utf-8"))["kayitlar"]
    np.savez(os.path.join(KOK, "veri", "gomme.npz"),
             h_id=np.array([r["id"] for r in h]), h_v=gom([r["i"] for r in h]),
             c_id=np.array([r["id"] for r in c]), c_v=gom([r["iskelet"] for r in c]))
    print("gömüldü:", len(h), "hikâye,", len(c), "çıkmaz")

if __name__ == "__main__":
    main()
