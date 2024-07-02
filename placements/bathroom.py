from svgwrite.container import Group
from placements.utils import *
from utils import get_object_indices

from annot_data import directions


def get_corner_asset_position(cx, cy, desired_direction, obj_dim):
    padding = 5
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
        x = cx - obj_dim[0]//2
        y = cy - obj_dim[1] - padding
    elif desired_direction == "East":
        x = cx + padding
        y = cy - obj_dim[1]//2
    else:  # West
        x = cx - obj_dim[0] - padding
        y = cy - obj_dim[1]//2

    return x, y

def place_asset(image, start_point, dim, rotation, used_space, path):
    x, y = start_point
    g = Group()

    img = image.image(href=path, insert=(int(x), int(y)), size=(f"{dim[0]}px", f"{dim[1]}px"))
    img['preserveAspectRatio'] = 'none'

    center_x = x + dim[0] / 2
    center_y = y + dim[1] / 2
    img.rotate(rotation, center=(center_x, center_y))

    g.add(img)
    image.add(g)

    used_space.append([[x, y], [x+dim[0], y+dim[1]]])

def bathroom_asset_placement(image, room, room_type, data, used_space):
    door_indices = get_object_indices(room, data["doors"], isMultiple=True)
    doors = [data["doors"][idx] for idx in door_indices]
    
    corner_points = [wall[0] for wall in room]
    center_points = [[(wall[0][0]+wall[1][0])//2, (wall[0][1]+wall[1][1])//2] for wall in room]

    dimensions = [[40, 40], [35, 35], [35,35]]
    assets = ["asset_data/toilet.svg", "asset_data/shower.svg", "asset_data/sink.svg"]
    sorted_points = sort_corners(corner_points, doors)

    for i, asset_path in enumerate(assets):
        isPlaced = False
        dimension = dimensions[i]

        for point in sorted_points.keys():
            idx = get_tuple_index(room, point)
            
            wall = room[idx]
            wall_direction = find_direction(room, idx)
            path, dim, wall_direction, rotation = get_asset_info(asset_path, dimension, room, idx)

            x, y = get_corner_asset_position(wall[0][0], wall[0][1], wall_direction, dim)
            points = [[x, y], [x, y+dim[1]], [x+dim[0], y], [x+dim[0], y+dim[1]]]
            if isValidPoint(points, room, used_space):
                place_asset(image, points[0], dim, rotation, used_space, path)
                isPlaced = True
                break

        if isPlaced:
            continue

        for idx, point in enumerate(center_points):
            wall = room[idx]
            wall_direction = find_direction(room, idx)
            path, dim, wall_direction, rotation = get_asset_info(asset_path, dimension, room, idx)

            x, y = get_center_asset_position(point[0], point[1], wall_direction, dim)
            points = [[x, y], [x, y+dim[1]], [x+dim[0], y], [x+dim[0], y+dim[1]]]
            if isValidPoint(points, room, used_space):
                place_asset(image, points[0], dim, rotation, used_space, path)
                break























# The provided code snippet includes functions that assist with the placement of assets, such as furniture or fixtures, in an SVG floorplan. The first function, `sort_corners`, sorts corner points in a room based on their distances from door endpoints. It takes `corner_points` (a list of points representing room corners) and `doors` (a list of door coordinates and dimensions) as input. For each corner point, the function calculates the distance to each endpoint of every door and tracks the minimum distance. If this minimum distance is greater than or equal to 10, the corner point is included in the sorted dictionary. The dictionary is then sorted by distance in descending order, outputting a dictionary of corner points sorted by their distance from door endpoints.

# The `get_corner_asset__position` function determines the position of an asset based on a given corner and the desired direction for placement. It takes `cx` and `cy` (the coordinates of the corner), `desired_direction` (the direction for placement), and `obj_dim` (the dimensions of the asset) as input. The function calculates the new position of the asset by adjusting the corner coordinates according to the desired direction and adds padding to ensure the asset is placed with some space around it. The output is the new coordinates `(x, y)` for placing the asset.

# The `place_asset` function places an asset (image) onto the SVG canvas. It takes `image` (the SVG canvas), `start_point` (the initial position), `dim` (the dimensions of the asset), `rotation` (the angle of rotation), `used_space` (a list of already occupied spaces), and `path` (the path to the asset image) as input. The function calculates the center of the asset for rotation purposes and creates an SVG group element (`g`). It then adds the image to this group, rotates the image around its center, and adds the group to the main SVG canvas. The space occupied by the asset is appended to the `used_space` list. The function ensures that the asset is correctly placed and oriented on the SVG canvas, and its occupied space is recorded.

# The `bathroom_asset_placement` function is a placeholder for handling the specific placement of bathroom assets in a room. It takes `image` (the SVG canvas), `room` (room coordinates), `room_type` (the type of the room), `data` (additional data), and `used_space` (a list of already occupied spaces) as input. Although the function body is not provided, it is intended to use these input parameters to place bathroom-specific assets within the SVG canvas. The specific implementation details are not included, indicating that this function is intended to be further developed.

# Lastly, the code includes imports from other modules. The `Group` class from `svgwrite.container` is used to create grouped elements in the SVG. Utility functions from `placements.utils` and `get_object_indices` from `utils` are presumably used to provide additional functionality required for asset placement. The `directions` constant from `annot_data` likely provides directional constants used in asset placement. These utility imports contribute to the precise and organized placement of assets within the SVG floorplan, ensuring each item is correctly positioned and oriented based on room layout and specified parameters.