
import tkinter as tk
from tkinter import filedialog
import math

BG = "#050505"
WHITE="#FFFFFF"
GREEN= "#9ACD32"
GOLD = "#C9A96E"
RED = "#FE3939"
CYAN = "#6DD6E8"

root = tk.Tk()
root.title("Circle of Numbers | Live Mathematical Art")
root.geometry("1100x800")
root.minsize(780, 650)
root.configure(bg=BG)

# ---------- HEADER ----------
tk.Label(
    root, text="CIRCLE OF NUMBERS",
    font=("Arial", 24, "bold"),
    fg=WHITE, bg=BG
).pack(pady=(14, 2))

tk.Label(
    root, text="WATCH MATHEMATICS TURN INTO ART",
    font=("Consolas", 10),
    fg=GOLD, bg=BG
).pack(pady=(0, 8))

# ---------- CANVAS ----------
canvas = tk.Canvas(root, bg=BG, highlightthickness=0)
canvas.pack(fill="both", expand=True, padx=20, pady=6)

# ---------- CONTROLS ----------
controls = tk.Frame(root, bg=BG)
controls.pack(fill="x", padx=24, pady=4)

multiplier = tk.DoubleVar(value=3.0)
point_count = tk.IntVar(value=240)
speed = tk.IntVar(value=20)
color = GOLD

running = False
drawn = 0
after_id = None
last_size = (0, 0)

def get_points():
    w = canvas.winfo_width()
    h = canvas.winfo_height()
    radius = min(w, h) * 0.43
    cx, cy = w / 2, h / 2
    n = point_count.get()

    return [
        (
            cx + radius * math.cos(2 * math.pi * i / n - math.pi / 2),
            cy + radius * math.sin(2 * math.pi * i / n - math.pi / 2)
        )
        for i in range(n)
    ]

def destination(i, n):
    # Fractional multipliers interpolate between points.
    value = (i * multiplier.get()) % n
    low = int(value)
    fraction = value - low
    high = (low + 1) % n
    return low, high, fraction

def target_position(points, i):
    n = len(points)
    low, high, fraction = destination(i, n)
    x1, y1 = points[low]
    x2, y2 = points[high]

    return (
        x1 * (1 - fraction) + x2 * fraction,
        y1 * (1 - fraction) + y2 * fraction
    )

def draw_scene():
    canvas.delete("all")

    w = canvas.winfo_width()
    h = canvas.winfo_height()
    if w < 100 or h < 100:
        return

    points = get_points()
    n = len(points)
    radius = min(w, h) * 0.43
    cx, cy = w / 2, h / 2

    # Outer circle
    canvas.create_oval(
        cx-radius, cy-radius, cx+radius, cy+radius,
        outline="#383838", width=1
    )

    # Draw the connections already completed.
    for i in range(min(drawn, n)):
        x1, y1 = points[i]
        x2, y2 = target_position(points, i)

        canvas.create_line(
            x1, y1, x2, y2,
            fill=color, width=0.7
        )

    # All numbered positions around the circumference.
    for x, y in points:
        canvas.create_oval(
            x-1.1, y-1.1, x+1.1, y+1.1,
            fill=WHITE, outline=""
        )

    # Moving point and the connection currently being drawn.
    if drawn < n:
        i = drawn
        x, y = points[i]
        tx, ty = target_position(points, i)

        canvas.create_line(
            x, y, tx, ty,
            fill=CYAN, width=1.8
        )

        # Highlight the moving point.
        canvas.create_oval(
            x-5, y-5, x+5, y+5,
            fill=GOLD, outline=WHITE, width=1
        )
    else:
        # Keep the final point highlighted.
        x, y = points[-1]
        canvas.create_oval(
            x-4, y-4, x+4, y+4,
            fill=GOLD, outline=WHITE
        )

    status.config(
        text=(
            f"CONNECTIONS: {drawn}/{n}    "
            f"MULTIPLIER: {multiplier.get():.1f}    "
            f"PROGRESS: {100 * drawn // n}%"
        )
    )

def animate():
    global drawn, running, after_id

    if not running:
        return

    n = point_count.get()

    if drawn >= n:
        running = False
        after_id = None
        play_button.config(text="▶  REPLAY")
        draw_scene()
        return

    drawn += 1
    draw_scene()

    # Lower delay means faster drawing.
    after_id = root.after(speed.get(), animate)

def start_animation():
    global running, after_id

    if drawn >= point_count.get():
        reset_animation()

    if not running:
        running = True
        play_button.config(text="Ⅱ  PAUSE")
        animate()

def pause_animation():
    global running, after_id

    running = False

    if after_id is not None:
        root.after_cancel(after_id)
        after_id = None

    play_button.config(text="▶  RESUME")

def toggle_animation():
    if running:
        pause_animation()
    else:
        start_animation()

def reset_animation():
    global running, drawn, after_id

    running = False

    if after_id is not None:
        root.after_cancel(after_id)
        after_id = None

    drawn = 0
    play_button.config(text="▶  START")
    draw_scene()

def settings_changed(_=None):
    reset_animation()

def change_color(new_color):
    global color
    color = new_color
    draw_scene()


def save_art():
    filename = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG Image", "*.png")],
        title="Save your mathematical artwork"
    )

    if filename:
        try:
            canvas.postscript(file="temp_artwork.ps", colormode="color")

            from PIL import Image

            img = Image.open("temp_artwork.ps")
            img.save(filename, "PNG")
            img.close()

            status.config(text="Artwork saved successfully!")

        except Exception as e:
            status.config(text=f"Save failed: {e}")

# Multiplier control
tk.Label(
    controls, text="MULTIPLIER",
    fg=WHITE, bg=BG, font=("Consolas", 10)
).grid(row=0, column=0, padx=5)

tk.Scale(
    controls, from_=2, to=10, resolution=0.1,
    variable=multiplier, orient="horizontal",
    length=180, bg=BG, fg=WHITE,
    troughcolor="#333333", highlightthickness=0,
    command=settings_changed
).grid(row=0, column=1, padx=5)

# Number of points
tk.Label(
    controls, text="POINTS",
    fg=WHITE, bg=BG, font=("Consolas", 10)
).grid(row=0, column=2, padx=5)

tk.Scale(
    controls, from_=80, to=360, resolution=20,
    variable=point_count, orient="horizontal",
    length=160, bg=BG, fg=WHITE,
    troughcolor="#333333", highlightthickness=0,
    command=settings_changed
).grid(row=0, column=3, padx=5)

# Animation speed
tk.Label(
    controls, text="SPEED",
    fg=WHITE, bg=BG, font=("Consolas", 10)
).grid(row=0, column=4, padx=5)

tk.Scale(
    controls, from_=5, to=100, resolution=5,
    variable=speed, orient="horizontal",
    length=120, bg=BG, fg=WHITE,
    troughcolor="#333333", highlightthickness=0,
    command=lambda _: None
).grid(row=0, column=5, padx=5)

# Buttons
buttons = tk.Frame(root, bg=BG)
buttons.pack(pady=8)

play_button = tk.Button(
    buttons, text="▶  START",
    command=toggle_animation, bg=GOLD, fg=BG,
    relief="flat", padx=18, pady=8,
    font=("Consolas", 10, "bold")
)
play_button.grid(row=0, column=0, padx=5)

tk.Button(
    buttons, text="↺  RESET",
    command=reset_animation, bg="#202020",
    fg=WHITE, relief="flat", padx=18, pady=8
).grid(row=0, column=1, padx=5)

tk.Button(
    buttons, text="RED", command=lambda: change_color(RED),
    bg="#202020", fg=RED, relief="flat", padx=12, pady=8
).grid(row=0, column=2, padx=5)

tk.Button(
    buttons, text="GREEN", command=lambda: change_color(GREEN),
    bg="#202020", fg=GREEN, relief="flat", padx=12, pady=8
).grid(row=0, column=3, padx=5)

tk.Button(
    buttons, text="BLUE", command=lambda: change_color(CYAN),
    bg="#202020", fg=CYAN, relief="flat", padx=12, pady=8
).grid(row=0, column=4, padx=5)

tk.Button(    
    buttons, text="SAVE ARTWORK", command=save_art,
    bg="#202020", fg=WHITE, relief="flat", padx=12, pady=8
).grid(row=0, column=5, padx=5)

status = tk.Label(
    root, text="Ready to explore.",
    fg=CYAN, bg=BG, font=("Consolas", 10)
)
status.pack(pady=(4, 12))

canvas.bind("<Configure>", lambda event: draw_scene())
root.after(200, draw_scene)

root.mainloop()
