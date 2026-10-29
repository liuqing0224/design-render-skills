#!/usr/bin/env python3
"""Aspect-preserving LANCZOS image resize. No generated detail. Requires Pillow."""
import argparse,io,json
from pathlib import Path
from PIL import Image,ImageOps
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('input',type=Path);p.add_argument('output',type=Path)
p.add_argument('--width',type=int);p.add_argument('--height',type=int)
a=p.parse_args()
if not a.width and not a.height:p.error('provide --width or --height')
if any(v is not None and v<=0 for v in [a.width,a.height]):p.error('dimensions must be positive')
if a.output.exists() or a.output.resolve()==a.input.resolve():p.error('output exists; choose a new filename')
if a.output.suffix.lower()!='.png':p.error('output must be PNG to preserve channels without lossy re-encoding')
with Image.open(a.input) as source:
 source.load();im=ImageOps.exif_transpose(source);info=im.info.copy()
 if im.mode=='P':im=im.convert('RGBA' if 'transparency' in info else 'RGB')
 w,h=im.size
 ow=a.width or max(1,round(w*a.height/h));oh=a.height or max(1,round(h*a.width/w))
 if a.width and a.height and abs(oh-ow*h/w)>1:p.error('target dimensions would distort aspect ratio; provide only one dimension')
 if ow*oh>100_000_000:p.error('requested size exceeds 100 million pixels')
 result=im.resize((ow,oh),Image.Resampling.LANCZOS)
 meta={k:info[k] for k in ['icc_profile','dpi','exif'] if k in info}
 buf=io.BytesIO();result.save(buf,format='PNG',**meta)
 a.output.parent.mkdir(parents=True,exist_ok=True)
 with a.output.open('xb') as f:f.write(buf.getvalue())
 print(json.dumps({'method':'LANCZOS interpolation; no inferred detail','input_pixels':[w,h],'output_pixels':[ow,oh],'alpha':'A' in result.getbands(),'output':str(a.output.resolve())},ensure_ascii=False))
