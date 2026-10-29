import io,json,subprocess,sys,tempfile,unittest
from pathlib import Path
from PIL import Image,ImageDraw
from PIL.PngImagePlugin import PngInfo
ROOT=Path(__file__).resolve().parents[1]
class ImageOpsTest(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.p=Path(self.tmp.name)
  self.im=Image.new('RGBA',(96,64),(0,0,0,0));d=ImageDraw.Draw(self.im);d.rectangle((12,12,74,50),fill=(32,120,180,255));d.line((12,12,74,50),fill=(240,120,30,128),width=3)
  self.src=self.p/'input.png';text=PngInfo();text.add_text('Description','test-image')
  self.im.save(self.src,compress_level=0,pnginfo=text)
 def run_tool(self,slug,script,*args,success=True):
  r=subprocess.run([sys.executable,str(ROOT/'skills'/slug/'scripts'/script),*map(str,args)],capture_output=True,text=True)
  if success:self.assertEqual(r.returncode,0,r.stderr);return json.loads(r.stdout)
  self.assertNotEqual(r.returncode,0);return r
 def test_png_lossless_preserves_pixels_and_alpha(self):
  out=self.p/'small.png';r=self.run_tool('evai-image-compress','compress.py',self.src,out)
  with Image.open(out) as actual:
   self.assertEqual(actual.size,self.im.size);self.assertEqual(actual.convert('RGBA').tobytes(),self.im.tobytes());self.assertEqual(actual.text['Description'],'test-image')
  self.assertTrue(r['pixel_lossless']);self.assertLess(out.stat().st_size,self.src.stat().st_size)
 def test_jpeg_passthrough_is_byte_identical(self):
  src=self.p/'original.jpg';self.im.convert('RGB').save(src)
  out=self.p/'copied.jpg';r=self.run_tool('evai-image-compress','compress.py',src,out)
  self.assertEqual(src.read_bytes(),out.read_bytes());self.assertEqual(r['saved_bytes'],0)
 def test_palette_transparency_survives_optimization(self):
  src=self.p/'palette.png';im=Image.new('P',(32,32),0);im.putpalette([0,0,0,255,0,0]+[0]*762);ImageDraw.Draw(im).rectangle((8,8,24,24),fill=1);im.save(src,transparency=0,compress_level=0)
  out=self.p/'palette-opt.png';self.run_tool('evai-image-compress','compress.py',src,out)
  with Image.open(src) as x,Image.open(out) as y:self.assertEqual(x.convert('RGBA').tobytes(),y.convert('RGBA').tobytes())
 def test_resize_is_labelled_not_lossless_and_preserves_alpha(self):
  out=self.p/'resized.png';r=self.run_tool('evai-image-compress','compress.py',self.src,out,'--max-width',48)
  self.assertEqual(r['output_pixels'],[48,32]);self.assertFalse(r['pixel_lossless'])
  with Image.open(out) as im:self.assertIn('A',im.getbands());self.assertEqual(im.getpixel((0,0))[3],0)
 def test_transparent_palette_resize_works(self):
  src=self.p/'palette.png';im=Image.new('P',(32,32),0);im.putpalette([0,0,0,255,0,0]+[0]*762);im.save(src,transparency=0)
  out=self.p/'resized.png';self.run_tool('evai-image-compress','compress.py',src,out,'--max-width',16)
  with Image.open(out) as x:self.assertEqual(x.getpixel((0,0))[3],0)
 def test_upscale_dimensions_alpha_and_input_unchanged(self):
  before=self.src.read_bytes();out=self.p/'large.png';r=self.run_tool('evai-image-upscale','upscale.py',self.src,out,'--width',192)
  self.assertEqual(r['output_pixels'],[192,128]);self.assertTrue(r['alpha']);self.assertEqual(before,self.src.read_bytes())
  with Image.open(out) as im:self.assertEqual(im.getpixel((0,0))[3],0)
 def test_upscale_rejects_distorting_dimensions(self):
  out=self.p/'bad.png';self.run_tool('evai-image-upscale','upscale.py',self.src,out,'--width',192,'--height',100,success=False);self.assertFalse(out.exists())
 def test_existing_outputs_are_never_overwritten(self):
  for slug,script,args in [('evai-image-compress','compress.py',[]),('evai-image-upscale','upscale.py',['--width',192]),('evai-image-to-lineart','lineart.py',[])]:
   out=self.p/(slug+'.png');out.write_bytes(b'preserve-me');self.run_tool(slug,script,self.src,out,*args,success=False);self.assertEqual(out.read_bytes(),b'preserve-me')
 def test_lineart_has_white_border_and_detected_structure(self):
  src=self.p/'shape.png';im=Image.new('RGB',(96,64),'white');ImageDraw.Draw(im).rectangle((20,16,72,48),fill='black');im.save(src)
  out=self.p/'line.png';r=self.run_tool('evai-image-to-lineart','lineart.py',src,out)
  with Image.open(out) as actual:
   self.assertEqual(actual.size,im.size);self.assertEqual(actual.getpixel((0,0)),255);self.assertGreater(list(actual.getdata()).count(0),20);self.assertEqual(actual.getpixel((48,32)),255)
 def test_upscale_respects_exif_orientation(self):
  src=self.p/'oriented.jpg';im=Image.new('RGB',(80,40),'red');exif=Image.Exif();exif[274]=6;im.save(src,exif=exif)
  out=self.p/'oriented-large.png';r=self.run_tool('evai-image-upscale','upscale.py',src,out,'--width',80)
  self.assertEqual(r['output_pixels'],[80,160])
 def test_animated_input_is_not_silently_flattened(self):
  src=self.p/'animated.png';a=Image.new('RGBA',(10,10),'red');b=Image.new('RGBA',(10,10),'blue');a.save(src,save_all=True,append_images=[b],duration=100,loop=0)
  self.run_tool('evai-image-compress','compress.py',src,self.p/'bad.png',success=False)
if __name__=='__main__':unittest.main(verbosity=2)
