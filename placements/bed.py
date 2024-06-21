from svgwrite.container import Group
from utils import get_object_indices
from placements.utils import *

from annot_data import directions

def get_bed_position(cx, cy, desired_direction, obj_dim):
    padding = 8
    if desired_direction == "South":
        x = cx
        y = cy + padding
    elif desired_direction == "North":
        x = cx
        y = cy - obj_dim[1] - padding
    elif desired_direction == "East":
        x = cx + padding
        y = cy
    else:  # West
        x = cx - obj_dim[0] - padding
        y = cy

    return x, y

def place_bed(image, start_point, dim, rotation, used_space):
    x, y = start_point

    g = Group()

    img = image.image(href="asset_data/bed.svg", insert=(x, y), size=(f"{dim[0]}px", f"{dim[1]}px"))
    img['preserveAspectRatio'] = 'none'

    center_x = x + dim[0] / 2
    center_y = y + dim[1] / 2
    img.rotate(rotation, center=(center_x, center_y))

    g.add(img)
    image.add(g)

    used_space.append([[x+y], [x+dim[0], y+dim[1]]])

def bed_asset_placement(image, room, data, used_space):
    windows_indices = get_object_indices(room, data["windows"], isMultiple=True)
    bed_direction = directions["bed.svg"]

    for win_idx in windows_indices:
        window = data["windows"][win_idx]
        wall_index = get_wall_index(room, [window])
        wall_direction = find_direction(room, wall_index)
        rotation = change_orientation(bed_direction, wall_direction)

        cx, cy = window[1:3]
        dim = [70, 90] if not wall_direction in ["East", "West"] else [90, 70]
        x, y = get_bed_position(cx, cy, wall_direction, dim)

        points = [[x, y], [x, y+dim[1]], [x+dim[0], y], [x+dim[0], y+dim[1]]]
        if isValidPoint(points, room, used_space):
            place_bed(image, points[0], dim, rotation, used_space)
            break

        # what if above code not work?













# The provided code snippet focuses on the placement of bed assets within a room in an SVG floorplan. It includes several functions that work together to calculate the position and orientation of the bed, place the bed on the SVG canvas, and ensure the bed is correctly positioned based on room layout and window locations.

# The `get_bed_position` function calculates the position for placing a bed based on given corner coordinates, desired direction, and bed dimensions. It takes `cx` and `cy` (corner coordinates), `desired_direction` (desired direction for bed placement), and `obj_dim` (dimensions of the bed) as input. The function adjusts the coordinates with a padding of 8 units depending on the desired direction (South, North, East, or West). It then outputs the new coordinates `(x, y)` for placing the bed.

# The `place_bed` function handles placing a bed image onto the SVG canvas. It requires `image` (SVG canvas), `start_point` (initial position), `dim` (dimensions of the bed), `rotation` (angle of rotation), and `used_space` (list of already occupied spaces) as input. The function creates an SVG group element (`g`) and adds the bed image to this group. It rotates the image around its center and adds it to the main SVG canvas. The space occupied by the bed is appended to the `used_space` list. This ensures that the bed is correctly added to the SVG canvas and its occupied space is recorded.

# The `bed_asset_placement` function is responsible for the specific placement of bed assets within a room. It takes `image` (SVG canvas), `room` (room coordinates), `data` (additional data), and `used_space` (list of already occupied spaces) as input. The function begins by finding the indices of windows in the room using the `get_object_indices` function. It then determines the direction and orientation for placing the bed based on the direction of the walls and windows. The appropriate position and dimensions for the bed are calculated. The function checks if the calculated position is valid and not overlapping with existing assets. If the position is valid, the bed is placed using the `place_bed` function.

# The code also includes several utility imports. The `Group` class from `svgwrite.container` is used to create grouped elements in the SVG. The `get_object_indices` function from `utils` and various functions from `placements.utils` provide additional functionality required for asset placement. The `directions` constant from `annot_data` provides directional constants used in bed placement. These utility imports contribute to the precise and organized placement of assets within the SVG floorplan, ensuring each item is correctly positioned and oriented based on room layout and specified parameters.