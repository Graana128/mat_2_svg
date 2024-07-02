from svgwrite.container import Group
from placements.utils import *

from annot_data import directions


def get_sliding_door(door, room_type, direction):
    door_threshold = 70
    door_size = door[4] if door[3] == 0 else door[3]
    if room_type in [9, 11, 12] or door_size >= door_threshold:
        return "asset_data/sliding_door.svg"

    return None

def get_door_path(wall, door, room_type, direction):
    if room_type == 0:
        return "asset_data/double_door.svg"
    
    sliding_door = get_sliding_door(door, room_type, direction)
    if sliding_door != None:
        return sliding_door

    wall_point1, wall_point2 = wall
    door_point1 = [int(door[1]), int(door[2])]
    door_point2 = [int(door[1] + door[3]), int(door[2] + door[4])]

    distance1 = calculate_distance(wall_point1, door_point1)
    distance2 = calculate_distance(wall_point2, door_point2)

    return "asset_data/right_door.svg" if distance1 > distance2 else "asset_data/left_door.svg"

def get_points(wall):
    start_point, end_point = wall[0], wall[1]
    if start_point[0] > end_point[0] or start_point[1] > end_point[1]:
        return end_point, start_point

    return start_point, end_point

def get_door_position(door_path, door, desired_direction, door_dim):
    cx, cy = door[1], door[2]
    if 'sliding_door' in door_path:
        if desired_direction == "South":
            x = cx
            y = cy - 5
        elif desired_direction == "North":
            x = cx
            y = cy - 5
        elif desired_direction == "East":
            x = cx - door_dim[1]//2
            y = cy
        else:  # West
            x = cx - door_dim[1]//2
            y = cy
    elif 'double_door' in door_path:
        if desired_direction == "South":
            x = cx
            y = cy
        elif desired_direction == "North":
            x = cx
            y = cy - door_dim[1]
        elif desired_direction == "East":
            x = cx
            y = cy
        else:  # West
            x = cx - door_dim[0]
            y = cy
    else:
        if desired_direction == "South":
            x = cx
            y = cy 
        elif desired_direction == "North":
            x = cx
            y = cy - door_dim[1]
        elif desired_direction == "East":
            x = cx
            y = cy
        else:  # West
            x = cx - door_dim[0]
            y = cy

    return x, y

def place_asset(image, start_point, dim, rotation, used_space, path):
    x, y = start_point
    used_space.append([[x,y], [x+dim[0], y+dim[1]]])

    g = Group()
    img = image.image(href=path, insert=(int(x), int(y)), size=(f"{dim[0]}px", f"{dim[1]}px"))

    center_x = x + dim[0] / 2
    center_y = y + dim[1] / 2
    img['preserveAspectRatio'] = 'none'
    img.rotate(rotation, center=(center_x, center_y))

    g.add(img)
    image.add(g)
    used_space.append([[x, y], [x + dim[0], y + dim[1]]])

def door_asset_placement(image, room, room_type, data, door_index, used_space):
    if room_type == 0:
        start_point, end_point = get_points(room[0])
        door = [0, *start_point, abs(start_point[0] - end_point[0]), abs(start_point[1] - end_point[1])]
    else:
        if not door_index:
            print(f"No door indices provided for room type {room_type}")
            return
        if door_index[0] >= len(data["doors"]):
            print(f"Invalid door index {door_index[0]} for room type {room_type}")
            return
        
        door = data["doors"][door_index[0]]
    size = door[4] if door[3] == 0 else door[3]
    
    wall_index = 0 if room_type == 0 else get_wall_index(room, [door])
    wall_direction = find_direction(room, wall_index)
    
    door_path = get_door_path(room[wall_index], door, room_type, wall_direction)
    if "sliding_door" in door_path:
        path, dim, wall_direction, rotation = get_asset_info(door_path, [size, 10], room, wall_index)
    else:
        door_direction = directions[door_path.split("/")[1]]
        path, dim = door_path, (size, size)
        rotation = change_orientation(door_direction, wall_direction)
        
    x, y  = get_door_position(door_path, door, wall_direction, dim)
    place_asset(image, (x,y), dim, rotation, used_space, path)
    return used_space[-1]

    
    
    
    # print(door_path.split("_rot"))
    # if door_path in ["asset_data/right_door_rot.svg", 'asset_data/right_door_rot.svg']:
    #     door_path = "".join(door_path.split("_rot"))
    #     print(door_path)
    # if "sliding_door" in door_path:
    #     width, height = [size, 10]
    # else:
    #     width, height = size, size

    # door_path, dim, wall_direction, rotation = get_asset_info(door_path, [width, height], room, wall_index)

    # x, y = get_door_position(door_path, door, wall_direction, (width, height))


    
    # g = Group()
    # img = image.image(href=door_path, insert=(int(x), int(y)), size=(f"{width}px", f"{height}px"))
    # img.rotate(rotation, center=(width // 2, height // 2))
    # g.add(img)
    # image.add(g)

    # used_space.append([[x, y], [x + width, y + height]])
    # return used_space[-1]





# The provided code is a series of functions aimed at accurately placing door assets within a room layout based on specific criteria. Here's a detailed summary in paragraphs:

# The `get_door_path` function determines the file path for the appropriate door asset based on the room type and the relative positions of the door and wall points. For room types 0, 9, and 11, it assigns specific door types such as double doors or sliding doors. For other room types, it uses the distances between wall points and door points to decide whether to use a right or left door asset.

# The `get_door_position` function calculates the exact position to place a door asset within the room, taking into account the room type and the desired door direction. It adjusts the door's coordinates (cx, cy) based on the room type and the direction (North, South, East, West). For instance, it makes specific adjustments for sliding doors and double doors, ensuring the door is positioned correctly relative to the wall and room layout.

# The `get_points` function ensures the correct order of wall points, returning them in ascending order of their coordinates. This function helps maintain consistency in how wall points are referenced and used throughout the placement process.

# The `door_asset_placement` function, which is incomplete in the provided snippet, likely integrates the previous functions to place a door asset within the room. It would utilize the determined door path, calculated door position, and the room's wall points to accurately position the door. It also considers used space to avoid overlaps and ensure the door is placed in an available and appropriate location.

# Overall, these functions work together to ensure that door assets are placed accurately and appropriately within a room layout, respecting the room's walls, type, and available space.