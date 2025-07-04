import os
import shutil
import subprocess
import tkinter as tk
from tkinter import colorchooser, font
from PIL import Image, ImageDraw, ImageFont, ImageTk
import ctypes
import json
from strokes_tool import setup_stroke_bindings
from ui import setup_toolbar
from text_tool import setup_text_tool
from wallpaper_utils import save_canvas_as_image, load_last_wallpaper

def setup_context_menu():
    install_path = r"C:\Program Files\WallSage"
    exe_path = os.path.join(install_path, "WallSage.exe")

    if os.path.exists(exe_path):
        return
    
    # Step 1: Copy EXE to Program Files (if not already there)
    if not os.path.exists(install_path):
        os.makedirs(install_path)
    
    # current_exe = os.path.abspath("main.exe") 
    import sys
    current_exe = sys.executable

    if not os.path.exists(exe_path):
        try:
            shutil.copy2(current_exe, exe_path)
        except Exception as e:
            print(f"Failed to copy exe: {e}")
            return

    # Step 2: Create .reg content
    reg_content = rf'''Windows Registry Editor Version 5.00

[HKEY_CLASSES_ROOT\Directory\Background\shell\WallSage]
@="Open WallSage Wallpaper Editor"
"Icon"="\\"{exe_path}\\""

[HKEY_CLASSES_ROOT\Directory\Background\shell\WallSage\command]
@="\\"{exe_path}\\""
'''

    # Step 3: Save and import .reg file
    reg_path = os.path.join(os.getenv("TEMP"), "wall_sage_register.reg")
    with open(reg_path, "w") as f:
        f.write(reg_content)

    try:
        subprocess.run(["reg", "import", reg_path], check=True)
        print("✅ Right-click menu added!")
    except subprocess.CalledProcessError as e:
        print("⚠️ Could not update registry. Try running as administrator.")

# Call this ONCE at the start of your main.py (only on first run or every time)


def launch_gui():


    # drawing_lines = []  # [(points, color, brush_size)]
    text_items = []     # [(id, x, y, text, color, font_name, font_size)]
    # history_stack = []  # Stack of ('draw', data) or ('text', data)
    current_line = []
    # current_color = "black"
    # brush_size = 3
    # eraser_mode = False
    bg_image_path = "background.jpg"
    # font_choice = "Arial"
    # font_size = 20
    redo_stack = []

    # Shared state
    drawing_lines = []
    history_stack = []
    state = {
        "current_color": "black",
        "brush_size": 3,
        "eraser_mode": False,
        "font_choice" : "Arial",
        "font_size" : 20,
        "dragging_text": False
    }

    # retreiving height and width as the screen size
    screen_width = ctypes.windll.user32.GetSystemMetrics(0)
    screen_height = ctypes.windll.user32.GetSystemMetrics(1)

    # creating the window
    root = tk.Tk()
    root.title("Task Scribble Pad Wallpaper")
    root.geometry(f"{screen_width}x{screen_height}")
    root.configure(bg="#8ba7cc")

    # adding a canvas to be able to draw strokes
    canvas_width = screen_width - 220
    canvas_height = screen_height
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white", cursor="pencil")
    canvas.pack(side="left", fill="both", expand=True)

    if os.path.exists(bg_image_path):
        bg_img = Image.open(bg_image_path).resize((canvas_width, canvas_height))
    else:
        bg_img = Image.new("RGB", (canvas_width, canvas_height), "white")
    bg_tk = ImageTk.PhotoImage(bg_img)

    # Load last wallpaper if available
    loaded_bg = load_last_wallpaper()
    if loaded_bg:
        state["bg_img"] = loaded_bg.resize((canvas_width, canvas_height))
    else:
        # fallback background
        if os.path.exists(bg_image_path):
            state["bg_img"] = Image.open(bg_image_path).resize((canvas_width, canvas_height))
        else:
            state["bg_img"] = Image.new("RGB", (canvas_width, canvas_height), "white")

    bg_tk = ImageTk.PhotoImage(state["bg_img"])
    canvas.create_image(0, 0, anchor="nw", image=bg_tk)
    state["bg_tk"] = bg_tk  # Prevent garbage collection


    # Setup stroke events
    setup_stroke_bindings(canvas, drawing_lines, history_stack, state)
    setup_toolbar(root, canvas, drawing_lines, text_items, history_stack, redo_stack, state)
    setup_text_tool(canvas, root, text_items, history_stack, state)

    # import threading
    # import time
    # from plyer import notification

    # def show_reminder():
    #     while True:
    #         # displayin
    #         time.sleep(3600)

    #         notification.notify(
    #             title="Wall Sage",
    #             message="You might want to check your wallpaper. Get your tasks done!",
    #             timeout=10  # seconds the notification stays visible
    #         )

    # # Start the notification thread in background
    # reminder_thread = threading.Thread(target=show_reminder, daemon=True)
    # reminder_thread.start()

    root.mainloop()

if __name__ == "__main__":
    setup_context_menu()
    launch_gui()