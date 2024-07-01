import math
from shapely.geometry import Point, Polygon


def get_wall_index(room, objects, largest=False):
    largest_object, largest_idx = 0, None

    for object in objects:
        object_direction = "Y" if object[3] == 0 else "X"
        object_static = object[1] if object[3] == 0 else object[2]
        object_dynamic = object[2] if object[3] == 0 else object[1]
        object_length = object[4] if object[3] == 0 else object[3]

        for index, wall in enumerate(room):
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
                    if not largest:
                        return index
                    else:
                        if object_length >= largest_object:
                            largest_object = object_length
                            largest_idx = index

    if largest:
        return largest_idx
                                
def get_wall_indices(room, doors):
    door_wall_index = get_wall_index(room, doors)
    left_wall_index = door_wall_index+1 if door_wall_index!=3 else 0
    right_wall_index = door_wall_index-1 if door_wall_index!=0 else 3
    
    avg_index = (left_wall_index+right_wall_index)//2
    if door_wall_index==avg_index:
        front_wall_index = 3 if avg_index==1 else 0
    else:
        front_wall_index = avg_index

    return door_wall_index, front_wall_index, left_wall_index, right_wall_index

def point_in_polygon(polygon, point):
    return Polygon(polygon).contains(Point(point))

def find_direction(walls, index):
    # Create the polygon points from the edges
    polygon_points = [point for edge in walls for point in edge]
    polygon = Polygon(polygon_points)

    wall = walls[index]
    x1, y1 = wall[0]
    x2, y2 = wall[1]
    
    if x1 == x2:  # Vertical wall
        center_x = x1
        center_y = (y1 + y2) / 2
        
        # Check left (west) and right (east) of the center point
        if point_in_polygon(polygon, (center_x - 1, center_y)):
            return "West"
        elif point_in_polygon(polygon, (center_x + 1, center_y)):
            return "East"
    
    elif y1 == y2:  # Horizontal wall
        center_x = (x1 + x2) / 2
        center_y = y1
        
        # Check above (north) and below (south) of the center point
        if point_in_polygon(polygon, (center_x, center_y - 1)):
            return "North"
        elif point_in_polygon(polygon, (center_x, center_y + 1)):
            return "South"

def calculate_distance(p1, p2):
    distance = math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    return distance

def find_direction(walls, index):
    polygon_points = [point for edge in walls for point in edge]
    polygon = Polygon(polygon_points)

    wall = walls[index]
    x1, y1 = wall[0]
    x2, y2 = wall[1]
    
    if x1 == x2:  # Vertical wall
        center_x = x1
        center_y = (y1 + y2) / 2
        
        # Check left (west) and right (east) of the center point
        if point_in_polygon(polygon, (center_x - 1, center_y)):
            return "West"
        elif point_in_polygon(polygon, (center_x + 1, center_y)):
            return "East"
    
    elif y1 == y2:  # Horizontal wall
        center_x = (x1 + x2) / 2
        center_y = y1
        
        # Check above (north) and below (south) of the center point
        if point_in_polygon(polygon, (center_x, center_y - 1)):
            return "North"
        elif point_in_polygon(polygon, (center_x, center_y + 1)):
            return "South"

def change_orientation(current_direction, desired_direction):
    direction_map = {
        ('North', 'East'): 90,
        ('North', 'South'): 180,
        ('North', 'West'): -90,
        
        ('East', 'South'): 90,
        ('East', 'West'): 180,
        ('East', 'North'): -90,
        
        ('South', 'West'): 90,
        ('South', 'North'): 180,
        ('South', 'East'): -90,

        ('West', 'North'): 90,
        ('West', 'East'): 180,
        ('West', 'South'): -90,
    }

    angle = direction_map.get((current_direction, desired_direction), 0)
    return angle if angle >= 0 else angle + 360

def is_point_inside_polygon(polygon, point):
    """
    Determine if the point is inside the polygon using ray-casting algorithm.
    """
    x, y = point
    inside = False

    n = len(polygon)
    p1x, p1y = polygon[0]
    for i in range(n+1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside

def isValidPoint(points, room, used_space):
    asset_center_point = [abs(points[0][0]-points[-1][0])//2, abs(points[0][1]-points[-1][1])//2]

    # checking if asset intersect with existing points
    for point in used_space:
        us_center_point = [abs(point[0][0]-point[1][0])//2, abs(point[0][1]-point[1][1])//2]
        if any(is_point_inside_rectangle(asset_point, *point) for asset_point in points):
            return False
        if any(is_point_inside_rectangle(us_point, points[0], points[3]) for us_point in point):
            return False
        if is_point_inside_rectangle(asset_center_point, *point):
            return False
        if is_point_inside_rectangle(us_center_point, points[0], points[3]):
            return False

    polygon_points = [edge[0] for edge in room]
    result = [point_in_polygon(polygon_points, asset_point) for asset_point in points]
    if all(result):
        return True
    
    return False

def is_point_inside_rectangle(point, upper_left, bottom_right):
    x, y = point
    ul_x, ul_y = upper_left
    br_x, br_y = bottom_right

    return ul_x <= x <= br_x and ul_y <= y <= br_y

def sort_corners(corner_points, doors):
    sorted_corners = dict()

    for point in corner_points:
        distances = []
        for door in doors:
            if len(door) < 5:
                print(f"Invalid door data: {door}")
                continue

            x, y, w, h = door[1:5]
            start_point = [x, y]
            end_point = [x + w, y + h]
            distances.append(calculate_distance(point, start_point))
            distances.append(calculate_distance(point, end_point))
        
        if not distances:
            print(f"No distances calculated for point: {point}")
            continue

        min_distance = min(distances)
        if min_distance >= 10:
            sorted_corners[tuple(point)] = min_distance

    return dict(sorted(sorted_corners.items(), key=lambda item: item[1], reverse=True))

def get_tuple_index(tuples_list, target_tuple):
    for index, (first_tuple, second_tuple) in enumerate(tuples_list):
        if (first_tuple[0] == target_tuple[0] and first_tuple[1] == target_tuple[1]) or (second_tuple[0] == target_tuple[0] and second_tuple[1] == target_tuple[1]):
            return index
    return -1





# The provided code includes a series of functions to support the placement and orientation of objects within a room based on wall and door positions. Here's a detailed summary of each function and its purpose:

# The `get_wall_index` function identifies the index of a wall within a room that aligns with the static and dynamic properties of the provided objects. It can return the first matching wall index or, if specified, the wall index corresponding to the largest object. It checks each wall's direction and compares it with the object's direction to find the appropriate wall.

# The `get_wall_indices` function determines the indices of walls relative to a given door. It calculates the indices for the door wall, front wall, left wall, and right wall by finding the door's wall index and adjusting accordingly. This helps in identifying the spatial relationship between walls and the door.

# The `point_in_polygon` function checks if a given point lies within a specified polygon using the Shapely library. This utility function is essential for verifying whether an object placement is valid within the room's boundaries.

# The `find_direction` function determines the direction (North, South, East, or West) of a wall based on its position relative to the polygon representing the room. It identifies the wall's center and checks adjacent points to determine if the wall is on the left (West), right (East), above (North), or below (South) within the polygon.

# The `calculate_distance` function computes the Euclidean distance between two points. This is useful for determining the proximity of objects to walls or other elements within the room.

# The `change_orientation` function calculates the rotation angle needed to align an object's current direction with the desired direction. It uses a mapping of direction changes to corresponding rotation angles, ensuring objects are correctly oriented.

# The `isValidPoint` function checks if a set of points (representing an object's placement) is valid within the room and not overlapping with used spaces. It ensures the points are within the room's polygon and not within any preoccupied space, maintaining proper placement without collision.

# Lastly, the `is_point_inside_rectangle` function (incomplete in the snippet) presumably checks if a point lies within a defined rectangular area, supporting collision detection and valid placement checks for objects.

# Together, these functions facilitate the accurate placement, orientation, and validation of objects (like furniture) within a room, ensuring they align with walls, doors, and other room elements while avoiding overlaps and maintaining spatial relationships.