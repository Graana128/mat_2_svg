import scipy.io
import numpy as np

def load_matlab_file(file_path):
    mat_contents = scipy.io.loadmat(file_path)
    mat_contents = mat_contents["data"][0][0]

    def convert_to_int(nested_item):
        if isinstance(nested_item, list):
            return [convert_to_int(item) for item in nested_item]
        elif isinstance(nested_item, np.ndarray):
            return np.array([convert_to_int(item) for item in nested_item])
        elif isinstance(nested_item, float):
            return int(nested_item)
        elif isinstance(nested_item, int):
            return nested_item
        else:
            return nested_item

    mat_data = {
        "exterior_walls": convert_to_int(mat_contents[1].tolist()),
        "walls": convert_to_int(mat_contents[5][0].tolist()),
        "doors": convert_to_int(mat_contents[-2].tolist()),
        "windows": convert_to_int(mat_contents[-1].tolist()),
        "types": convert_to_int(mat_contents[-6][0].tolist())
    }

    return mat_data

def get_object_indices(walls, objects, isMultiple=False):
    object_single_indices, object_indices = [], []

    for object_idx, object in enumerate(objects):
        object_direction = "Y" if object[3] == 0 else "X"
        object_static = object[1] if object[3] == 0 else object[2]
        object_dynamic = object[2] if object[3] == 0 else object[1]
        object_length = object[4] if object[3] == 0 else object[3]

        wall_idx = 0
        for index, wall in enumerate(walls):
            if wall==None:
                wall_idx += 1
                continue
        
            if wall[0][0] == wall[1][0]:
                wall_static = wall[0][0]
                wall_min, wall_max = sorted([wall[0][1], wall[1][1]])
                wall_direction = "Y"
            else:
                wall_static = wall[0][1]
                wall_min, wall_max = sorted([wall[0][0], wall[1][0]])
                wall_direction = "X"

            if wall_direction == object_direction and object_static == wall_static:
                if wall_min <= object_dynamic <= wall_max and wall_min <= (object_dynamic+object_length) <= wall_max:
                    if isMultiple:
                        object_indices.append(object_idx)
                        continue
                    else:
                        object_single_indices.append(index)
                        break
    
    return object_indices if isMultiple else object_single_indices

def scale_walls(walls, scaling_factor=2):
    scaled_walls = []

    for wall in walls:
        if wall == None:
            scaled_walls.append(None)
            continue

        point1, point2 = wall
        point1 = [point*scaling_factor for point in point1]
        point2 = [point*scaling_factor for point in point2]

        if len(scaled_walls)!=0 and scaled_walls[-1]!=None:
            if point1[0]==point2[0]:
                point1[0] = point2[0] = scaled_walls[-1][1][0]
            else:
                point1[1] = point2[1] = scaled_walls[-1][1][1]

        scaled_walls.append([point1, point2])
    return scaled_walls

def scale_objects(walls, objects, object_indices, scaling_factor=2):
        for i, index in enumerate(object_indices):
            point1, point2 = walls[index]
            
            if point1[0]==point2[0]:
                objects[i][1] = point1[0]
                objects[i][2] = objects[i][2] * scaling_factor
                objects[i][4] = objects[i][4] * scaling_factor
            else:
                objects[i][2] = point1[1]
                objects[i][1] = objects[i][1] * scaling_factor
                objects[i][3] = objects[i][3] * scaling_factor

        return objects

def split_rooms(walls, sep=None):
    rooms = []
    room = []

    for wall in walls:
        if wall == sep:
            if room:
                rooms.append(room)
            room = []
        else:
            room.append(wall)
    if room:
        rooms.append(room)
    return rooms

def remove_duplicate_objects(objects):
    for key, value in objects.items():
        if len(value) >= 2:
            for key2, value2 in objects.items():
                if key != key2 and len(value2)==1 and value2[0] in value:
                    objects[key].remove(value2[0])

    return objects

def find_largest_walls(room):
    vertical_wall, vertical_dist = None, -1
    horizontal_wall, horiznotal_dist = None, -1

    for wall in room:
        if wall[0][0] == wall[1][0]:
            distance = abs(wall[0][1]-wall[1][1])
            if distance > vertical_dist:
                vertical_dist = distance
                vertical_wall = wall
        else:
            distance = abs(wall[0][0]-wall[1][0])
            if distance > horiznotal_dist:
                horiznotal_dist = distance
                horizontal_wall = wall
    
    return horizontal_wall, vertical_wall





# The provided code includes a set of utility functions designed to support the `FloorplanGenerator` class by loading MATLAB data and processing walls, doors, and windows for drawing a floorplan. 

# The `load_matlab_file` function is responsible for loading MATLAB data from a specified file path. It extracts and processes specific components of the data, such as exterior walls, interior walls, doors, windows, and room types. To ensure consistency, it uses a helper function `convert_to_int` that recursively converts nested structures from floating-point numbers to integers. This conversion helps in maintaining uniformity in the data types used in subsequent processing.

# The `get_object_indices` function determines the indices of objects, such as doors or windows, that align with the given wall segments. For each object, the function calculates its orientation and position to match it with a corresponding wall segment. Depending on the `isMultiple` flag, it returns either single or multiple indices. This function is crucial for identifying the precise location of objects relative to walls, which is essential for accurate placement in the floorplan.

# Scaling functions play a significant role in adjusting the size and position of walls and objects. The `scale_walls` function scales wall coordinates by a specified factor. It ensures wall continuity by adjusting the coordinates of subsequent walls to match the ending point of the previous wall, thus maintaining the integrity of the wall structure. Similarly, the `scale_objects` function scales the coordinates and dimensions of objects based on the corresponding wall segments. It adjusts the object's position and size according to the scaling factor, ensuring that objects are proportionately resized and correctly positioned.

# To organize the walls into separate rooms, the `split_rooms` function splits the list of walls using a specified separator. It returns a list of rooms, where each room is represented by a list of walls. This function helps in structuring the floorplan into distinct areas, making it easier to manage and visualize. Additionally, the `remove_duplicate_objects` function removes duplicate object indices from a dictionary, ensuring that objects are uniquely associated with the correct room or wall segment. This step is important to avoid redundancy and to ensure that each object is correctly placed within the floorplan.

# Overall, these utility functions facilitate the processing and visualization of architectural data by converting, scaling, and organizing the information necessary for the `FloorplanGenerator` to create accurate and visually consistent floorplans.