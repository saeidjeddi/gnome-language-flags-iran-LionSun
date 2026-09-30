import io, sys
from fontTools.ttLib import TTFont
from PIL import Image

SRC = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
flag_png = sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 else "NotoColorEmojiLionSun.ttf"

font = TTFont(SRC)

glyph = None
for lk in font["GSUB"].table.LookupList.Lookup:
    for st in lk.SubTable:
        st = getattr(st, "ExtSubTable", st)
        for l in getattr(st, "ligatures", {}).get("u1F1EE", []):
            if l.Component == ["u1F1F7"]:
                glyph = l.LigGlyph
if glyph is None:
    sys.exit("glyph پرچم ایران پیدا نشد")

strike = font["CBDT"].strikeData[0]
g = strike[glyph]
W, H = g.metrics.width, g.metrics.height         

orig = Image.open(io.BytesIO(g.imageData)).convert("RGBA")
ox0, oy0, ox1, oy1 = orig.split()[-1].getbbox()
flag = Image.open(flag_png).convert("RGBA")
flag = flag.crop(flag.split()[-1].getbbox())
bw, bh = ox1 - ox0, oy1 - oy0
scale = min(bw / flag.width, bh / flag.height)
nw, nh = round(flag.width * scale), round(flag.height * scale)
flag = flag.resize((nw, nh), Image.LANCZOS)

canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
canvas.paste(flag, (ox0 + (bw - nw) // 2, oy0 + (bh - nh) // 2), flag)
buf = io.BytesIO(); canvas.save(buf, "PNG", optimize=True)
g.imageData = buf.getvalue()

for rec in font["name"].names:
    if rec.nameID in (1, 4, 16):
        rec.string = "Noto Color Emoji LionSun"
    elif rec.nameID == 6:
        rec.string = "NotoColorEmojiLionSun"
font.save(out)
print("OK ->", out, "| glyph:", glyph)
