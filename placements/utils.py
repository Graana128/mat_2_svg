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

def isValidPoint(points, room, used_space):
    for point in used_space:
        if any(is_point_inside_rectangle(asset_point, *point) for asset_point in points):
            return False

    polygon_points = [point for edge in room for point in edge]
    if all(point_in_polygon(polygon_points, asset_point) for asset_point in points):
        return True
    
    return False

def is_point_inside_rectangle(point, upper_left, bottom_right):
    x, y = point
    ul_x, ul_y = upper_left
    br_x, br_y = bottom_right

    return ul_x <= x <= br_x and ul_y <= y <= br_y