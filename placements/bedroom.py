from svgwrite.container import Group
from utils import get_object_indices
from placements.utils import *

from annot_data import directions

def get_corner_asset_position(cx, cy, desired_direction, obj_dim):
    padding = 7
    if desired_direction == "South":
        x = cx - obj_dim[0] - padding
        y = cy + padding
    elif desired_direction == "North":
        x = cx + padding
        y = cy - obj_dim[1] - padding
    elif desired_direction == "East":
        x = cx + padding
        y = cy + padding
    else:  # West
        x = cx - obj_dim[0] - padding
        y = cy - obj_dim[1] - padding

    return x, y

def get_center_asset_position(cx, cy, desired_direction, obj_dim):
    padding = 5
    if desired_direction == "South":
        x = cx - obj_dim[0]//2
        y = cy + padding
    elif desired_direction == "North":
        x = cx - obj_dim[0]//2 + padding
        y = cy - obj_dim[1] - padding
    elif desired_direction == "East":
        x = cx + padding
        y = cy - obj_dim[1]//2
    else:  # West
        x = cx - obj_dim[0] - padding
        y = cy - obj_dim[1]//2

    return x, y

def get_bed_position(cx, cy, desired_direction, obj_dim):
    padding = 2
    if desired_direction == "South":
        x = cx
        y = cy + padding
    elif desired_direction == "North":
        x = cx
        y = cy - obj_dim[1] - padding
    elif desired_direction == "East":
        x = cx + padding + 4
        y = cy
    else:  # West
        x = cx - obj_dim[0] - padding - 4
        y = cy

    return x, y

def place_asset(image, start_point, dim, rotation, used_space, path="asset_data/bed.svg", padding=10):
    x, y = start_point
    used_space.append([[x,y], [x+dim[0], y+dim[1]]])
    
    if rotation==90:
        x += padding
    elif rotation==270:
        x -= padding

    g = Group()
    img = image.image(href=path, insert=(int(x), int(y)), size=(f"{dim[0]}px", f"{dim[1]}px"))

    center_x = x + dim[0] // 2
    center_y = y + dim[1] // 2
    img.rotate(rotation, center=(center_x, center_y))
    img['preserveAspectRatio'] = 'none'

    g.add(img)
    image.add(g)

def bedroom_asset_placement(image, room, data, used_space):
    windows_indices = get_object_indices(room, data["windows"], isMultiple=True)
    dimensions = [(110, 90), [80, 40]]
    paddings = [10, 25, 0]
    assets = ["asset_data/bed.svg", "asset_data/closet_vert.svg"]

    for win_idx in windows_indices:
        window = data["windows"][win_idx]
        wall_index = get_wall_index(room, [window])
        wall_direction = find_direction(room, wall_index)
        bed_direction = directions["bed.svg"]
        rotation = change_orientation(bed_direction, wall_direction)

        cx, cy = window[1:3]
        dim = dimensions[0]
        x, y = get_bed_position(cx, cy, wall_direction, dim)

        points = [[x, y], [x, y+dim[1]], [x+dim[0], y], [x+dim[0], y+dim[1]]]
        if isValidPoint(points, room, used_space):
            place_asset(image, points[0], dim, rotation, used_space)
            assets.pop(0)
            dimensions.pop(0)
            paddings.pop(0)
            break

        # what if above code not work?

    door_indices = get_object_indices(room, data["doors"], isMultiple=True)
    doors = [data["doors"][idx] for idx in door_indices]
    
    corner_points = [wall[0] for wall in room]
    center_points = [[(wall[0][0]+wall[1][0])//2, (wall[0][1]+wall[1][1])//2] for wall in room]
    sorted_points = sort_corners(corner_points, doors)

    for i, asset in enumerate(assets):
        isPlaced = False
        dim = dimensions[i]
        asset_direction = directions[asset.split("/")[-1]]
        padding = paddings[i]

        for idx, point in enumerate(center_points):
            wall = room[idx]
            wall_direction = find_direction(room, idx)
            rotation = change_orientation(asset_direction, wall_direction)
            if "closet" in asset and rotation in [90, 270]:
                dim = dim[::-1]
                dim = [10,10]
                asset = asset.split(".")[0] + "_vert.svg"
                rotation = 0 if rotation==270 else 180

            # rotation = 0
            x, y = get_center_asset_position(point[0], point[1], wall_direction, dim)
            points = [[x, y], [x, y+dim[1]], [x+dim[0], y], [x+dim[0], y+dim[1]]]
            if isValidPoint(points, room, used_space):
                place_asset(image, points[0], dim, rotation, used_space, asset, padding)
                isPlaced = True
                break

        if isPlaced:
            continue

        for point in sorted_points.keys():
            idx = get_tuple_index(room, point)
            wall = room[idx]
            wall_direction = find_direction(room, idx)
            rotation = change_orientation(asset_direction, wall_direction)
            if "closet" in asset and rotation in [90, 270]:
                dim = dim[::-1]
                asset = asset.split(".")[0] + "_vert.svg"
                rotation = 0 if rotation==90 else 180
            # print(asset)

            x, y = get_corner_asset_position(wall[0][0], wall[0][1], wall_direction, dim)
            points = [[x, y], [x, y+dim[1]], [x+dim[0], y], [x+dim[0], y+dim[1]]]
            
            if isValidPoint(points, room, used_space):
                place_asset(image, points[0], dim, rotation, used_space, asset, padding)
                isPlaced = True
                break






# The provided code snippet focuses on the placement of bed assets within a room in an SVG floorplan. It includes several functions that work together to calculate the position and orientation of the bed, place the bed on the SVG canvas, and ensure the bed is correctly positioned based on room layout and window locations.

# The `get_bed_position` function calculates the position for placing a bed based on given corner coordinates, desired direction, and bed dimensions. It takes `cx` and `cy` (corner coordinates), `desired_direction` (desired direction for bed placement), and `obj_dim` (dimensions of the bed) as input. The function adjusts the coordinates with a padding of 8 units depending on the desired direction (South, North, East, or West). It then outputs the new coordinates `(x, y)` for placing the bed.

# The `place_bed` function handles placing a bed image onto the SVG canvas. It requires `image` (SVG canvas), `start_point` (initial position), `dim` (dimensions of the bed), `rotation` (angle of rotation), and `used_space` (list of already occupied spaces) as input. The function creates an SVG group element (`g`) and adds the bed image to this group. It rotates the image around its center and adds it to the main SVG canvas. The space occupied by the bed is appended to the `used_space` list. This ensures that the bed is correctly added to the SVG canvas and its occupied space is recorded.

# The `bed_asset_placement` function is responsible for the specific placement of bed assets within a room. It takes `image` (SVG canvas), `room` (room coordinates), `data` (additional data), and `used_space` (list of already occupied spaces) as input. The function begins by finding the indices of windows in the room using the `get_object_indices` function. It then determines the direction and orientation for placing the bed based on the direction of the walls and windows. The appropriate position and dimensions for the bed are calculated. The function checks if the calculated position is valid and not overlapping with existing assets. If the position is valid, the bed is placed using the `place_bed` function.

# The code also includes several utility imports. The `Group` class from `svgwrite.container` is used to create grouped elements in the SVG. The `get_object_indices` function from `utils` and various functions from `placements.utils` provide additional functionality required for asset placement. The `directions` constant from `annot_data` provides directional constants used in bed placement. These utility imports contribute to the precise and organized placement of assets within the SVG floorplan, ensuring each item is correctly positioned and oriented based on room layout and specified parameters.