from PIL import Image, ImageDraw, ImageFont, ImageTk
import os
import ctypes
import json
from datetime import datetime
import matplotlib.font_manager as fm 

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
            # Dynamically find the full path to the system-installed font
            font_path = fm.findfont(fm.FontProperties(family=font_name), fallback_to_default=True)
            font = ImageFont.truetype(font_path, font_sz)
        except Exception as e:
            print(f"Warning: Could not load font '{font_name}': {e}")
            font = ImageFont.load_default()
    
        draw.text((x, y), text, fill=color, font=font)
    # Saving the final image
    img.save(output_path)

def set_as_wallpaper(image_path):
    # SPI_SETDESKWALLPAPER = 20
    # 3rd param is the image path
    # 4th param is update flags: 3 = update user profile + send change broadcast
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
    
def load_last_wallpaper():
    try:
        with open("last_wallpaper.json", "r") as f:
            data = json.load(f)
            path = data.get("path")
            if path and os.path.exists(path):
                return Image.open(path)
    except Exception:
        pass
    return None

def set_and_save_wallpaper(canvas, drawing_lines, text_items, state):
    os.makedirs("wallpapers", exist_ok=True)
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    output_path = os.path.join("wallpapers", f"wallpaper_{timestamp}.png")

    save_canvas_as_image(
        canvas.winfo_width(),
        canvas.winfo_height(),
        state.get("bg_img"),
        drawing_lines,
        text_items,
        output_path
    )
    set_as_wallpaper(os.path.abspath(output_path))

    with open("last_wallpaper.json", "w") as f:
        json.dump({"path": os.path.abspath(output_path)}, f)

def reset_canvas(canvas, drawing_lines, text_items, history_stack, redo_stack, state):
    drawing_lines.clear()
    text_items.clear()
    history_stack.clear()
    redo_stack.clear()

    if os.path.exists("background.jpg"):
        bg_img = Image.open("background.jpg").resize(
            (canvas.winfo_width(), canvas.winfo_height())
        )
    else:
        bg_img = Image.new("RGB", (canvas.winfo_width(), canvas.winfo_height()), "white")

    state["bg_img"] = bg_img
    bg_tk = ImageTk.PhotoImage(bg_img)
    state["bg_tk"] = bg_tk
    canvas.delete("all")
    canvas.create_image(0, 0, anchor="nw", image=bg_tk)