#!/usr/bin/env python3
"""Extract raster edge lineart; does not create CAD or inferred geometry. Requires Pillow."""
import argparse,io,json
from pathlib import Path
from PIL import Image,ImageOps,ImageFilter,ImageDraw
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('input',type=Path);p.add_argument('output',type=Path)
p.add_argument('--blur',type=float,default=1.0);p.add_argument('--threshold',type=int,default=24)
a=p.parse_args()
if a.blur<0 or not 0<=a.threshold<=255:p.error('blur must be nonnegative and threshold must be 0..255')
if a.output.exists() or a.output.resolve()==a.input.resolve():p.error('output exists; choose a new filename')
if a.output.suffix.lower()!='.png':p.error('output must be PNG')
with Image.open(a.input) as source:
 source.load();im=ImageOps.exif_transpose(source).convert('RGBA')
 bg=Image.new('RGBA',im.size,'white');bg.alpha_composite(im)
 gray=ImageOps.grayscale(bg).filter(ImageFilter.GaussianBlur(a.blur))
 edges=gray.filter(ImageFilter.FIND_EDGES)
 line=edges.point(lambda v:0 if v>a.threshold else 255).convert('L')
 if min(line.size)>2:ImageDraw.Draw(line).rectangle([0,0,line.width-1,line.height-1],outline=255,width=1)
 buf=io.BytesIO();line.save(buf,format='PNG',optimize=True)
 a.output.parent.mkdir(parents=True,exist_ok=True)
 with a.output.open('xb') as f:f.write(buf.getvalue())
 print(json.dumps({'method':'raster edge extraction; not CAD','output_pixels':line.size,'threshold':a.threshold,'blur':a.blur,'output':str(a.output.resolve())},ensure_ascii=False))
