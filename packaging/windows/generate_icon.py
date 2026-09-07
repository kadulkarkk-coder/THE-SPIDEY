"""Generate the small WEBSTER spider ICO during CI."""
from PIL import Image, ImageDraw

sizes = (16, 32, 48, 64, 128, 256)
images = []
for size in sizes:
    image = Image.new("RGBA", (size, size), (10, 10, 10, 255))
    draw = ImageDraw.Draw(image)
    s = size
    draw.ellipse((s*0.16, s*0.16, s*0.84, s*0.84), fill=(209, 23, 23, 255))
    draw.polygon([(s*.50,s*.22),(s*.60,s*.43),(s*.82,s*.31),(s*.68,s*.53),(s*.88,s*.62),(s*.65,s*.66),(s*.72,s*.88),(s*.50,s*.72),(s*.28,s*.88),(s*.35,s*.66),(s*.12,s*.62),(s*.32,s*.53),(s*.18,s*.31),(s*.40,s*.43)], fill=(10,10,10,255))
    draw.ellipse((s*.38,s*.43,s*.47,s*.55), fill=(255,255,255,255))
    draw.ellipse((s*.53,s*.43,s*.62,s*.55), fill=(255,255,255,255))
    images.append(image)
images[0].save("packaging/windows/webster.ico", format="ICO", sizes=[(s, s) for s in sizes], append_images=images[1:])
