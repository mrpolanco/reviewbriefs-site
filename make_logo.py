"""
Generates ReviewBriefs logo and OG image using Gemini image generation.

Outputs:
  assets/images/logo-mark-raw.png     - Gemini-generated mark (raw)
  assets/images/logo-mark.png         - mark composited (transparent bg)
  assets/images/logo.svg              - horizontal wordmark SVG (uses PNG mark)
  assets/images/logo-light.svg        - light variant for dark backgrounds
  assets/images/logo@2x.png           - 496x104 full logo raster
  assets/images/og-image.png          - 1200x630 OG card
"""

import json, os, io, time
from pathlib import Path
from google import genai
from google.genai import types
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

# ── Auth ────────────────────────────────────────────────────────────────────
settings = json.load(open(os.path.expanduser("~/.claude/settings.json")))
API_KEY = settings["mcpServers"]["gemini"]["env"]["GEMINI_API_KEY"]
client = genai.Client(api_key=API_KEY)

OUT = Path("assets/images")
OUT.mkdir(parents=True, exist_ok=True)

# ── Brand colors ─────────────────────────────────────────────────────────────
INK       = (24,  32,  28)
INK_SOFT  = (61,  73,  67)
MUTED     = (111, 122, 115)
CREAM     = (247, 243, 234)
PAPER     = (255, 253, 248)
STONE     = (231, 224, 211)
MOSS      = (79,  111, 82)
MOSS_DARK = (48,  71,  52)
SAGE      = (168, 184, 160)
CLAY      = (184, 107, 75)
GOLD      = (198, 161, 91)


def gemini_image(prompt: str, path: Path, attempts=3) -> Image.Image | None:
    if path.exists():
        print(f"  skip (exists): {path.name}")
        return Image.open(path)
    for attempt in range(attempts):
        try:
            response = client.models.generate_content(
                model="gemini-3.1-flash-image-preview",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE", "TEXT"]
                ),
            )
            for part in response.candidates[0].content.parts:
                if hasattr(part, "inline_data") and part.inline_data:
                    img = Image.open(io.BytesIO(part.inline_data.data))
                    img.save(path, "PNG")
                    print(f"  saved: {path.name}  {img.size}")
                    return img
            print(f"  no image in response (attempt {attempt+1})")
        except Exception as e:
            print(f"  attempt {attempt+1} error: {e}")
            if attempt < attempts - 1:
                time.sleep(12)
    return None


def load_font(size, bold=False):
    bold_paths = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    reg_paths = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for p in (bold_paths if bold else reg_paths):
        try:
            return ImageFont.truetype(p, size)
        except:
            pass
    return ImageFont.load_default()


# ══════════════════════════════════════════════════════════════════════════════
# 1. LOGO MARK  - Gemini generates a refined monogram/seal
# ══════════════════════════════════════════════════════════════════════════════

MARK_PROMPT = (
    "A modern, minimal logo mark for a B2B SaaS brand called ReviewBriefs - a guest review intelligence tool for hotels and hospitality agencies. "
    "The mark should feel like a clean, contemporary app icon: a simple document or brief shape combined with a subtle review or insight signal. "
    "Design direction: a stylised document icon - clean rectangular shape with a folded top-right corner, "
    "with two or three short horizontal lines suggesting text/content inside. "
    "Optionally incorporate a very subtle upward trend line, checkmark, or small star to suggest insight or quality. "
    "Color: deep forest green (#4F6F52) icon on a warm cream (#F7F3EA) or white background. "
    "Style: geometric, modern, flat - like a well-designed iOS or SaaS app icon. "
    "No serif fonts, no circular badges, no old-fashioned monogram rings. No gradients, no glow effects. "
    "Clean vector aesthetic. Square or slightly rounded-square format. No text, no letters."
)

print("[1/3] Generating logo mark via Gemini...")
mark_raw = gemini_image(MARK_PROMPT, OUT / "logo-mark-raw.png")

if mark_raw:
    # Crop to square center, resize to 200x200 for use in composites
    w, h = mark_raw.size
    side = min(w, h)
    left = (w - side) // 2
    top  = (h - side) // 2
    mark = mark_raw.crop((left, top, left + side, top + side))
    mark = mark.resize((200, 200), Image.LANCZOS)
    mark.save(OUT / "logo-mark.png", "PNG")
    print(f"  logo-mark.png saved (200x200)")
else:
    print("  mark generation failed - using fallback")
    mark = None

time.sleep(6)


# ══════════════════════════════════════════════════════════════════════════════
# 2. OG IMAGE BACKGROUND - Gemini generates editorial hospitality scene
# ══════════════════════════════════════════════════════════════════════════════

OG_BG_PROMPT = (
    "Wide editorial photograph-style image for a hospitality intelligence brand. "
    "A beautifully composed boutique hotel scene: warm interior light, a writing desk or "
    "reception area with a leather-bound notebook open, a pen resting on the page, "
    "architectural details - stone walls, arched doorways, or courtyard garden visible. "
    "Natural light, warm cream and sage green tones, earthy textures. "
    "Atmosphere: calm, professional, premium, tasteful. "
    "Think a boutique hotel in Antigua Guatemala, Tuscany, or Lisbon. "
    "The left third of the image should be relatively open - softer tones, less busy - "
    "to allow text overlay. "
    "No text, no people, no phones. No generic stock photo feel. "
    "Horizontal 16:9 format. Warm, editorial, grounded."
)

print("[2/3] Generating OG image background via Gemini...")
og_bg_raw = gemini_image(OG_BG_PROMPT, OUT / "og-bg-raw.png")

time.sleep(6)


# ══════════════════════════════════════════════════════════════════════════════
# 3. COMPOSITE: OG IMAGE  (1200 × 630)
# ══════════════════════════════════════════════════════════════════════════════

print("[3/3] Compositing OG image...")

W, H = 1200, 630
og = Image.new("RGB", (W, H), CREAM)

if og_bg_raw:
    # Resize background to fill canvas
    bg = og_bg_raw.convert("RGB")
    bg_w, bg_h = bg.size
    scale = max(W / bg_w, H / bg_h)
    bg = bg.resize((int(bg_w * scale), int(bg_h * scale)), Image.LANCZOS)
    # Center crop
    bw, bh = bg.size
    left = (bw - W) // 2
    top  = (bh - H) // 2
    bg = bg.crop((left, top, left + W, top + H))
    # Slightly desaturate and lighten for text legibility
    bg = ImageEnhance.Color(bg).enhance(0.8)
    bg = ImageEnhance.Brightness(bg).enhance(1.08)
    og.paste(bg)

draw = ImageDraw.Draw(og, "RGBA")

# Solid cream panel on left, feathering into photo on the right
# Solid from 0-460, then gradient fade to transparent at 660
for x in range(W):
    if x < 460:
        alpha = 230
    elif x < 680:
        t = (x - 460) / 220
        alpha = int(230 * (1 - t) ** 1.4)
    else:
        alpha = 0
    if alpha > 0:
        draw.line([(x, 0), (x, H)], fill=(*CREAM, alpha))

# Left accent bar
draw.rectangle([0, 0, 5, H], fill=MOSS)

# Gold top-right accent
draw.rectangle([W - 220, 0, W, 4], fill=GOLD)

# Bottom strip
draw.rectangle([0, H - 52, W, H], fill=(*MOSS_DARK, 230))

# ── Logo mark (if generated) ──────────────────────────────────────────────
if mark:
    # Place mark at top-left
    mark_og = mark.resize((72, 72), Image.LANCZOS).convert("RGBA")
    # Rounded mask
    mask = Image.new("L", (72, 72), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, 72, 72], radius=16, fill=255)
    og.paste(mark_og, (64, 58), mask)
    brand_x = 148
else:
    # Fallback: moss square with RB
    draw.rounded_rectangle([64, 58, 128, 122], radius=16, fill=MOSS)
    draw.text((78, 70), "RB", font=load_font(36, bold=True), fill=PAPER)
    brand_x = 148

# Brand name
draw.text((brand_x, 70), "Review", font=load_font(22), fill=INK)
rev_w = draw.textlength("Review", font=load_font(22))
draw.text((brand_x + rev_w, 70), "Briefs", font=load_font(22, bold=True), fill=INK)

# ── Headline ──────────────────────────────────────────────────────────────
hy = 178
draw.text((72, hy),      "Turn guest reviews into",   font=load_font(44, bold=True), fill=INK)
draw.text((72, hy + 54), "client-ready insights.",    font=load_font(44, bold=True), fill=MOSS)

# Sub
draw.text((72, hy + 118), "Praise themes · reputation risks",        font=load_font(18), fill=INK_SOFT)
draw.text((72, hy + 142), "marketing opportunities · action lists",  font=load_font(18), fill=INK_SOFT)

# Tags
ty = hy + 200
tags = [("For hospitality agencies", False), ("For boutique hotels", False), ("Private beta", True)]
tx = 72
f_tag = load_font(13)
for label, accent in tags:
    tw = draw.textlength(label, font=f_tag)
    bg_col = (*MOSS, 220) if accent else (*STONE, 210)
    fg_col = PAPER if accent else INK_SOFT
    draw.rounded_rectangle([tx - 10, ty - 5, tx + tw + 10, ty + 19], radius=12, fill=bg_col)
    draw.text((tx, ty), label, font=f_tag, fill=fg_col)
    tx += tw + 24

# Bottom strip text
draw.text((72, H - 34), "reviewbriefs.com", font=load_font(14), fill=(198, 230, 200))
draw.text((W - 310, H - 34), "Guest review intelligence", font=load_font(14), fill=(160, 195, 163))

og.save(OUT / "og-image.png", "PNG", optimize=True)
print("  og-image.png saved (1200x630)")


# ══════════════════════════════════════════════════════════════════════════════
# 4. FULL LOGO RASTER  logo@2x.png  (496 × 104)
# ══════════════════════════════════════════════════════════════════════════════

LW, LH = 496, 104
logo_img = Image.new("RGBA", (LW, LH), (0, 0, 0, 0))
logo_draw = ImageDraw.Draw(logo_img)

if mark:
    mark_sm = mark.resize((LH, LH), Image.LANCZOS).convert("RGBA")
    mask_sm = Image.new("L", (LH, LH), 0)
    ImageDraw.Draw(mask_sm).rounded_rectangle([0, 0, LH, LH], radius=24, fill=255)
    logo_img.paste(mark_sm, (0, 0), mask_sm)
    wm_x = LH + 20
else:
    logo_draw.rounded_rectangle([0, 0, LH, LH], radius=24, fill=MOSS)
    logo_draw.text((18, 20), "RB", font=load_font(52, bold=True), fill=PAPER)
    wm_x = LH + 20

f_rev = load_font(44)
f_brf = load_font(44, bold=True)
logo_draw.text((wm_x, 30), "Review", font=f_rev, fill=INK)
rev_w2 = logo_draw.textlength("Review", font=f_rev)
logo_draw.text((wm_x + rev_w2, 30), "Briefs", font=f_brf, fill=INK)

# Cream bg preview
preview = Image.new("RGB", (LW, LH), CREAM)
preview.paste(logo_img, mask=logo_img.split()[3])
preview.save(OUT / "logo-preview.png", "PNG")

logo_img.save(OUT / "logo@2x.png", "PNG")
print("  logo@2x.png saved")

# ══════════════════════════════════════════════════════════════════════════════
# 5. SVGs with inline document icon paths (no external PNG dependency)
# ══════════════════════════════════════════════════════════════════════════════
#
# Document icon (48×48, cream bg rounded-square, moss icon):
#   - Rounded square container
#   - Document body: rect with clipped top-right fold
#   - Fold triangle
#   - 3 content lines
#   - Small upward trend arrow bottom-right

# Icon paths designed for a 48×48 viewBox, icon centered ~10-38 x / 6-42 y
ICON_PATHS = """
  <!-- Mark container -->
  <rect x="0" y="0" width="48" height="48" rx="11" fill="#F7F3EA"/>

  <!-- Document body (clip fold at top-right) -->
  <path d="M13 8 L29 8 L37 16 L37 42 L13 42 Z" fill="none" stroke="#4F6F52" stroke-width="1.8" stroke-linejoin="round"/>

  <!-- Fold crease -->
  <path d="M29 8 L29 16 L37 16" fill="none" stroke="#4F6F52" stroke-width="1.8" stroke-linejoin="round"/>

  <!-- Content lines -->
  <line x1="17" y1="22" x2="33" y2="22" stroke="#4F6F52" stroke-width="1.6" stroke-linecap="round"/>
  <line x1="17" y1="27" x2="33" y2="27" stroke="#4F6F52" stroke-width="1.6" stroke-linecap="round"/>

  <!-- Trend arrow (upward-right) -->
  <polyline points="17,36 22,31 26,33 33,25" fill="none" stroke="#4F6F52" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
  <polyline points="29,24 33,25 32,29" fill="none" stroke="#4F6F52" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
"""

# Light variant icon (cream bg with subtle opacity, cream text)
ICON_PATHS_LIGHT = """
  <rect x="0" y="0" width="48" height="48" rx="11" fill="rgba(255,253,248,0.15)"/>
  <rect x="0" y="0" width="48" height="48" rx="11" fill="none" stroke="rgba(255,253,248,0.35)" stroke-width="1"/>
  <path d="M13 8 L29 8 L37 16 L37 42 L13 42 Z" fill="none" stroke="#FFFDF8" stroke-width="1.8" stroke-linejoin="round"/>
  <path d="M29 8 L29 16 L37 16" fill="none" stroke="#FFFDF8" stroke-width="1.8" stroke-linejoin="round"/>
  <line x1="17" y1="22" x2="33" y2="22" stroke="#FFFDF8" stroke-width="1.6" stroke-linecap="round"/>
  <line x1="17" y1="27" x2="33" y2="27" stroke="#FFFDF8" stroke-width="1.6" stroke-linecap="round"/>
  <polyline points="17,36 22,31 26,33 33,25" fill="none" stroke="#FFFDF8" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
  <polyline points="29,24 33,25 32,29" fill="none" stroke="#FFFDF8" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
"""

FONT = "'Inter',ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,sans-serif"

LOGO_SVG = f"""\
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 48" width="220" height="48" role="img" aria-label="ReviewBriefs">
  <title>ReviewBriefs</title>
  {ICON_PATHS}
  <text x="60" y="33" font-family={FONT!r} font-size="20" font-weight="400" fill="#18201C" letter-spacing="-0.3">Review</text>
  <text x="133" y="33" font-family={FONT!r} font-size="20" font-weight="700" fill="#18201C" letter-spacing="-0.3">Briefs</text>
</svg>
"""

LOGO_LIGHT_SVG = f"""\
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 48" width="220" height="48" role="img" aria-label="ReviewBriefs">
  <title>ReviewBriefs</title>
  {ICON_PATHS_LIGHT}
  <text x="60" y="33" font-family={FONT!r} font-size="20" font-weight="400" fill="#FFFDF8" letter-spacing="-0.3" opacity="0.88">Review</text>
  <text x="133" y="33" font-family={FONT!r} font-size="20" font-weight="700" fill="#FFFDF8" letter-spacing="-0.3">Briefs</text>
</svg>
"""

MARK_SVG = f"""\
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48" role="img" aria-label="ReviewBriefs">
  <title>ReviewBriefs</title>
  {ICON_PATHS}
</svg>
"""

with open(OUT / "logo.svg", "w") as f:
    f.write(LOGO_SVG)
with open(OUT / "logo-light.svg", "w") as f:
    f.write(LOGO_LIGHT_SVG)
with open(OUT / "logo-mark.svg", "w") as f:
    f.write(MARK_SVG)

print("  SVGs written (inline paths, no external dependencies)")
print("\nAll done.")
