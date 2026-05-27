"""
Generates ReviewBriefs logo assets:
  assets/images/logo.svg          — horizontal (mark + wordmark)
  assets/images/logo-mark.svg     — mark only (square)
  assets/images/logo-light.svg    — horizontal on dark backgrounds
  assets/images/logo@2x.png       — 496x104 raster (Pillow)
  assets/images/logo-mark@2x.png  — 104x104 raster
"""

import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs('assets/images', exist_ok=True)

# ── SVG: Horizontal logo ────────────────────────────────────────────────────

LOGO_SVG = '''\
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 56" width="256" height="56" role="img" aria-label="ReviewBriefs">
  <title>ReviewBriefs</title>

  <!-- Mark: moss rounded square -->
  <rect x="0" y="0" width="56" height="56" rx="13" fill="#4F6F52"/>

  <!-- Inner highlight strip (top) -->
  <rect x="0" y="0" width="56" height="4" rx="2" fill="#6B9970" opacity="0.5"/>

  <!-- RB lettermark -->
  <!-- R -->
  <text
    x="14"
    y="38"
    font-family="'Inter', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, sans-serif"
    font-size="26"
    font-weight="800"
    letter-spacing="-1"
    fill="#FFFDF8"
  >RB</text>

  <!-- Wordmark: "Review" regular + "Briefs" bold -->
  <text
    x="72"
    y="37"
    font-family="'Inter', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, sans-serif"
    font-size="22"
    font-weight="400"
    fill="#18201C"
    letter-spacing="-0.3"
  >Review</text>
  <text
    x="155"
    y="37"
    font-family="'Inter', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, sans-serif"
    font-size="22"
    font-weight="700"
    fill="#18201C"
    letter-spacing="-0.3"
  >Briefs</text>
</svg>
'''

# ── SVG: Mark only ──────────────────────────────────────────────────────────

MARK_SVG = '''\
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 56 56" width="56" height="56" role="img" aria-label="ReviewBriefs">
  <title>ReviewBriefs</title>
  <rect x="0" y="0" width="56" height="56" rx="13" fill="#4F6F52"/>
  <rect x="0" y="0" width="56" height="4" rx="2" fill="#6B9970" opacity="0.5"/>
  <text
    x="14"
    y="38"
    font-family="'Inter', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, sans-serif"
    font-size="26"
    font-weight="800"
    letter-spacing="-1"
    fill="#FFFDF8"
  >RB</text>
</svg>
'''

# ── SVG: Light (for dark backgrounds) ──────────────────────────────────────

LOGO_LIGHT_SVG = '''\
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 56" width="256" height="56" role="img" aria-label="ReviewBriefs">
  <title>ReviewBriefs</title>
  <rect x="0" y="0" width="56" height="56" rx="13" fill="#FFFDF8" opacity="0.12"/>
  <rect x="0" y="0" width="56" height="56" rx="13" fill="none" stroke="#FFFDF8" stroke-width="1.5" opacity="0.3"/>
  <text
    x="14"
    y="38"
    font-family="'Inter', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, sans-serif"
    font-size="26"
    font-weight="800"
    letter-spacing="-1"
    fill="#FFFDF8"
  >RB</text>
  <text
    x="72"
    y="37"
    font-family="'Inter', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, sans-serif"
    font-size="22"
    font-weight="400"
    fill="#FFFDF8"
    letter-spacing="-0.3"
    opacity="0.9"
  >Review</text>
  <text
    x="155"
    y="37"
    font-family="'Inter', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, sans-serif"
    font-size="22"
    font-weight="700"
    fill="#FFFDF8"
    letter-spacing="-0.3"
  >Briefs</text>
</svg>
'''

with open('assets/images/logo.svg', 'w') as f:
    f.write(LOGO_SVG)
with open('assets/images/logo-mark.svg', 'w') as f:
    f.write(MARK_SVG)
with open('assets/images/logo-light.svg', 'w') as f:
    f.write(LOGO_LIGHT_SVG)

print('SVGs written.')

# ── PNG: logo@2x (496 x 104) ───────────────────────────────────────────────

def load_font(size, bold=False):
    candidates_bold = [
        '/System/Library/Fonts/Supplemental/Arial Bold.ttf',
        '/System/Library/Fonts/Supplemental/Arial.ttf',
        '/System/Library/Fonts/Helvetica.ttc',
    ]
    candidates = [
        '/System/Library/Fonts/Supplemental/Arial.ttf',
        '/System/Library/Fonts/Helvetica.ttc',
    ]
    for p in (candidates_bold if bold else candidates):
        try:
            return ImageFont.truetype(p, size)
        except:
            pass
    return ImageFont.load_default()

SCALE = 2
W, H = 496, 104
CREAM  = (247, 243, 234)
PAPER  = (255, 253, 248)
INK    = (24,  32,  28)
MOSS   = (79,  111, 82)
MOSS_L = (107, 153, 112)

img = Image.new('RGBA', (W, H), (0, 0, 0, 0))  # transparent
draw = ImageDraw.Draw(img)

# Mark background
mark_size = H
r = 26

def rounded_rect(draw, xy, radius, fill, outline=None, width=1):
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=width)

rounded_rect(draw, [0, 0, mark_size, mark_size], r, MOSS)

# Top highlight on mark
rounded_rect(draw, [0, 0, mark_size, 8], r, MOSS_L)
draw.rectangle([0, 4, mark_size, 8], fill=MOSS_L)

# RB text in mark — tight, bold
f_rb   = load_font(52, bold=True)
f_rev  = load_font(44)
f_brf  = load_font(44, bold=True)

# Center "RB" in the mark
rb_w  = draw.textlength('RB', font=f_rb)
rb_x  = (mark_size - rb_w) / 2
draw.text((rb_x, 22), 'RB', font=f_rb, fill=PAPER)

# Wordmark
wm_x = mark_size + 28
# baseline align to mark center
base_y = 62

draw.text((wm_x, base_y - 44), 'Review', font=f_rev, fill=INK)
review_w = draw.textlength('Review', font=f_rev)
draw.text((wm_x + review_w, base_y - 44), 'Briefs', font=f_brf, fill=INK)

img.save('assets/images/logo@2x.png', 'PNG')
print('logo@2x.png saved:', img.size)

# Also save on cream bg for preview
img_preview = Image.new('RGB', (W, H), CREAM)
img_preview.paste(img, mask=img.split()[3])
img_preview.save('assets/images/logo-preview.png', 'PNG')
print('logo-preview.png saved')

# ── PNG: logo-mark@2x (104 x 104) ─────────────────────────────────────────

mark_img = Image.new('RGBA', (104, 104), (0, 0, 0, 0))
mark_draw = ImageDraw.Draw(mark_img)
rounded_rect(mark_draw, [0, 0, 104, 104], 26, MOSS)
rounded_rect(mark_draw, [0, 0, 104, 8], 4, MOSS_L)
mark_draw.rectangle([0, 4, 104, 8], fill=MOSS_L)

rb_w2 = mark_draw.textlength('RB', font=f_rb)
mark_draw.text(((104 - rb_w2) / 2, 22), 'RB', font=f_rb, fill=PAPER)
mark_img.save('assets/images/logo-mark@2x.png', 'PNG')
print('logo-mark@2x.png saved')

print('\nAll logo assets written to assets/images/')
