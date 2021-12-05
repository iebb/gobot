from PIL import Image, ImageDraw


def add_corners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im


def center_text(draw: ImageDraw, left, right, y, text, font, **kwargs):
    if not text:
        text = ""
    box = draw.textsize(
        text,
        font=font
    )
    draw.text(
        (left + ((right - left) - box[0]) / 2, y),
        text,
        font=font,
        **kwargs,
    )
