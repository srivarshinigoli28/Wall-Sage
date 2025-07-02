import tkinter as tk
from tkinter import colorchooser, font
from PIL import Image, ImageDraw, ImageFont, ImageTk
import ctypes
import os
import json

drawing_lines = []  # [(points, color, brush_size)]
text_items = []     # [(id, x, y, text, color, font_name, font_size)]
history_stack = []  # Stack of ('draw', data) or ('text', data)
current_line = []
current_color = "black"
brush_size = 3
eraser_mode = False
bg_image_path = "background.jpg"
font_choice = "Arial"
font_size = 20
redo_stack = []

# setting window's(display of app) height and width
screen_width = ctypes.windll.user32.GetSystemMetrics(0)
screen_height = ctypes.windll.user32.GetSystemMetrics(1)

# creating the window for the app
root = tk.Tk()
root.title("Task Scribble Pad Wallpaper")
root.geometry(f"{screen_width}x{screen_height}")
root.configure(bg="#8ba7cc")

# adding a canvas to be able to draw strokes
canvas_width = screen_width - 220
canvas_height = screen_height
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white", cursor="pencil")
canvas.pack(side="left", fill="both", expand=True)

# connecting the canvas to the window
if os.path.exists(bg_image_path):
    bg_img = Image.open(bg_image_path).resize((canvas_width, canvas_height))
else:
    bg_img = Image.new("RGB", (canvas_width, canvas_height), "white")
bg_tk = ImageTk.PhotoImage(bg_img)
canvas.create_image(0, 0, anchor="center", image=bg_tk)

# drawing on canvas: save coordinates in respective stacks
def start_draw(event):
    global current_line
    current_line = [(event.x, event.y)]

def draw(event):
    if current_line:
        x1, y1 = current_line[-1]
        x2, y2 = event.x, event.y
        color = "white" if eraser_mode else current_color
        width = brush_size * 2 if eraser_mode else brush_size
        canvas.create_line(x1, y1, x2, y2, fill=color, width=width, capstyle=tk.ROUND, smooth=True)
        current_line.append((x2, y2))

def stop_draw(event):
    global current_line
    if current_line:
        color = "white" if eraser_mode else current_color
        width = brush_size * 2 if eraser_mode else brush_size
        drawing_lines.append((list(current_line), color, width))
        history_stack.append(('draw', (list(current_line), color, width)))
        current_line = []

# binding functions to mouse events
canvas.bind("<ButtonPress-1>", start_draw)
canvas.bind("<B1-Motion>", draw)
canvas.bind("<ButtonRelease-1>", stop_draw)

root.mainloop()
