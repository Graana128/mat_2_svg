from shapely.geometry import Point, Polygon
from utils import split_rooms, find_largest_walls
from annot_data import annotation_dict

def place_info_text(image):
    labels = {
    'LR': "Living Room",
    'MR': "Master Room",
    'Ki': "Kitchen",
    'Ba': "Bathroom",
    'Be': "Bedroom",
    'Bl': "Balcony"
    }

    initial_y = 35
    
    for i, (key, value) in enumerate(labels.items()):
        text = f'{key}: {value}'
        text_x = 850
        text_y = initial_y + (i * 50)

        image.add(image.text(
            text,
            insert=(int(text_x), int(text_y)),
            font_size=28,
            font_family="Helvetica",
            fill='black'
        ))
        

def place_text_inside_room(image, room, text_X, text_Y, text):
    image.add(image.text(
        text,
        insert=(int(text_X), int(text_Y)),
        font_size=18,
        font_family="Helvetica",
        fill='black'
    ))

    # size = 28

    # image.add(image.rect(insert=(int(text_X-1), int(text_Y-size+1)), size=(f"{size}px", f"{size}px"), fill='white'))

def annotate(image, all_rooms, room_types):
    rooms = split_rooms(all_rooms, None)
    text_size = 28
    padding = 5

    for room_idx, room in enumerate(rooms):
        isPlaced = False
        polygon_points = [edge[0] for edge in room]
        horizontal_wall, vertical_wall = find_largest_walls(room)
        text = annotation_dict[room_types[room_idx]]
        
        text_x = (horizontal_wall[0][0]+horizontal_wall[1][0]) // 2
        text_y = (vertical_wall[0][1]+vertical_wall[1][1]) // 2
        
        points = [[text_x-padding, text_y+padding], [text_x+text_size+padding, text_y+padding], [text_x-padding, text_y-text_size-padding], [[text_x+text_size+padding, text_y-text_size-padding]]]
        if all(Polygon(polygon_points).contains(Point(point)) for point in points):
            place_text_inside_room(image, room, text_x, text_y, text)
            continue


        for y in range(text_y-40, text_y+40):
            for x in range(text_x-40, text_x+40):
                points = [[x-padding, y+padding], [x+text_size+padding, y+padding], [x-padding, y-text_size-padding], [[x+text_size+padding, y-text_size-padding]]]
                if all(Polygon(polygon_points).contains(Point(point)) for point in points):
                    place_text_inside_room(image, room, x, y, text)
                    isPlaced = True
                    break
            if isPlaced:
                break

        if not isPlaced:
            place_text_inside_room(image, room, text_x, text_y, text)