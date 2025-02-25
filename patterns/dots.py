from reportlab.graphics.shapes import Drawing, Circle, Rect
from reportlab.graphics import renderPDF
from reportlab.lib.colors import HexColor
import numpy as np
from patterns.helper.perfect_fill import perfect_fill


def generate_template(
    output_file: str,
    paper_format: tuple,
    density: int,
    margin: list,
    theme: dict,
    thickness: float,
    help_lines: str|int,
    fill_perfect: bool = False,
    ):
    
    """generates PDF with dotted grid

    Args:
        output_file (str): path + name of output file
        paper_format (tuple): paper format (width, height)
        density (int): how dense the dots should be
        margin (list): margin [left_bottom, right_bottom, left_top, right_top]
        theme (dict): color theme {'background_color': str in hexcolor, 'line_color': str in hexcolor}
        thickness (float): line thickness
        filles_perfect (bool, optional): choose if the squares should perfectly fill the paper. Default to True
        help_lines (str | int, optional): not used
    """
    
    ## base values ##
    
    # calculate the available height and width of the paper
    available_height = paper_format[1] - margin[0] - margin[1]
    available_width = paper_format[0] - margin[2] - margin[3]
    
    # calculate the spacing between lines
    desired_square_size = available_height / (density - 1)
    
    # check if the squares will fill the paper perfectly
    perfekt_square_size = perfect_fill(available_width, available_height, desired_square_size, use_nearest_size=fill_perfect)
    
    # set square size depending on user liking
    # use perfect fill / use user set size
    if fill_perfect:
        square_size = perfekt_square_size
    else:
        square_size = desired_square_size
    
    # square count for the height
    square_count_height = int(available_height / square_size)
    # square count for the width
    square_count_width = int(available_width / square_size)
    
    drawing = Drawing(paper_format[0], paper_format[1])
    
    # set background color
    background_rect = Rect(0, 0, available_width, available_height)
    background_rect.fillColor = HexColor(theme['background_color'])
    background_rect.strokeColor = None
    drawing.add(background_rect)
    
    # Loop over rows and columns without printing every iteration.
    y_base = np.linspace(0, square_count_height, square_count_height)
    y_values = y_base * square_size + margin[2]
    
    x_base = np.linspace(0, square_count_width, square_count_width)
    x_values = x_base * square_size + margin[0]
    
    for y in y_values:
        for x in x_values:
            # Create a Circle shape and add it to the drawing.
            dot = Circle(x, y, thickness)
            dot.fillColor = HexColor(theme['line_color'])
            dot.strokeColor = None
            drawing.add(dot)
    
    # Render the complete drawing to a PDF.
    renderPDF.drawToFile(drawing, output_file)
    