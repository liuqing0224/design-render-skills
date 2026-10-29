#!/usr/bin/env python3
"""Pixel-lossless PNG optimization, or explicitly requested resize. Requires Pillow."""
import argparse,io,json,shutil
from pathlib import Path
from PIL import Image
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('input',type=Path);p.add_argument('output',type=Path)
p.add_argument('--max-width',type=int);p.add_argument('--max-height',type=int)
a=p.parse_args()
if any(v is not None and v<=0 for v in [a.max_width,a.max_height]):p.error('maximum dimensions must be positive')
if a.output.exists() or a.output.resolve()==a.input.resolve():p.error('output exists; choose a new filename')
original=a.input.read_bytes()
with Image.open(a.input) as im:
 im.load();size=im.size;info=im.info.copy()
 if getattr(im,'n_frames',1)>1:p.error('animated or multi-frame input is not supported')
 resize=bool(a.max_width or a.max_height)
 if resize:
  if a.output.suffix.lower()!='.png':p.error('resize output must be PNG; resize is not pixel-lossless')
  scale=min(1,(a.max_width or size[0])/size[0],(a.max_height or size[1])/size[1])
  result=im.convert('RGBA' if 'A' in im.getbands() or 'transparency' in info else 'RGB')
  result=result.resize((max(1,round(size[0]*scale)),max(1,round(size[1]*scale))),Image.Resampling.LANCZOS)
  method='resized; not pixel-lossless' if result.size!=size else 'no resize needed; PNG encoding'
 elif im.format=='PNG':
  if a.output.suffix.lower()!='.png':p.error('lossless PNG output must use .png')
  result=im.copy();method='pixel-lossless PNG optimization'
 else:
  if a.output.suffix.lower()!=a.input.suffix.lower():p.error('copy-through requires the same extension')
  result=None;method='unchanged copy; no lossless optimizer for this format'
 if result is not None:
  meta={k:info[k] for k in ['icc_profile','dpi','exif','transparency'] if k in info}
  if 'A' in result.getbands():meta.pop('transparency',None)
  from PIL.PngImagePlugin import PngInfo
  pnginfo=PngInfo()
  for k,v in im.text.items() if hasattr(im,'text') else []:
   if isinstance(v,str):pnginfo.add_itxt(k,v)
  buf=io.BytesIO();result.save(buf,format='PNG',optimize=True,compress_level=9,pnginfo=pnginfo,**meta)
  output=buf.getvalue()
  with Image.open(io.BytesIO(output)) as check:
   check.load();expected=result.convert('RGBA')
   if check.size!=result.size or check.convert('RGBA').tobytes()!=expected.tobytes():raise RuntimeError('PNG round-trip pixel verification failed')
  if not resize and len(output)>=len(original):output=original;method='unchanged original; optimized PNG was not smaller'
  out_size=result.size
 else:output=original;out_size=size
 a.output.parent.mkdir(parents=True,exist_ok=True)
 with a.output.open('xb') as f:f.write(output)
 print(json.dumps({'method':method,'input_bytes':len(original),'output_bytes':len(output),'saved_bytes':len(original)-len(output),'input_pixels':size,'output_pixels':out_size,'pixel_lossless':out_size==size,'metadata':'ICC, DPI, EXIF, PNG text retained where present; other ancillary chunks may not be retained','output':str(a.output.resolve())},ensure_ascii=False))
