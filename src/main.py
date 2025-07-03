import tkinter as tk
from tkinter import colorchooser, font
from PIL import Image, ImageDraw, ImageFont, ImageTk
import ctypes
import os
import json
from strokes_tool import setup_stroke_bindings
from ui import setup_toolbar
from text_tool import setup_text_tool
from wallpaper_utils import save_canvas_as_image

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
canvas.create_image(0, 0, anchor="center", image=bg_tk)

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
state["bg_img"] = bg_img
# Setup stroke events
setup_stroke_bindings(canvas, drawing_lines, history_stack, state)
setup_toolbar(root, canvas, drawing_lines, text_items, history_stack, redo_stack, state)
setup_text_tool(canvas, root, text_items, history_stack, state)
save_canvas_as_image(
    canvas_width,
    canvas_height,
    bg_img,
    drawing_lines,
    text_items,
    "output_wallpaper.png"
)

root.mainloop()