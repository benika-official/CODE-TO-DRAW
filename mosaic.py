"""
LEVEL 1 — Pixel Mosaic
------------------------
Reads an image, shrinks it down to a small grid (so each "pixel" becomes a
visible block), reads the RGB color of every cell, and redraws the whole
image as colored squares using matplotlib.

Usage:
    python mosaic.py path/to/image.jpg
    python mosaic.py path/to/image.jpg --grid 40
"""

import sys
import argparse
from pathlib import Path

from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def load_pixel_grid(image_path: str, grid_size: int):
    """
    Shrinks the image down to grid_size x grid_size and returns a 2D list
    of (r, g, b) tuples — one per cell.
    """
    img = Image.open(image_path).convert("RGB")
    # Resize down to grid_size x grid_size. Each resulting pixel represents
    # the average color of a whole block of the original image.
    small = img.resize((grid_size, grid_size), Image.LANCZOS)

    pixels = small.load()
    grid = []
    for y in range(grid_size):
        row = []
        for x in range(grid_size):
            row.append(pixels[x, y])
        grid.append(row)
    return grid


def draw_mosaic(grid, output_path: str, cell_size: float = 1.0):
    """
    Draws the pixel grid as colored squares and saves it as an image.
    """
    grid_size = len(grid)
    fig, ax = plt.subplots(figsize=(8, 8))

    for y, row in enumerate(grid):
        for x, (r, g, b) in enumerate(row):
            color = (r / 255, g / 255, b / 255)
            # Flip y so the image isn't drawn upside down.
            rect = patches.Rectangle(
                (x * cell_size, (grid_size - 1 - y) * cell_size),
                cell_size, cell_size,
                facecolor=color,
                edgecolor="none"
            )
            ax.add_patch(rect)

    ax.set_xlim(0, grid_size * cell_size)
    ax.set_ylim(0, grid_size * cell_size)
    ax.set_aspect("equal")
    ax.axis("off")

    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    print(f"Saved mosaic to {output_path}")
    plt.show()


def main():
    parser = argparse.ArgumentParser(description="Redraw an image as a pixel mosaic.")
    parser.add_argument("image", help="Path to input image")
    parser.add_argument("--grid", type=int, default=32, help="Grid size (default: 32x32)")
    parser.add_argument("--out", default=None, help="Output file path")
    args = parser.parse_args()

    input_path = Path(args.image)
    if not input_path.exists():
        print(f"Error: {input_path} not found.")
        sys.exit(1)

    output_path = args.out or f"images/output/{input_path.stem}_mosaic.png"
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    print(f"Loading '{input_path.name}' and reducing to a {args.grid}x{args.grid} grid...")
    grid = load_pixel_grid(str(input_path), args.grid)

    print("Drawing mosaic...")
    draw_mosaic(grid, output_path)


if __name__ == "__main__":
    main()
