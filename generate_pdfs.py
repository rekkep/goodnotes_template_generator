"""
inspired by the "goodnotes-pdf-template-generation"-project by agedpomel (https://github.com/agedpomelo/goodnotes-pdf-template-generator)
"""

# import patterns.dots as dots
# import patterns.lines as lines
# import patterns.square as squares
# import patterns.blank as blank
# import patterns.hexagons as hexagons

import os
import importlib
import argparse

from json import load as json_load
from json import loads as json_loads

PAPER_SIZES_FILE = "paper_size/paper_sizes.json"
with open(PAPER_SIZES_FILE, "r") as themes:
    PAPER_SIZES = json_load(themes)

PATTERNS_DIR = "patterns/"


# PATTERNS = {
#     'blank': blank.generate_template,
#     'dots': dots.generate_template,
#     'hexagons': hexagons.generate_template,
#     'lines': lines.generate_template,
#     'squares': squares.generate_template
# }

# load themes
THEME_FILE = "themes/themes.json"
with open(THEME_FILE, "r") as themes:
    data = json_load(themes)
    THEMES = {k.lower(): v for k, v in data.items()}


def load_patterns():
    global PATTERNS
    PATTERNS = {}
    available_patterns = os.listdir(PATTERNS_DIR)
    for pattern in available_patterns:
        pattern.replace('.py', '')

    # Directory containing your pattern modules
    pattern_dir = "patterns"

    # Iterate over all files in the directory
    for filename in os.listdir(pattern_dir):
        if filename.endswith('.py') and not filename.startswith('__'):
            # Remove the '.py' extension
            module_name = filename[:-3]
            # Dynamically import the module from the patterns package
            module = importlib.import_module(f"patterns.{module_name}")
            globals()[module_name] = module
            
            PATTERNS[module_name] = module.generate_template



def bulk_generation(paper_sizes, out_dir, patterns, themes, orientations, density, margin, thickness, hexagon_lines):
    for pattern in patterns:
        action = PATTERNS[pattern]
        for theme in themes:
            theme_dir = os.path.join(out_dir, theme)
            os.makedirs(theme_dir, exist_ok=True)
            for paper_size in paper_sizes:
                size_dir = os.path.join(theme_dir, paper_size)
                for orientation in orientations:
                    if orientation == "landscape":
                        height, width = PAPER_SIZES[paper_size]
                        landscape_dir = os.path.join(size_dir, 'landscape')
                        os.makedirs(landscape_dir, exist_ok=True)
                        filename = f'{pattern}.pdf'
                        file_path = os.path.join(landscape_dir, filename)
                        action(output_file=file_path,
                            paper_format=(width, height),
                            density=density,
                            margin=margin,
                            theme=THEMES[theme],
                            thickness=thickness,
                            help_lines=hexagon_lines)
                        print(f"PDF file '{filename}' has been generated.")
                    elif orientation == "portrait":
                        width, height = PAPER_SIZES[paper_size]
                        portrait_dir = os.path.join(size_dir, 'portrait')
                        os.makedirs(portrait_dir, exist_ok=True)
                        filename = f'{pattern}.pdf'
                        file_path = os.path.join(portrait_dir, filename)
                        action(output_file=file_path,
                            paper_format=(width, height),
                            density=density,
                            margin=margin,
                            theme=THEMES[theme],
                            thickness=thickness,
                            help_lines=hexagon_lines)
                        print(f"PDF file '{filename}' has been generated.")
                

def main():
    
    load_patterns()
    
    parser = argparse.ArgumentParser(description="Generate PDFs for paper size, template and themes.")
    parser.add_argument("paper_size", 
                        choices=["all"] + list(PAPER_SIZES.keys()), 
                        help="Paper size")
    parser.add_argument("theme", 
                        choices=list(THEMES.keys()), 
                        help="Themes. To add more add your theme in the themes.json")
    parser.add_argument("--patterns", 
                        choices=["all"] + list(PATTERNS.keys()), 
                        default="all", 
                        help="Choose the pattern that should be generated")
    parser.add_argument("--orientation", 
                        choices=["all", 'landscape', 'portrait'], 
                        default="all", 
                        help="Paper orientation")
    parser.add_argument("--density", 
                        type=int, 
                        default=54, 
                        help="How dense the pattern shout be")
    parser.add_argument("--margin", 
                        type=json_loads, 
                        default=[-5, -5, -5, -5], 
                        help="Paper margin in format [left_bottom, right_bottom, left_top, right_top]")
    parser.add_argument("--thickness", 
                        type=float, 
                        default=0.2, 
                        help="Line thickness")
    parser.add_argument("--hexagonlines", 
                        type=int,
                        choices=list(range(0, 13)),
                        default=12, 
                        help="Line thickness")
    
    args = parser.parse_args()
    
    paper_size = list(PAPER_SIZES.keys()) if args.paper_size == "all" else [args.paper_size.lower()]
    theme = list(THEMES.keys()) if args.theme == "all" else [args.theme.lower()]
    patterns = list(PATTERNS.keys()) if args.patterns == "all" else [args.patterns.lower()]
    orientation = ['landscape', 'portrait'] if args.orientation == "all" else [args.orientation.lower()]
    density = args.density
    margin = args.margin
    thickness = args.thickness
    hexagon_lines = args.hexagonlines
    
    out_dir = "out"

    bulk_generation(
        paper_sizes = paper_size,
        themes = theme,
        out_dir = out_dir,
        patterns = patterns,
        orientations = orientation,
        density = density,
        margin = margin,
        thickness = thickness,
        hexagon_lines = hexagon_lines
    )
    
if __name__ == "__main__":
    main()