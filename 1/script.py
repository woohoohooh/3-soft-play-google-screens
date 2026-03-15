from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"

BLUR_LEVEL = 40   # 1–10 сила blur

titles = {
"1.png": "Build Career", # screen: Onboarding
"2.png": "Pro Resume", # screen: ResumePreview
"3.png": "CV Score", # screen: Analysis
"4.png": "Job Match", # screen: JobFit
"5.png": "Easy Editor", # screen: ResumeBuilder
"6.png": "Dark Mode" # screen: Profile
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

    # зона blur по всей ширине
    padding_y = 150
    y0 = max(0, int(height * 0.08) - padding_y)
    y1 = min(height, int(height * 0.08) + text_h + padding_y)
    area = (0, y0, width, y1)
    region = img.crop(area)

    # сильный blur
    blur_radius = 2 + BLUR_LEVEL * 2
    blurred = region.filter(ImageFilter.GaussianBlur(blur_radius))

    # маска с плавным увеличением сверху вниз
    mask = Image.new("L", region.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    w, h = region.size
    for i in range(h):
        # alpha = 0 внизу, alpha = 255 вверху
        alpha = int(255 * ((h - i) / h) * (BLUR_LEVEL / 10))
        mask_draw.line([(0,i),(w,i)], fill=alpha)

    # небольшая лёгкая фильтрация для сглаживания перехода
    mask = mask.filter(ImageFilter.GaussianBlur(10))

    # накладываем blur
    region = Image.composite(blurred, region, mask)
    img.paste(region, area)
    return img, int((width - text_w)/2), int(height * 0.08)


for file, text in titles.items():
    path = os.path.join(INPUT_FOLDER, file)
    img = Image.open(path).convert("RGBA")

    img = top_gradient(img)
    img, x, y = blur_under_text(img, text)

    draw = ImageDraw.Draw(img)
    draw.text((x,y), text, font=font, fill=(255,255,255))

    output_path = os.path.join(OUTPUT_FOLDER, file)
    img.save(output_path)

print("Screenshots generated.")
