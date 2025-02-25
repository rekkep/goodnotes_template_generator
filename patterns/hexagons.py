# Import modules
from reportlab.pdfgen import canvas

from math import radians, sin, cos, sqrt

"""
Modified version of merv1n34k's HexPaper (https://github.com/merv1n34k/HexaPaper/tree/main)
"""

# Declare constants
MAX_HELP_LINES = 12
MIN_HELP_LINES = 0
SQ3 = sqrt(3)
BLACK = '#000000'

# Function to draw a line
def draw_line(
    canvas,
    length,
    angle,
    x_shift,
    y_shift,
    thickness=1 / 8,
    dashed=False,
    dash_length=None,
    color=BLACK
):
    """
    Draw a line with defined angle, length, shift by x and y coordinates,
    and thickness, color and dashed parameters as optional.
    """
    angle = radians(angle)
    x_origin, y_origin = x_shift, canvas._pagesize[1] - y_shift
    end_x = x_origin + length * cos(angle)
    end_y = y_origin - length * sin(angle)

    # set line width and color
    canvas.setLineWidth(thickness)
    canvas.setStrokeColor(color)

    if dashed:
        if not dash_length:
            dash_length = thickness * 2
        canvas.setDash((dash_length, 2 * dash_length))

    canvas.line(x_origin, y_origin, end_x, end_y)

    if dashed:
        canvas.setDash()


# Draw a hexagonal grid
def draw_grid(canvas, scale, help_lines_show, thickness_1, color_1, 
              thickness_2, color_2):
    """Create a grid of lines."""
    height, width = canvas._pagesize
    max_height = int(height//scale) + 1
    max_width = int(width//scale)
    #print(max_height,max_width) # print a paper max height and width depending on scale
    help_lines_number = 0
    hex_lines_number = 3
    help_lines = {
            "thickness" : thickness_2,
            "angles"  : [120,120,120,90,60,60,60,180,180,150,30,180],
            "lengths" : [1,1,1,2/SQ3,1,1,1,1,1,2/SQ3,2/SQ3,1],
            "shift_x" : [1/2,0,1/4,0,-1/2,0,-1/4,1/2,1/2,1/2,-1/2,1/2],
            "shift_y" : [0,-1/2,-1/4,-1/2,0,-1/2,-1/4,0,1,0,0,1/2],
            "dashed" : True,
            "dash_lengths" : 5,
            "color" : color_2,
    }
    hex_lines = {
            "thickness" : thickness_1,
            "angles"  : [30,90,150],
            "lengths" : 1/SQ3,
            "shift_x" : 0,
            "shift_y" : [1,3,1],
            "color" : color_1,
    }
    if help_lines_show == 'all':
        help_lines_number = MAX_HELP_LINES
    elif help_lines_show >= MIN_HELP_LINES and help_lines_show < MAX_HELP_LINES:
        help_lines_number = help_lines_show
    else:
        help_num = MIN_HELP_LINES
    n = 0
    for m in range(max_width):
        n -= 4
        for n in range(max_height):
            # If row is even then move it by one half
            if n%2 == 0:
                m += 1/2
            for x in range(help_lines_number):
                draw_line(
                    canvas,
                    help_lines["lengths"][x] * SQ3 * scale,
                    help_lines["angles"][x],
                    (help_lines["shift_x"][x] + m) * SQ3 * scale,
                    (help_lines["shift_y"][x] + 3/2 * n) * scale,
                    dashed=help_lines["dashed"],
                    dash_length=help_lines["dash_lengths"],
                    thickness=help_lines["thickness"],
                    color = help_lines["color"]
                )
            for x in range(hex_lines_number):
                draw_line(
                    canvas,
                    hex_lines["lengths"] * SQ3 * scale,
                    hex_lines["angles"][x],
                    (hex_lines["shift_x"] + m) * SQ3 * scale,
                    ( -1 / 2 * hex_lines["shift_y"][x] + 3/2 * n) * scale,
                    thickness=hex_lines["thickness"],
                    color = hex_lines["color"]
                )
            if n%2 == 0:
                m -= 1/2


# modification to work with the bulk generation and themes
def generate_template(
    output_file: str,
    paper_format: tuple,
    theme: dict,
    thickness: float,
    margin: list,
    density: int,
    scale: int = 25,
    help_lines: str|int = 'all'
    ):
    """Generates PDF with Hexagon pattern

    Args:
        output_file (str): Path and name of output file
        paper_format (tuple): size of the paper in format (width, height)
        theme (dict): color theme {'background_color': str in hexcolor, 'line_color': str in hexcolor}
        thickness (float): line thickness
        margin (list): not used, just for the bulk generation!
        density (int): not used, just for the bulk generation!
        scale (int, optional): 25 Best for a4 paper. Defaults to 25.
        help_lines (str | int, optional): this will configure how many help lined you want, options can be int 0-12 or "all". Defaults to 'all'.
    """    
    
    help_thickness = thickness / 3
    hex_thickness = thickness
    line_color = theme['line_color']
    
    
    # Create a new PDF file
    c = canvas.Canvas(output_file, pagesize=paper_format)
    # Apply background color
    c.setFillColor(theme['background_color'])
    c.rect(0, 0, paper_format[0], paper_format[1], fill=True, stroke=False)
    draw_grid(c,
                scale=scale, 
                help_lines_show=help_lines,
                thickness_1=hex_thickness,
                color_1=line_color,
                thickness_2=help_thickness,
                color_2=line_color)

    # Save the PDF file
    c.save()