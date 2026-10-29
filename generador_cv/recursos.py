"""Graphic assets created locally. No bundled fonts, third-party icons or user photos."""
import math
from pathlib import Path
from PIL import Image, ImageDraw

COLORS = {"profile":"user", "experience":"briefcase", "skills":"code", "project":"folder",
          "education":"cap", "language":"globe", "other":"dots"}

def _color(value):
    raw = value.lstrip('#')
    if len(raw) != 6 or any(c not in '0123456789abcdefABCDEF' for c in raw):
        raise ValueError('Los colores deben tener formato HEX de seis cifras')
    return tuple(bytes.fromhex(raw))

def wavy_photo(source, dest, cfg):
    """Crop photograph and add subtle 5-lobed, anti-aliased gray frame."""
    src = Image.open(source).convert('RGB')
    high, size = 900, 450
    side = min(src.size)
    x, y = (src.width-side)//2, (src.height-side)//2
    src = src.crop((x,y,x+side,y+side)).resize((high,high),Image.Resampling.LANCZOS)
    amp=float(cfg.get('wave_amplitude', 5.3)); thickness=float(cfg.get('wave_thickness', 9))
    if not 0 <= amp <= 15 or not 2 <= thickness <= 22: raise ValueError('Ondulación fuera de rango')
    r0= high*.465
    def make_mask(r):
        mask=Image.new('L',(high,high)); d=ImageDraw.Draw(mask)
        coords=[]
        for k in range(1440):
            t=k*2*math.pi/1440
            rad=r + amp*high/450*math.sin(5*t+.3) + 1.4*high/450*math.sin(2*t-.2)
            coords.append((high/2+rad*math.cos(t), high/2+rad*math.sin(t)))
        d.polygon(coords,fill=255)
        return mask
    ring=Image.new('RGBA',(high,high),(*_color(cfg['wave_color']),255))
    ring.putalpha(make_mask(r0))
    src_rgba=src.convert('RGBA')
    src_rgba.putalpha(make_mask(r0-thickness*high/450))
    ring.alpha_composite(src_rgba)
    ring=ring.resize((size,size),Image.Resampling.LANCZOS)
    dest=Path(dest);dest.parent.mkdir(parents=True,exist_ok=True)
    ring.save(dest)
    return dest

def icon(category, dest, color='6E7073'):
    """Simple original 1-bit-ish line drawings, rendered as antialiased PNG."""
    kind=COLORS.get(category,'dots'); C=(*_color(color),255)
    im=Image.new('RGBA',(96,96),(255,255,255,0));d=ImageDraw.Draw(im)
    kw=dict(fill=None,outline=C,width=6)
    if kind=='user':
        d.ellipse((35,14,61,40),**kw);d.arc((18,38,78,95),190,350,fill=C,width=6)
    elif kind=='briefcase':
        d.rounded_rectangle((13,31,83,76),radius=5,**kw);d.rectangle((37,19,59,32),**kw);d.line((13,49,48,57,83,49),fill=C,width=5)
    elif kind=='code':
        d.line((39,24,19,47,39,69),fill=C,width=7,joint='curve');d.line((57,24,77,47,57,69),fill=C,width=7,joint='curve')
    elif kind=='folder':
        d.line((12,32,12,76,84,76,84,40,47,40,37,28,12,28,12,32),fill=C,width=6,joint='curve')
    elif kind=='cap':
        d.line((8,36,48,18,88,36,48,55,8,36),fill=C,width=6,joint='curve');d.line((26,48,26,67,48,76,70,67,70,48),fill=C,width=5)
    elif kind=='globe':
        d.ellipse((14,14,82,82),**kw);d.ellipse((31,14,65,82),**kw);d.line((14,47,82,47),fill=C,width=5)
    else:
        for x in (24,48,72):d.ellipse((x-5,43,x+5,53),fill=C)
    dest=Path(dest);dest.parent.mkdir(parents=True,exist_ok=True)
    im.resize((32,32),Image.Resampling.LANCZOS).save(dest)
    return dest

def corner(which, dest, cfg):
    """Square transparent-ish corner over a white page, for a rounded editable header grid."""
    N=160
    image=Image.new('RGB',(N,N),'white'); px=image.load(); radius=N
    cx = N if which.endswith('l') else 0
    cy = N if which.startswith('t') else 0
    base=_color(cfg['header_bg'])
    for y in range(N):
        for x in range(N):
            if (x+.5-cx)**2+(y+.5-cy)**2 <= radius**2:
                px[x,y]=base
    dest=Path(dest);dest.parent.mkdir(parents=True,exist_ok=True)
    image.save(dest)
    return dest
