"""
LEVEL 2 — Turtle Pixel Draw
-----------------------------
Same idea as Level 1 (shrink the image to a grid, read each pixel's color),
but this time a turtle physically draws each square on screen, one at a
time, so you can watch the image get built live.

Usage:
    python turtle_draw.py path/to/image.jpg
    python turtle_draw.py path/to/image.jpg --grid 25 --speed 0
"""

import sys
import argparse
import turtle
from pathlib import Path

from PIL import Image


def load_pixel_grid(image_path: str, grid_size: int):
    img = Image.open(image_path).convert("RGB")
    small = img.resize((grid_size, grid_size), Image.LANCZOS)
    pixels = small.load()

    grid = []
    for y in range(grid_size):
        row = []
        for x in range(grid_size):
            row.append(pixels[x, y])
        grid.append(row)
    return grid


def draw_pixel(t: turtle.Turtle, x, y, size, color):
    """Draws one filled square at (x, y) with the given side length + color."""
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.fillcolor(color)
    t.begin_fill()
    for _ in range(4):
        t.forward(size)
        t.right(90)
    t.end_fill()


def draw_grid(grid, canvas_size=600, speed=0):
    grid_size = len(grid)
    cell_size = canvas_size / grid_size

    screen = turtle.Screen()
    screen.setup(canvas_size + 60, canvas_size + 60)
    screen.title("CODE TO DRAW — Level 2: Turtle Pixel Draw")
    screen.tracer(0)  # turn off auto-refresh for a MUCH faster draw

    t = turtle.Turtle()
    t.hideturtle()
    t.speed(speed)
    t.penup()

    start_x = -canvas_size / 2
    start_y = canvas_size / 2

    for row_index, row in enumerate(grid):
        for col_index, (r, g, b) in enumerate(row):
            color = (r / 255, g / 255, b / 255)
            x = start_x + col_index * cell_size
            y = start_y - row_index * cell_size
            draw_pixel(t, x, y, cell_size, color)

        # Refresh once per row so you can still see it "build" without
        # being painfully slow.
        screen.update()

    screen.update()
    print("Done! Click the window to close.")
    screen.exitonclick()


def main():
    parser = argparse.ArgumentParser(description="Draw an image live using turtle graphics.")
    parser.add_argument("image", help="Path to input image")
    parser.add_argument("--grid", type=int, default=25, help="Grid size (default: 25x25). Keep it small — turtle is slow!")
    parser.add_argument("--speed", type=int, default=0, help="Turtle draw speed 0-10 (0 = fastest)")
    args = parser.parse_args()

    input_path = Path(args.image)
    if not input_path.exists():
        print(f"Error: {input_path} not found.")
        sys.exit(1)

    print(f"Loading '{input_path.name}' and reducing to a {args.grid}x{args.grid} grid...")
    grid = load_pixel_grid(str(input_path), args.grid)

    print("Drawing... a turtle window should open.")
    draw_grid(grid, speed=args.speed)


if __name__ == "__main__":
    main()
