from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

INPUT_FOLDER = "input"        # папка с исходными скринами планшетов
OUTPUT_FOLDER = "output"      # куда сохраняем готовые скриншоты
BLUR_LEVEL = 40               # сила blur под текст
TABLET_TITLES = {
  "1.png": "Stay Focused",
  "2.png": "Focus Timer",
  "3.png": "Track Activity",
  "4.png": "Daily Stats",
  "5.png": "Smart Insights",
  "7.png": "Minimalism",
}

os.makedirs(OUTPUT_FOLDER, exist_ok=True)
font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 110)

def top_gradient(img):
    width, height = img.size
    overlay = Image.new("RGBA", img.size, (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    h = int(height * 0.60)
    strength = 160
    for y in range(h):
        alpha = int(strength * (1 - y/h))
        draw.line([(0,y),(width,y)], fill=(0,0,0,alpha))
    return Image.alpha_composite(img, overlay)

def blur_under_text(img, text):
    width, height = img.size
    draw = ImageDraw.Draw(img)
    bbox = draw.textbbox((0,0), text, font=font)
    text_w = bbox[2]-bbox[0]
    text_h = bbox[3]-bbox[1]

    padding_y = 150
    y0 = max(0, int(height * 0.08) - padding_y)
    y1 = min(height, int(height * 0.08) + text_h + padding_y)
    area = (0, y0, width, y1)
    region = img.crop(area)

    blur_radius = 2 + BLUR_LEVEL * 2
    blurred = region.filter(ImageFilter.GaussianBlur(blur_radius))

    mask = Image.new("L", region.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    w,h = region.size
    for i in range(h):
        alpha = int(255 * ((h-i)/h) * (BLUR_LEVEL / 10))
        mask_draw.line([(0,i),(w,i)], fill=alpha)
    mask = mask.filter(ImageFilter.GaussianBlur(10))

    region = Image.composite(blurred, region, mask)
    img.paste(region, area)
    return img, int((width - text_w)/2), int(height * 0.08)

def generate_tablet_screenshots():
    for file, text in TABLET_TITLES.items():
        path = os.path.join(INPUT_FOLDER, file)
        if not os.path.exists(path):
            print(f"⚠ {file} не найден, пропускаем")
            continue
        img = Image.open(path).convert("RGBA")
        img = top_gradient(img)
        img, x, y = blur_under_text(img, text)

        draw = ImageDraw.Draw(img)
        draw.text((x,y), text, font=font, fill=(255,255,255))

        # Генерируем для 7" и 10" планшетов
        for device, size in {"tablet_7": (1200,1920), "tablet_10": (1600,2560)}.items():
            canvas = Image.new("RGBA", size, (255,255,255,255))
            img_copy = img.copy()
            img_copy.thumbnail(size, Image.Resampling.LANCZOS)
            offset = ((size[0]-img_copy.width)//2, (size[1]-img_copy.height)//2)
            canvas.paste(img_copy, offset)
            out_folder = os.path.join(OUTPUT_FOLDER, device)
            os.makedirs(out_folder, exist_ok=True)
            canvas.save(os.path.join(out_folder, file))
            print(f"✔ {device} {file} generated")

    print("✅ Все планшетные скриншоты готовы")

if __name__ == "__main__":
    generate_tablet_screenshots()
