from reportlab.pdfgen import canvas

def generate_template(
    output_file: str,
    paper_format: tuple,
    theme: dict,
    density: int,
    margin: list,
    thickness: float,
    help_lines: str|int
    ):
    """generates blank template

    Args:
        output_file (str): path + name of output file
        paper_format (tuple): paper format (width, height)
        theme (dict): color theme {'background_color': str in hexcolor, 'line_color': str in hexcolor}
        density (int): not used
        margin (list): not used
        thickness (float): not used
        help_lines (str | int, optional): not used
    """    
    width, height = paper_format
    c = canvas.Canvas(output_file, pagesize=(width, height))

    # Apply background color
    c.setFillColor(theme['background_color'])
    c.rect(0, 0, width, height, fill=True, stroke=False)
    
    c.save()