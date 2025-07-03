import tkinter as tk
from tkinter import colorchooser
from tkinter import ttk, font
from erase_tool import toggle_eraser

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

    # Font style selector
    tk.Label(toolbar, text="Font Style").pack(pady=(15, 0))

    available_fonts = list(font.families())
    available_fonts.sort()

    font_dropdown = ttk.Combobox(
        toolbar,
        values=available_fonts,
        state="readonly",
        width=18
    )
    font_dropdown.set(state["font_choice"])  # default selection
    font_dropdown.pack(pady=5)

    def on_font_change(event):
        state["font_choice"] = font_dropdown.get()

    font_dropdown.bind("<<ComboboxSelected>>", on_font_change)

    # font slider
    tk.Label(toolbar, text="Font Size").pack(pady=(15, 0))

    font_size_slider = tk.Scale(
        toolbar,
        from_=8,
        to=72,
        orient="horizontal",
        length=150,
        showvalue=True,
        command=lambda val: state.update({"font_size": int(val)})
    )
    font_size_slider.set(state["font_size"])
    font_size_slider.pack(pady=5)

    # eraser button
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
