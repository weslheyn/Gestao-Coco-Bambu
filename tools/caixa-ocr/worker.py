import os, re, json, urllib.request
from datetime import datetime
import pytesseract
from PIL import Image, ImageOps, ImageEnhance, ImageFilter

def norm_money(s):
    s=s.replace("R$","").replace(" ","").replace(".","").replace(",",".")
    try: return float(s)
    except: return None

def parse(text):
    pago=bool(re.search(r"\bPAGO\b",text,re.I))
    vals=[]
    for m in re.finditer(r"(?:R\$\s*)?\d{1,4}(?:\.\d{3})*,\d{2}",text):
        v=norm_money(m.group(0))
        if v and 10 <= v < 10000 and v not in vals: vals.append(v)
    dates=[]
    for m in re.finditer(r"\b(\d{1,2})[\/.-](\d{1,2})[\/.-](\d{2,4})\b",text):
        d,mo,y=m.groups(); y=int(y); y=y+2000 if y<100 else y
        try: dates.append(datetime(y,int(mo),int(d)).date().isoformat())
        except: pass
    receipt=None
    patterns=[r"(?:RECIBO|RECIB0)\s*(?:N[º°O.]?)?\s*[:#-]?\s*(\d{1,10})",r"N[º°O.]?\s*[:#-]?\s*(\d{1,10})"]
    for p in patterns:
        m=re.search(p,text,re.I)
        if m:
            candidate=m.group(1)
            if len(candidate) >= 2:
                receipt=candidate
                break
    return {"marcado_pago":pago,"valor_candidatos":vals,"data_candidatos":list(dict.fromkeys(dates)),"numero_recibo":receipt}

def variants(img):
    g=ImageOps.grayscale(img)
    g=ImageOps.autocontrast(g)
    scale=max(1,2200//max(1,g.width))
    if scale>1: g=g.resize((g.width*scale,g.height*scale))
    yield "gray", ImageEnhance.Contrast(g).enhance(1.8)
    sharp=g.filter(ImageFilter.SHARPEN)
    yield "sharp", ImageEnhance.Contrast(sharp).enhance(2.2)
    yield "bw160", g.point(lambda p: 255 if p>160 else 0)
    yield "bw190", g.point(lambda p: 255 if p>190 else 0)

def score(fields):
    return (4 if fields["numero_recibo"] else 0)+(3 if fields["data_candidatos"] else 0)+(3 if fields["valor_candidatos"] else 0)+(1 if fields["marcado_pago"] else 0)

def main():
    image_url=os.environ.get("OCR_IMAGE_URL")
    out=os.environ.get("OCR_OUTPUT","ocr-result.json")
    if not image_url: raise SystemExit("OCR_IMAGE_URL ausente")
    urllib.request.urlretrieve(image_url,"/tmp/caixa-input")
    img=Image.open("/tmp/caixa-input")
    best=None
    for variant_name,im in variants(img):
        for psm in (6,11,12,4):
            text=pytesseract.image_to_string(im,lang="por",config=f"--oem 3 --psm {psm}")
            fields=parse(text)
            candidate={"score":score(fields),"variant":variant_name,"psm":psm,"campos":fields}
            if best is None or candidate["score"]>best["score"]: best=candidate
    # O texto bruto existe apenas em memória durante cada tentativa e nunca é persistido.
    result={"ok":True,"engine":"tesseract-native","strategy":"multi-pass","quality_score":best["score"],"campos":best["campos"]}
    with open(out,"w",encoding="utf-8") as f: json.dump(result,f,ensure_ascii=False,indent=2)
    print(json.dumps(result,ensure_ascii=False))
if __name__=="__main__": main()
