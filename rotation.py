from glob import glob
import svgwrite
from svgpathtools import svg2paths, wsvg
import numpy as np

def rotate_point(point, angle_rad):
    """Rotate a point by a given angle in radians."""
    return point * np.exp(1j * angle_rad)

def rotate_svg(input_file, output_file, angle):
    # Load SVG paths and attributes
    paths, attributes = svg2paths(input_file)

    # Convert angle to radians
    angle_rad = np.deg2rad(angle)

    # Rotate each path
    for path in paths:
        for segment in path:
            segment.start = rotate_point(segment.start, angle_rad)
            segment.end = rotate_point(segment.end, angle_rad)
            if hasattr(segment, 'control1'):
                segment.control1 = rotate_point(segment.control1, angle_rad)
            if hasattr(segment, 'control2'):
                segment.control2 = rotate_point(segment.control2, angle_rad)

    # Save the rotated SVG
    wsvg(paths, attributes=attributes, filename=output_file)


# Usage


svg_files = glob("asset_data/*.svg")

svg_files = ["asset_data/double_door.svg"]
for file in svg_files:
    output_file = file.split(".")[0] + "_rot.svg"
    print(output_file)
    rotate_svg(file, output_file, 90)
