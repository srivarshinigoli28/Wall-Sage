from PIL import Image, ImageDraw, ImageFont
import os
import ctypes

def save_canvas_as_image(canvas_width, canvas_height, bg_img, drawing_lines, text_items, output_path):
    # Creating a blank image with white background
    img = Image.new("RGB", (canvas_width, canvas_height), "white")
    draw = ImageDraw.Draw(img)

    # Pasting the background image if present
    if bg_img:
        img.paste(bg_img)

    # Drawing all lines (strokes)
    for points, color, size in drawing_lines:
        if len(points) > 1:
            draw.line(points, fill=color, width=size)

    # Drawing all text items
    for (_, x, y, text, color, font_name, font_sz) in text_items:
        try:
            font_file_map = {
                "Arial": "arial.ttf",
                "Courier": "cour.ttf",
                "Times New Roman": "times.ttf"
            }
            font_path = font_file_map.get(font_name, "arial.ttf")
            font = ImageFont.truetype(font_path, font_sz)
        except OSError:
            font = ImageFont.load_default()
        draw.text((x, y), text, fill=color, font=font)

    # Saving the final image
    img.save(output_path)

def set_as_wallpaper(image_path):
    # SPI_SETDESKWALLPAPER = 20
    # 3rd param is the image path
    # 4th param is update flags: 3 = update user profile + send change broadcast
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)