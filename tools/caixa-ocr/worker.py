import os, re, json, sys, urllib.request
from datetime import datetime
try:
    import pytesseract
    from PIL import Image, ImageOps, ImageEnhance
except ImportError as e:
    raise SystemExit(f"Dependência ausente: {e}")

def norm_money(s):
    s=s.replace("R$","").replace(" ","").replace(".","").replace(",",".")
    try: return float(s)
    except: return None

def parse(text):
    pago=bool(re.search(r"\bPAGO\b",text,re.I))
    vals=[]
    for m in re.finditer(r"(?:R\$\s*)?\d{1,4}(?:\.\d{3})*,\d{2}",text):
        v=norm_money(m.group(0))
        if v and 0 < v < 10000 and v not in vals: vals.append(v)
    dates=[]
    for m in re.finditer(r"\b(\d{1,2})[\/.-](\d{1,2})[\/.-](\d{2,4})\b",text):
        d,mo,y=m.groups(); y=int(y); y=y+2000 if y<100 else y
        try: dates.append(datetime(y,int(mo),int(d)).date().isoformat())
        except: pass
    receipt=None
    m=re.search(r"(?:RECIBO|N[º°O.]?)\s*[:#-]?\s*(\d{1,10})",text,re.I)
    if m: receipt=m.group(1)
    return {"marcado_pago":pago,"valor_candidatos":vals,"data_candidatos":list(dict.fromkeys(dates)),"numero_recibo":receipt}

def main():
    image_url=os.environ.get("OCR_IMAGE_URL")
    out=os.environ.get("OCR_OUTPUT","ocr-result.json")
    if not image_url: raise SystemExit("OCR_IMAGE_URL ausente")
    urllib.request.urlretrieve(image_url,"/tmp/caixa-input")
    img=Image.open("/tmp/caixa-input").convert("L")
    img=ImageOps.autocontrast(img)
    img=ImageEnhance.Contrast(img).enhance(1.5)
    text=pytesseract.image_to_string(img,lang="por",config="--oem 3 --psm 6")
    # Texto bruto NÃO é persistido: pode conter dados pessoais do recibo.
    result={"ok":True,"engine":"tesseract-native","campos":parse(text)}
    with open(out,"w",encoding="utf-8") as f: json.dump(result,f,ensure_ascii=False,indent=2)
    print(json.dumps(result,ensure_ascii=False))
if __name__=="__main__": main()
