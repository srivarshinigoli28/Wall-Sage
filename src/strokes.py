import tkinter as tk

def setup_stroke_bindings(canvas, drawing_lines, history_stack, state):
    current_line = []
    # drawing on canvas: save coordinates in respective stacks

    def start_draw(event):
        nonlocal current_line
        current_line = [(event.x, event.y)]

    def draw(event):
        if current_line:
            x1, y1 = current_line[-1]
            x2, y2 = event.x, event.y
            color = "white" if state["eraser_mode"] else state["current_color"]
            width = state["brush_size"] * 2 if state["eraser_mode"] else state["brush_size"]
            canvas.create_line(x1, y1, x2, y2, fill=color, width=width, capstyle=tk.ROUND, smooth=True)
            current_line.append((x2, y2))

    def stop_draw(event):
        nonlocal current_line
        if current_line:
            color = "white" if state["eraser_mode"] else state["current_color"]
            width = state["brush_size"] * 2 if state["eraser_mode"] else state["brush_size"]
            drawing_lines.append((list(current_line), color, width))
            history_stack.append(('draw', (list(current_line), color, width)))
            current_line = []

    # binding functions to mouse events
    canvas.bind("<ButtonPress-1>", start_draw)
    canvas.bind("<B1-Motion>", draw)
    canvas.bind("<ButtonRelease-1>", stop_draw)