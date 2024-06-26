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
            font_size=28,
            font_family="Helvetica",
            fill='black'
        ))

def annotate(image, all_rooms, room_types):
    rooms = split_rooms(all_rooms, None)

    for room_idx, room in enumerate(rooms):
        horizontal_wall, vertical_wall = find_largest_walls(room)
        
        text_x = (horizontal_wall[0][0]+horizontal_wall[1][0]) // 2
        text_y = (vertical_wall[0][1]+vertical_wall[1][1]) // 2
        text = annotation_dict[room_types[room_idx]]

        place_text_inside_room(image, room, text_x, text_y, text)
