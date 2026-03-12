import os
from PIL import Image

# настройки
CANVAS_W = 1920
CANVAS_H = 1080

PHONE_MAX_H = 900
PHONE_MAX_W = 500

screens = sorted(
    [f for f in os.listdir() if f.endswith(".png")],
    key=lambda x: int(x.split(".")[0])
)

PER_PAGE = 3


def resize_keep_ratio(img):

    w, h = img.size
    ratio = min(PHONE_MAX_W / w, PHONE_MAX_H / h)

    new_w = int(w * ratio)
    new_h = int(h * ratio)

    return img.resize((new_w, new_h), Image.LANCZOS)


def gradient_bg():

    bg = Image.new("RGB", (CANVAS_W, CANVAS_H))

    for y in range(CANVAS_H):
        c = int(40 + (y / CANVAS_H) * 60)
        for x in range(CANVAS_W):
            bg.putpixel((x, y), (c, c, c+20))

    return bg


pages = [screens[i:i+PER_PAGE] for i in range(0, len(screens), PER_PAGE)]


for p, page in enumerate(pages, 1):

    canvas = gradient_bg()

    count = len(page)

    if count == 3:
        positions = [320, 960, 1600]
    elif count == 2:
        positions = [640, 1280]
    else:
        positions = [960]

    for i, file in enumerate(page):

        img = Image.open(file)
        img = resize_keep_ratio(img)

        x = positions[i] - img.width // 2
        y = (CANVAS_H - img.height) // 2

        canvas.paste(img, (x, y))

    canvas.save(f"portfolio_{p}.jpg", quality=95)

print("done")
