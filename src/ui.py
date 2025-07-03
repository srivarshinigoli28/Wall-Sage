
import tkinter as tk
from tkinter import colorchooser
from eraser import toggle_eraser

def setup_toolbar(root, state):
    # toolbar
    toolbar = tk.Frame(root, bg="#d0e0f0", width=200)
    toolbar.pack(side="right", fill="y")

    # toolbar - brush size + color
    def pick_color():
        color = colorchooser.askcolor(title="Pick a color")[1]
        if color:
            state["current_color"] = color

    tk.Button(toolbar, text="Pick Color", command=pick_color).pack(pady=10)

    tk.Label(toolbar, text="Brush Size").pack(pady=(20, 0))

    brush_slider = tk.Scale(
        toolbar,
        from_=1,
        to=20,
        orient="horizontal",
        length=150,
        showvalue=0,          
        tickinterval=0,       
        sliderlength=20,      
        troughcolor="#e0e0e0",
        command=lambda val: state.update({"brush_size": int(val)})
    )
    brush_slider.set(state["brush_size"])
    brush_slider.pack(pady=5)

    eraser_btn = tk.Button(toolbar, text="Eraser")

    def eraser_toggle():
        toggle_eraser(state)
        if state["eraser_mode"]:
            eraser_btn.config(bg="#737070", fg="white")  # light red background
        else:
            eraser_btn.config(bg="SystemButtonFace", fg="black")
    eraser_btn.config(command=eraser_toggle)

    # Pack it into the toolbar
    eraser_btn.pack(pady=10)
