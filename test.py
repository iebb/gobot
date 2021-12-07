from PIL import ImageDraw, Image, ImageFont

img = Image.new(
    'RGBA', (300, 300),
    color=(255, 255, 255, 255)
)
monospace_font = ImageFont.load('fonts/lcdsolid.pil')
d = ImageDraw.Draw(img)
d.fontmode = "P"
d.text(
    (1, 1),
    '0123456789:ABCDEFG',
    font=monospace_font,
    fill="black",
    # spacing=44,
)
img.save('pil_text_font.png')