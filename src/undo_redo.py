import tkinter as tk
def undo(canvas, drawing_lines, text_items, history_stack, redo_stack):
    if not history_stack:
        return

    action, data = history_stack.pop()
    redo_stack.append((action, data))

    if action == 'draw':
        # Remove last drawn line
        drawing_lines.pop()
        canvas.delete("all")
        
        # Redraw all remaining lines
        for points, color, width in drawing_lines:
            for i in range(1, len(points)):
                x1, y1 = points[i-1]
                x2, y2 = points[i]
                canvas.create_line(x1, y1, x2, y2, fill=color, width=width, capstyle=tk.ROUND, smooth=True)

        # Redraw all text items
        for item in text_items:
            text_id, x, y, text, color, font_name, font_size = item
            canvas.create_text(x, y, text=text, fill=color, font=(font_name, font_size), anchor="nw")

    elif action == 'text':
        text_id, *_ = data
        canvas.delete(text_id)
        # Remove from text_items
        text_items[:] = [item for item in text_items if item[0] != text_id]

def redo(canvas, drawing_lines, text_items, history_stack, redo_stack):
    if not redo_stack:
        return

    action, data = redo_stack.pop()
    history_stack.append((action, data))

    if action == 'draw':
        points, color, width = data
        drawing_lines.append((points, color, width))
        for i in range(1, len(points)):
            x1, y1 = points[i-1]
            x2, y2 = points[i]
            canvas.create_line(x1, y1, x2, y2, fill=color, width=width, capstyle=tk.ROUND, smooth=True)

    elif action == 'text':
        text_id, x, y, text, color, font_name, font_size = data
        new_id = canvas.create_text(x, y, text=text, fill=color, font=(font_name, font_size), anchor="nw")
        text_items.append((new_id, x, y, text, color, font_name, font_size))
