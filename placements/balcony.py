from svgwrite.container import Group
from placements.utils import *

from annot_data import directions

def get_coffetable_position(cx, cy, desired_direction, obj_dim):
    padding = 10
    if desired_direction == "South":
        x = cx - obj_dim[0]//2
        y = cy + padding
    elif desired_direction == "North":
        x = cx - obj_dim[0]//2
        y = cy - obj_dim[1] - padding
    elif desired_direction == "East":
        x = cx + obj_dim[0]
        y = cy - obj_dim[1]//2
    else:  # West
        x = cx - obj_dim[0] - padding
        y = cy - obj_dim[1]

    return x, y

def get_plant_position(cx, cy, desired_direction, obj_dim):
    if desired_direction == "South":
        x = cx - obj_dim[0] - 5 
        y = cy + 5
    elif desired_direction == "North":
        x = cx + 5
        y = cy - obj_dim[1] - 5
    elif desired_direction == "East":
        x = cx + 5
        y = cy + 5
    else:  # West
        x = cx - obj_dim[0] - 5
        y = cy - obj_dim[1] - 5

    return x, y

def place_asset(image, start_point, dim, rotation, used_space, path):
    x, y = tuple(map(int, start_point))

    g = Group()

    img = image.image(href=path, insert=(x, y), size=(f"{dim[0]}px", f"{dim[1]}px"))
    img['preserveAspectRatio'] = 'none'

    center_x = x + dim[0] / 2
    center_y = y + dim[1] / 2
    img.rotate(rotation, center=(center_x, center_y))

    g.add(img)
    image.add(g)

    used_space.append([[x+y], [x+dim[0], y+dim[1]]])

def plant_asset_placement(image, room, used_space):
    dim = [15, 15]
    for wall_idx, wall in enumerate(room):
        cx, cy = wall[0]
        wall_direction = find_direction(room, wall_idx)
        start_point= get_plant_position(cx, cy, wall_direction, dim)
        place_asset(image, start_point, dim, 0, used_space, "asset_data/plant.svg")

def coffetable_asset_placement(image, room, data, used_space):
    dim = [50, 15]
    path = "asset_data/coffetable.svg"

    wall_index = get_wall_index(room, data["windows"], largest=True)
    path, dim, wall_direction, rotation = get_asset_info(path, dim, room, wall_index)    

    cx = (room[wall_index][0][0] + room[wall_index][1][0]) // 2
    cy = (room[wall_index][0][1] + room[wall_index][1][1]) // 2
    x, y = get_coffetable_position(cx, cy, wall_direction, dim)

    place_asset(image, (x, y), dim, rotation, used_space, path)

def balcony_asset_placement(image, room, data, used_space):
    coffetable_asset_placement(image, room, data, used_space)
    plant_asset_placement(image, room, used_space)




