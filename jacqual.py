#  ---------- Imports

import argparse
import os

from PIL import Image, ImageDraw

# ---------- Functions

def draw_grid(image, margin, grid_size=10, line_width=1, line_color=(0, 0, 0)):
    draw = ImageDraw.Draw(image)
    width, height = image.size

    #  line is draw in the middle. If line_width = 5, 2*1px lines will be drawn before, 1 px central and 2x1px after
    if (line_width % 2) == 0:
        line_gap = int(line_width / 2) - 1
    else:
        line_gap = int(line_width / 2)

    # Vertical black lines
    for x in range(margin, width - margin, grid_size + line_width):
        line = ((x + line_gap, 0), (x + line_gap, height))
        draw.line(line, fill=line_color, width=line_width)

    # Horizontal black lines
    for y in range(margin, height - margin, grid_size + line_width):
        line = ((0, y + line_gap), (width, y + line_gap))
        draw.line(line, fill=line_color, width=line_width)

    # Vertical red lines
    line_counter = 10
    for x in range(margin, width - margin, grid_size + line_width):
        if line_counter == 10:
            line_counter = 1
            line = ((x + line_gap, 0), (x + line_gap, height))
            draw.line(line, fill=(255, 0, 0), width=line_width)
        else:
            line_counter = line_counter + 1

    # Horizontal red lines
    line_counter = 10
    for y in range(margin, height - margin, grid_size + line_width):

        if line_counter == 10:
            line_counter = 1
            line = ((0, y + line_gap), (width, y + line_gap))
            draw.line(line, fill=(255, 0, 0), width=line_width)
        else:
            line_counter = line_counter + 1


# ---------- Argument parser

parser = argparse.ArgumentParser()

# Mandatory args
parser.add_argument('input_image', type=str,
                    help='Path to the input image.')
parser.add_argument('meshes_number', type=int,
                    help='Number of desired meshes (= columns = width).')
parser.add_argument('rows_number', type=int,
                    help='Number of desired rows (= height).')
parser.add_argument('colors_number', type=int,
                    help='Number of desired colors.')
parser.add_argument('enlarge_factor', type=int,
                    help='Factor to enlarge the pixels with.')
parser.add_argument('grid_thickness', type=int,
                    help='Grid thickness in px (5 px maximum).')
args = parser.parse_args()


# ---------- Main script

# ----- 0. Input args

grd_thck = args.grid_thickness
if (grd_thck > 5):
    grd_thck = 5

enl_fac = args.enlarge_factor
margin = 50  #  to better see the grid on edges

img_path_wo_ext = os.path.splitext(os.path.basename(args.input_image))[0]
print("Input image without ext: ", img_path_wo_ext)

print('''Launching jacqual using parameters:

input_image = {input_image}
meshes_number = {meshes_number}
rows_number = {rows_number}
colors_number = {colors_number}
enlarge_factor = {enlarge_factor}
grid_thickness = {grid_thickness}

Begin processing...
'''.format(input_image=args.input_image, meshes_number=args.meshes_number, rows_number=args.rows_number, colors_number=args.colors_number, enlarge_factor=args.enlarge_factor, grid_thickness=args.grid_thickness))

# ----- 1. Resize input image

input_img = Image.open(args.input_image)
input_img = input_img.convert('RGB')  #  remove transparency
newsize = (args.meshes_number, args.rows_number)
resized_img = input_img.resize(newsize)

# ----- 2. Reduce the number of colors

resized_img = resized_img.quantize(colors=args.colors_number)
resized_img = resized_img.convert('RGB')  #  required because quantize() changes the palette

# ----- 3. Build a new image with enlarged pixels (x enl_fac)

# Get resized_img image size in pixels
width, height = resized_img.size

# Create a new image with margin and enough space for the grid
upscaled_img = Image.new('RGB', (width * enl_fac + (width + 1) * grd_thck + 2 * margin, height * enl_fac + (height + 1) * grd_thck + 2 * margin), color='white')

# Iterate through each pixel of resized_img
for y in range(height):
    for x in range(width):
        # Get the pixel value at the current position
        pixel = resized_img.getpixel((x, y))

        # Duplicate the pixel 4x4 times in the enlarged image
        for dy in range(enl_fac):
            for dx in range(enl_fac):
                upscaled_img.putpixel((x * enl_fac + dx + (x + 1) * grd_thck + margin, y * enl_fac + dy + (y + 1) * grd_thck + margin), pixel)


# ----- 4. Draw a black grid of thickness grd_thck with a red line every ten meshes

draw_grid(upscaled_img, margin, enl_fac, grd_thck)

# ----- 5. Save output file

output_img = os.path.join(os.getcwd(), img_path_wo_ext + '_jacquard.png')
print('Saving file: ', output_img)
upscaled_img.save(output_img, format='PNG')
