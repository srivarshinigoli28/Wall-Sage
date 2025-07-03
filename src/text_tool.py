import tkinter as tk

def setup_text_tool(canvas, root, text_items, history_stack, state):
    text_drag_data = {"item": None, "x": 0, "y": 0}

    def canvas_click(event):
        entry_popup(event.x, event.y)

    canvas.bind("<Button-3>", canvas_click)  # Right-click

    def entry_popup(x, y):
        popup = tk.Toplevel(root)
        popup.overrideredirect(True)
        popup.geometry(f"+{x + root.winfo_rootx()}+{y + root.winfo_rooty()}")

        max_lines = 5
        min_lines = 1

        frame = tk.Frame(popup)
        frame.pack()

        text_widget = tk.Text(
            frame,
            width=30,
            height=min_lines,
            font=(state["font_choice"], state["font_size"]),
            fg=state["current_color"],
            bg="#ffffff",
            wrap="word"
        )
        text_widget.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame, command=text_widget.yview)
        scrollbar.pack(side="right", fill="y")
        text_widget.config(yscrollcommand=scrollbar.set)

        def resize_text(event=None):
            lines = int(text_widget.index('end-1c').split('.')[0])
            lines = max(min_lines, min(lines, max_lines))
            text_widget.config(height=lines)
            if lines == max_lines:
                scrollbar.pack(side="right", fill="y")
            else:
                scrollbar.pack_forget()

        text_widget.bind("<KeyRelease>", resize_text)

        def save_text(event=None):
            text = text_widget.get("1.0", "end-1c").strip()
            if text:
                text_id = canvas.create_text(
                    x, y,
                    text=text,
                    font=(state["font_choice"], state["font_size"]),
                    fill=state["current_color"],
                    anchor="nw"
                )
                text_items.append((text_id, x, y, text, state["current_color"], state["font_choice"], state["font_size"]))
                history_stack.append(('text', (text_id, x, y, text, state["current_color"], state["font_choice"], state["font_size"])))
                make_draggable(text_id)

            popup.destroy()

        def on_key(event):
            if event.keysym == "Return":
                if event.state & 0x0001:  # Shift pressed
                    return None
                else:
                    save_text()
                    return "break"
            elif event.keysym == "Escape":
                popup.destroy()

        text_widget.bind("<Key>", on_key)
        text_widget.focus_set()
        resize_text()

    def make_draggable(text_id):
        def start_drag(event):
            state["dragging_text"] = True
            text_drag_data["item"] = text_id
            text_drag_data["x"] = event.x
            text_drag_data["y"] = event.y

        def drag(event):
            dx = event.x - text_drag_data["x"]
            dy = event.y - text_drag_data["y"]
            canvas.move(text_id, dx, dy)
            text_drag_data["x"] = event.x
            text_drag_data["y"] = event.y

        def stop_drag(event):
            state["dragging_text"] = False
            
        canvas.tag_bind(text_id, "<ButtonRelease-1>", stop_drag)

        canvas.tag_bind(text_id, "<Button-1>", start_drag)
        canvas.tag_bind(text_id, "<B1-Motion>", drag)
