from reportlab.pdfgen import canvas
import numpy as np

def generate_template(
    output_file: str,
    paper_format: tuple,
    density: int,
    margin: list,
    theme: dict,
    thickness: float,
    help_lines: str|int
):
    """generates PDF with line grid

    Args:
        output_file (str): path + name of output file
        paper_format (tuple): paper format (width, height)
        density (int): how dense the lines should be
        margin (list): margin [left_bottom, right_bottom, left_top, right_top]
        theme (dict): color theme {'background_color': str in hexcolor, 'line_color': str in hexcolor}
        thickness (float): line thickness
        help_lines (str | int, optional): not used
    """    
    
    ## base values ##
    
    # calculate the available height and width of the paper
    available_height = paper_format[1] - margin[0] - margin[1]
    
    ## lines ##
    
    # calculate the spacing between lines
    line_spacing = available_height / (density - 1)
    base_values = np.linspace(0, density - 1, density)
    
    # generate y-values for the horizontal lines
    y_values = base_values * line_spacing + margin[0]
    
    # generate x-values for the horizontal lines
    x_start = np.full(density, margin[2])
    x_end = np.full(density, paper_format[0] - margin[3])
    
    # generate line list with x- and y-values
    line_list = np.stack((x_start, y_values, x_end, y_values), axis=-1)
    
    
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
