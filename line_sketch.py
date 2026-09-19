"""
LEVEL 3 — Line Sketch
------------------------
Instead of filling in colored blocks, this level detects the EDGES in an
image (the outlines of shapes) and draws only those — turtle "sketches"
the picture like a pencil drawing instead of painting it in.

How the edge detection works (no heavy libraries needed):
    - Convert the image to grayscale.
    - Apply PIL's built-in FIND_EDGES filter, which highlights areas where
      brightness changes sharply (i.e. outlines).
    - Threshold it: any pixel brighter than the threshold counts as "edge".
    - Downsample to a grid like before, but this time each cell is either
      "draw a dot here" or "skip it" instead of a full color.

Usage:
    python line_sketch.py path/to/image.jpg
    python line_sketch.py path/to/image.jpg --grid 60 --threshold 40
"""

import sys
import argparse
import turtle
from pathlib import Path

from PIL import Image, ImageFilter


def load_edge_grid(image_path: str, grid_size: int, threshold: int):
    """
    Returns a 2D grid of booleans: True where an edge was detected.
    """
    img = Image.open(image_path).convert("L")  # grayscale
    edges = img.filter(ImageFilter.FIND_EDGES)
    small = edges.resize((grid_size, grid_size), Image.LANCZOS)
    pixels = small.load()

    grid = []
    for y in range(grid_size):
        row = []
        for x in range(grid_size):
            brightness = pixels[x, y]
            row.append(brightness > threshold)
        grid.append(row)
    return grid


def draw_sketch(grid, canvas_size=600, speed=0, dot_size=6):
    grid_size = len(grid)
    cell_size = canvas_size / grid_size

    screen = turtle.Screen()
    screen.setup(canvas_size + 60, canvas_size + 60)
    screen.title("CODE TO DRAW — Level 3: Line Sketch")
    screen.bgcolor("white")
    screen.tracer(0)

    t = turtle.Turtle()
    t.hideturtle()
    t.speed(speed)
    t.color("black")
    t.penup()

    start_x = -canvas_size / 2
    start_y = canvas_size / 2

    for row_index, row in enumerate(grid):
        for col_index, is_edge in enumerate(row):
            if not is_edge:
                continue
            x = start_x + col_index * cell_size
            y = start_y - row_index * cell_size
            t.goto(x, y)
            t.dot(dot_size)
        screen.update()

    screen.update()
    print("Done! Click the window to close.")
    screen.exitonclick()


def main():
    parser = argparse.ArgumentParser(description="Sketch an image's outlines using turtle graphics.")
    parser.add_argument("image", help="Path to input image")
    parser.add_argument("--grid", type=int, default=60, help="Grid size (default: 60x60)")
    parser.add_argument("--threshold", type=int, default=40,
                         help="Edge sensitivity 0-255. Lower = more lines detected (default: 40)")
    args = parser.parse_args()

    input_path = Path(args.image)
    if not input_path.exists():
        print(f"Error: {input_path} not found.")
        sys.exit(1)

    print(f"Loading '{input_path.name}' and detecting edges on a {args.grid}x{args.grid} grid...")
    grid = load_edge_grid(str(input_path), args.grid, args.threshold)

    print("Sketching... a turtle window should open.")
    draw_sketch(grid)


if __name__ == "__main__":
    main()
