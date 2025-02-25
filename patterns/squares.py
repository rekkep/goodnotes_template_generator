from reportlab.pdfgen import canvas
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
    fill_perfect: bool = False
    ):
    
    """generates PDF with square grid

    Args:
        output_file (str): path + name of output file
        paper_format (tuple): paper format (width, height)
        density (int): how dense the squares should be
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
    
    ## generates horizontal lines ##
    
    # array of horizontal spacing
    base_values_horizontal = np.linspace(0, square_count_height, square_count_height)
    # get max length of horizontal lines
    horizontal_max = square_size * square_count_width + margin[0]
    
    # y-values for the horizontal lines
    y_horizontal_values = base_values_horizontal * square_size + margin[2]
    
    # x-values for the horizontal lines
    x_horizontal_start = np.full(square_count_height, margin[2])
    x_horizontal_end = np.full(square_count_height, paper_format[0] - margin[3])
    
    # horizontal lines list with x- and y-values
    horizontal_line_list = np.stack((x_horizontal_start, y_horizontal_values, x_horizontal_end, y_horizontal_values), axis=-1)
    
    
    ## vertical lines ##
    
    # array of vertical spacing
    base_values_vertical = np.linspace(0, square_count_width, square_count_width)
    
    # x-values for the vertical lines
    x_vertical_values = base_values_vertical * square_size + margin[2]
    # y-values for the vertical lines
    y_vertical_start = np.full(square_count_width, margin[0])
    y_vertical_end = np.full(square_count_width, paper_format[1] - margin[1])
    
    # vertical lines list with x- and y-values
    vertical_line_list = np.stack((x_vertical_values, y_vertical_start, x_vertical_values, y_vertical_end), axis=-1)
    
    
    # combine vertical and horizontal lines
    line_list = np.concatenate([horizontal_line_list, vertical_line_list], axis=0)
    
    ## generate pdf ##
    
    # create a canvas with the given paper format (width, height)
    c = canvas.Canvas(output_file, pagesize=paper_format)
    
    # fill background
    c.setFillColor(theme['background_color'])
    c.rect(0, 0, paper_format[0], paper_format[1], fill=True, stroke=False)
    
    # set line color and thickness
    c.setStrokeColor(theme['line_color'])
    c.setLineWidth(thickness)
    
    # draw all lines
    c.lines(line_list)
    
    # close and save
    c.showPage()
    c.save()
