
import tkinter as tk
import math

BG = "#050505"
WHITE = "#F3F0E8"
GREEN = "#9ACD32"
GOLD = "#C9A96E"
RED =  "#FE3939"
CYAN = "#6DD6E8"
MUTED = "#777777"

root = tk.Tk()
root.title("Circle of Numbers | Mathematical String Art")
root.geometry("1100x780")
root.minsize(780, 600)
root.configure(bg=BG)

# Header
tk.Label(
    root, text="CIRCLE OF NUMBERS",
    font=("Arial", 24, "bold"),
    fg=WHITE, bg=BG
).pack(pady=(16, 2))

tk.Label(
    root, text="HOW MULTIPLICATION CREATES MATHEMATICAL ART",
    font=("Consolas", 10),
    fg=GOLD, bg=BG
).pack(pady=(0, 12))

# Drawing area
canvas = tk.Canvas(
    root, bg=BG, highlightthickness=0
)
canvas.pack(fill="both", expand=True, padx=18, pady=5)

# Controls
controls = tk.Frame(root, bg=BG)
controls.pack(fill="x", padx=25, pady=(8, 5))

tk.Label(
    controls, text="MULTIPLIER",
    fg=WHITE, bg=BG, font=("Consolas", 10, "bold")
).grid(row=0, column=0, padx=8)

multiplier = tk.DoubleVar(value=3.0)
mult_scale = tk.Scale(
    controls, from_=2, to=10, resolution=0.1,
    orient="horizontal", variable=multiplier,
    bg=BG, fg=WHITE, troughcolor="#333333",
    highlightthickness=0, length=220,
    command=lambda _: draw()
)
mult_scale.grid(row=0, column=1, padx=8)

tk.Label(
    controls, text="POINTS",
    fg=WHITE, bg=BG, font=("Consolas", 10, "bold")
).grid(row=0, column=2, padx=8)

point_count = tk.IntVar(value=240)
point_scale = tk.Scale(
    controls, from_=80, to=360, resolution=20,
    orient="horizontal", variable=point_count,
    bg=BG, fg=WHITE, troughcolor="#333333",
    highlightthickness=0, length=180,
    command=lambda _: draw()
)
point_scale.grid(row=0, column=3, padx=8)

# Color choices
color = tk.StringVar(value=GREEN)

def choose_color(new_color):
    color.set(new_color)
    draw()

for label, shade in [
    ("RED", RED), ("GREEN", GREEN), ("BLUE", CYAN)
]:
    tk.Button(
        controls, text=label, fg=shade, bg="#151515",
        activebackground="#303030",
        activeforeground=shade,
        relief="flat", padx=10,
        command=lambda c=shade: choose_color(c)
    ).grid(row=1, column=["RED", "GREEN", "BLUE"].index(label),
           pady=12, padx=5)

# Information
info = tk.Label(
    root, text="",
    font=("Consolas", 10),
    fg=CYAN, bg=BG
)
info.pack(pady=(2, 12))


def draw():
    canvas.delete("all")

    w = canvas.winfo_width()
    h = canvas.winfo_height()

    if w < 100 or h < 100:
        return

    n = point_count.get()
    factor = multiplier.get()

    radius = min(w, h) * 0.43
    cx, cy = w / 2, h / 2

    # Circle boundary
    canvas.create_oval(
        cx-radius, cy-radius,
        cx+radius, cy+radius,
        outline="#373737", width=1
    )

    # Equally spaced points on the circle
    points = []
    for i in range(n):
        angle = 2 * math.pi * i / n - math.pi / 2
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        points.append((x, y))

    # Draw multiplication connections
    # The modulo operation wraps values around the circle.
    for i, (x1, y1) in enumerate(points):
        destination = (i * factor) % n

        # Interpolate between neighboring points for
        # smooth patterns when the multiplier is decimal.
        low = int(destination)
        fraction = destination - low
        high = (low + 1) % n

        x2 = points[low][0] * (1 - fraction) + points[high][0] * fraction
        y2 = points[low][1] * (1 - fraction) + points[high][1] * fraction

        canvas.create_line(
            x1, y1, x2, y2,
            fill=color.get(), width=0.65
        )

    # Draw the numbered points
    for x, y in points:
        canvas.create_oval(
            x-1.3, y-1.3, x+1.3, y+1.3,
            fill=WHITE, outline=""
        )

    info.config(
        text=f"POINTS: {n}     MULTIPLIER: {factor:.1f}"
        f"     CONNECTIONS: {n}"
    )


def save_art():
    filename = tk.filedialog.asksaveasfilename(
        defaultextension=".ps",
        filetypes=[("PostScript artwork", "*.ps")],
        title="Save your mathematical artwork"
    )
    if filename:
        canvas.postscript(
            file=filename, colormode="color"
        )
        info.config(text="ARTWORK SAVED: " + filename)


# Import the dialog explicitly
from tkinter import filedialog
tk.filedialog = filedialog

tk.Button(
    root, text="SAVE ARTWORK",
    command=save_art, fg=BG, bg=GOLD,
    activebackground=WHITE, relief="flat",
    font=("Consolas", 10, "bold"), padx=16, pady=7
).pack(pady=(0, 16))

canvas.bind("<Configure>", lambda event: draw())
root.after(150, draw)

root.mainloop()
