from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630

INK       = (24,  32,  28)
INK_SOFT  = (61,  73,  67)
MUTED     = (111, 122, 115)
CREAM     = (247, 243, 234)
PAPER     = (255, 253, 248)
STONE     = (231, 224, 211)
MOSS      = (79,  111, 82)
MOSS_DARK = (48,  71,  52)
CLAY      = (184, 107, 75)
GOLD      = (198, 161, 91)

img = Image.new('RGB', (W, H), CREAM)
draw = ImageDraw.Draw(img, 'RGBA')

# Subtle warm gradient background
for y in range(H):
    t = y / H
    r = int(247 + (255 - 247) * t)
    g = int(243 + (253 - 243) * t)
    b = int(234 + (248 - 234) * t)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# Left accent bar
draw.rectangle([0, 0, 5, H], fill=MOSS)

# Top-right gold accent
draw.rectangle([W-220, 0, W, 4], fill=GOLD)

# --- Report card ---
cx, cy = 680, 80
cw, ch = 460, 460
r = 20

# Shadow
draw.rounded_rectangle([cx+6, cy+8, cx+cw+6, cy+ch+8], radius=r, fill=(24, 32, 28, 18))
# Body
draw.rounded_rectangle([cx, cy, cx+cw, cy+ch], radius=r, fill=PAPER)
# Border
draw.rounded_rectangle([cx, cy, cx+cw, cy+ch], radius=r, fill=None, outline=(24, 32, 28, 25), width=1)

# Card header stripe
draw.rounded_rectangle([cx, cy, cx+cw, cy+52], radius=r, fill=MOSS_DARK)
draw.rectangle([cx, cy+32, cx+cw, cy+52], fill=MOSS_DARK)

def load_font(size, bold=False):
    candidates = [
        '/System/Library/Fonts/Supplemental/Arial Bold.ttf',
        '/System/Library/Fonts/Supplemental/Arial.ttf',
        '/System/Library/Fonts/Helvetica.ttc',
        '/System/Library/Fonts/SFNS.ttf',
    ] if bold else [
        '/System/Library/Fonts/Supplemental/Arial.ttf',
        '/System/Library/Fonts/Helvetica.ttc',
        '/System/Library/Fonts/SFNS.ttf',
    ]
    for p in candidates:
        try:
            return ImageFont.truetype(p, size)
        except:
            pass
    return ImageFont.load_default()

f_label  = load_font(11)
f_title  = load_font(15, bold=True)
f_body   = load_font(13)
f_sm     = load_font(11)
f_sect   = load_font(10)
f_h1     = load_font(44, bold=True)
f_h2     = load_font(44, bold=True)
f_sub    = load_font(18)
f_brand  = load_font(20, bold=True)
f_domain = load_font(13)
f_tag    = load_font(13)
f_mark   = load_font(22, bold=True)
f_foot   = load_font(14)

# Card header label
draw.text((cx+20, cy+16), 'MONTHLY REVIEW BRIEF', font=f_label, fill=(198, 230, 200))

# Property name
draw.text((cx+20, cy+68), 'Casa Mariposa Boutique Hotel', font=f_title, fill=INK)
draw.text((cx+20, cy+88), 'Antigua, Guatemala  ·  90-day  ·  84 reviews', font=f_sm, fill=MUTED)

# Divider
draw.line([(cx+20, cy+112), (cx+cw-20, cy+112)], fill=STONE, width=1)

# Signal box
draw.rounded_rectangle([cx+20, cy+124, cx+cw-20, cy+200], radius=8, fill=CREAM)
draw.text((cx+30, cy+134), 'TOP SIGNAL', font=f_sect, fill=MOSS)
draw.text((cx+30, cy+150), 'Staff warmth and walkable location are', font=f_body, fill=INK_SOFT)
draw.text((cx+30, cy+167), 'the most repeated positives. 31% of', font=f_body, fill=INK_SOFT)
draw.text((cx+30, cy+184), 'reviews mention personal service.', font=f_sm, fill=MUTED)

# Priority actions heading
draw.text((cx+20, cy+218), 'PRIORITY ACTIONS', font=f_sect, fill=CLAY)

actions = [
    ('1', 'Add parking info to pre-arrival email', 'High'),
    ('2', 'Use walkable location in booking copy', 'High'),
    ('3', 'Create noise-complaint response template', 'Med'),
]
ay = cy + 236
for num, action, priority in actions:
    draw.ellipse([cx+20, ay-1, cx+34, ay+13], fill=MOSS)
    draw.text((cx+24, ay), num, font=f_sm, fill=PAPER)
    draw.text((cx+42, ay), action, font=f_body, fill=INK_SOFT)
    tag_color = CLAY if priority == 'High' else GOLD
    draw.rounded_rectangle([cx+cw-64, ay-2, cx+cw-20, ay+14], radius=4, fill=(*tag_color, 30))
    draw.text((cx+cw-56, ay), priority, font=load_font(10), fill=tag_color)
    ay += 28

# Divider
draw.line([(cx+20, ay+6), (cx+cw-20, ay+6)], fill=STONE, width=1)
ay += 20

# Guest language chips
draw.text((cx+20, ay), 'GUEST LANGUAGE', font=f_sect, fill=MUTED)
ay += 16
phrases = ['"felt like coming home"', '"steps from everything"', '"staff remembered us"']
px = cx + 20
for phrase in phrases:
    tw = draw.textlength(phrase, font=f_sm)
    draw.rounded_rectangle([px-6, ay-3, px+tw+6, ay+13], radius=5, fill=STONE)
    draw.text((px, ay), phrase, font=f_sm, fill=INK_SOFT)
    px += tw + 14
    if px > cx + cw - 40:
        break

# --- Left side ---
# RB logomark
mx, my = 72, 72
draw.rounded_rectangle([mx, my, mx+52, my+52], radius=12, fill=MOSS)
draw.text((mx+10, my+12), 'RB', font=f_mark, fill=PAPER)

draw.text((mx+64, my+8),  'ReviewBriefs', font=f_brand, fill=INK)
draw.text((mx+64, my+32), 'reviewbriefs.com', font=f_domain, fill=MUTED)

# Headline
hy = 180
draw.text((72, hy),    'Turn guest reviews into', font=f_h1, fill=INK)
draw.text((72, hy+54), 'client-ready insights.', font=f_h2, fill=MOSS)

# Subheadline
draw.text((72, hy+118), 'Praise themes, reputation risks,', font=f_sub, fill=INK_SOFT)
draw.text((72, hy+142), 'marketing opportunities, action lists.', font=f_sub, fill=INK_SOFT)

# Tags
ty = hy + 200
tags = [('For hospitality agencies', False), ('For boutique hotels', False), ('Private beta', True)]
tx = 72
for label, accent in tags:
    tw = draw.textlength(label, font=f_tag)
    bg = MOSS if accent else STONE
    fg = PAPER if accent else INK_SOFT
    draw.rounded_rectangle([tx-10, ty-5, tx+tw+10, ty+19], radius=12, fill=bg)
    draw.text((tx, ty), label, font=f_tag, fill=fg)
    tx += tw + 24

# Bottom strip
draw.rectangle([0, H-44, W, H], fill=MOSS_DARK)
draw.text((72, H-28), 'reviewbriefs.com', font=f_foot, fill=(198, 230, 200))
draw.text((W-290, H-28), 'Guest review intelligence', font=f_foot, fill=(160, 195, 163))

os.makedirs('assets/images', exist_ok=True)
img.save('assets/images/og-image.png', 'PNG', optimize=True)
print('Saved 1200x630 OG image')
