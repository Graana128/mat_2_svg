from svgwrite.container import Group
from placements.utils import calculate_distance, find_direction, get_wall_index, change_orientation

from annot_data import directions

def get_door_path(wall, door, room_type):
        if room_type==0:
            return "asset_data/double_door.svg"   
        elif room_type in [9, 11]:
                return "asset_data/sliding_door.svg"

        wall_point1, wall_point2 = wall
        door_point1 = [int(door[1]), int(door[2])]
        door_point2 = [int(door[1]+door[3]), int(door[2]+door[4])]

        distance1 = calculate_distance(wall_point1, door_point1)
        distance2 = calculate_distance(wall_point2, door_point2)

        # if direction in ["East", "West"]:
        #     return "asset_data/right_door.svg" if distance1 > distance2 else "asset_data/left_door.svg"
        # else:
        return "asset_data/right_door.svg" if distance1 > distance2 else "asset_data/left_door.svg"
    
def get_door_position(room_type, door, desired_direction, door_dim):
    cx, cy = door[1], door[2]
    if room_type in [9, 11]:
        if desired_direction == "South":
            x = cx
            y = cy - door_dim[0]//2
        elif desired_direction == "North":
            x = cx
            y = cy - door_dim[1]//2
        elif desired_direction == "East":
            x = cx - door_dim[1]//2
            y = cy
        else:  # West
            x = cx - door_dim[1]//2
            y = cy
    elif room_type==0:
        if desired_direction == "South":
            x = cx
            y = cy-13
        elif desired_direction == "North":
            x = cx
            y = cy-door_dim[1]+10
        elif desired_direction == "East":
            x = cx-13
            y = cy
        else:  # West
            x = cx-door_dim[0]+15
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

def get_points(wall):
    start_point, end_point = wall[0], wall[1]
    if start_point[0] > end_point[0] or start_point[1] > end_point[1]:
        return end_point, start_point

    return start_point, end_point


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
    
    wall_index = 0 if room_type == 0 else get_wall_index(room, [door])
    desired_direction = find_direction(room, wall_index)
    door_path = get_door_path(room[wall_index], door, room_type)
    door_direction = directions[door_path.split("/")[-1]]

    size = door[4] if door[3] == 0 else door[3]
    width, height = size, size
    x, y = get_door_position(room_type, door, desired_direction, (width, height))
    rotation = change_orientation(door_direction, desired_direction)
      
    g = Group()
    img = image.image(href=door_path, size=(f"{width}px", f"{height}px"))
    img.translate(x, y)
    img.rotate(rotation, center=(width // 2, height // 2))
    g.add(img)
    image.add(g)

    used_space.append([[x, y], [x + width, y + height]])






# The provided code is a series of functions aimed at accurately placing door assets within a room layout based on specific criteria. Here's a detailed summary in paragraphs:

# The `get_door_path` function determines the file path for the appropriate door asset based on the room type and the relative positions of the door and wall points. For room types 0, 9, and 11, it assigns specific door types such as double doors or sliding doors. For other room types, it uses the distances between wall points and door points to decide whether to use a right or left door asset.

# The `get_door_position` function calculates the exact position to place a door asset within the room, taking into account the room type and the desired door direction. It adjusts the door's coordinates (cx, cy) based on the room type and the direction (North, South, East, West). For instance, it makes specific adjustments for sliding doors and double doors, ensuring the door is positioned correctly relative to the wall and room layout.

# The `get_points` function ensures the correct order of wall points, returning them in ascending order of their coordinates. This function helps maintain consistency in how wall points are referenced and used throughout the placement process.

# The `door_asset_placement` function, which is incomplete in the provided snippet, likely integrates the previous functions to place a door asset within the room. It would utilize the determined door path, calculated door position, and the room's wall points to accurately position the door. It also considers used space to avoid overlaps and ensure the door is placed in an available and appropriate location.

# Overall, these functions work together to ensure that door assets are placed accurately and appropriately within a room layout, respecting the room's walls, type, and available space.