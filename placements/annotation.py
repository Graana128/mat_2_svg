import svgwrite
from shapely.geometry import Point, Polygon
from utils import split_rooms, find_largest_walls
from PIL import Image, ImageDraw, ImageFont
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

def annotate(image, all_rooms, room_types):
    rooms = split_rooms(all_rooms, None)
    text_size1, text_size2 = 28, 28
    padding = 5

    for room_idx, room in enumerate(rooms):
        isPlaced = False
        polygon_points = [edge[0] for edge in room]
        horizontal_wall, vertical_wall = find_largest_walls(room)
        text = annotation_dict[room_types[room_idx]]
        
        text_x = (horizontal_wall[0][0]+horizontal_wall[1][0]) // 2
        text_y = (vertical_wall[0][1]+vertical_wall[1][1]) // 2
        
        points = [[text_x-padding, text_y+padding], [text_x+text_size1+padding, text_y+padding], [text_x-padding, text_y-text_size2-padding], [[text_x+text_size1+padding, text_y-text_size2-padding]]]
        if all(Polygon(polygon_points).contains(Point(point)) for point in points):
            place_text_inside_room(image, room, text_x, text_y, text)
            continue


        threshold = 40
        for y in range(text_y-threshold, text_y+threshold):
            for x in range(text_x-threshold, text_x+threshold):
                points = [[x-padding, y+padding], [x+text_size1+padding, y+padding], [x-padding, y-text_size1-padding], [[x+text_size1+padding, y-text_size2-padding]]]
                if all(Polygon(polygon_points).contains(Point(point)) for point in points):
                    place_text_inside_room(image, room, x, y, text)
                    isPlaced = True
                    break
            if isPlaced:
                break

        if not isPlaced:
            place_text_inside_room(image, room, text_x, text_y, text)




# def annotate(image, all_rooms, room_types):
#     rooms = split_rooms(all_rooms, None)
#     initial_text_size = 20
#     padding = 5

#     def calculate_max_text_size(polygon, text, padding):
#         max_width = polygon.bounds[2] - polygon.bounds[0] - 2 * padding
#         max_height = polygon.bounds[3] - polygon.bounds[1] - 2 * padding
#         max_text_size = initial_text_size

#         while max_text_size > 1:
#             # points = [[text_x-padding, text_y+padding], [text_x+max_width+padding, text_y+padding], [text_x-padding, text_y-max_height-padding], [[text_x+max_width+padding, text_y-max_height-padding]]]
#             # if all(Polygon(polygon_points).contains(Point(point)) for point in points):
#             #     print("yes")
#             #     break
#             print("oyuet")
            
#             # Approximate width and height of the text
#             text_width = len(text) * max_text_size * 0.9  # Adjust this factor as needed
#             text_height = max_text_size

#             if text_width <= max_width and text_height <= max_height:
#                 return max_text_size
#             max_text_size -= 1

#         return max_text_size

#     def place_text_inside_room(image, room, text_x, text_y, text, text_size):
#         # Convert text size to points (assuming 1 text_size unit = 1 point)
#         font_size = text_size
#         # Manually estimate the bounding box for centering the text
#         text_width = len(text) * text_size * 0.5
#         text_height = text_size
#         adjusted_x = text_x - text_width / 2
#         adjusted_y = text_y + text_height / 2  # SVG text uses the baseline for y coordinate
#         image.add(image.text(text, insert=(adjusted_x, adjusted_y), font_size=font_size, fill="black"))

#     for room_idx, room in enumerate(rooms):
#         isPlaced = False
#         polygon_points = [edge[0] for edge in room]
#         polygon = Polygon(polygon_points)
#         horizontal_wall, vertical_wall = find_largest_walls(room)
#         text = annotation_dict[room_types[room_idx]]
        
#         text_x = (horizontal_wall[0][0] + horizontal_wall[1][0]) // 2
#         text_y = (vertical_wall[0][1] + vertical_wall[1][1]) // 2
        
#         max_text_size = calculate_max_text_size(polygon, text, padding)

#         if max_text_size > 1:
#             place_text_inside_room(image, room, text_x, text_y, text, max_text_size)
#             continue

#         for y in range(text_y - 40, text_y + 40):
#             for x in range(text_x - 40, text_x + 40):
#                 max_text_size = calculate_max_text_size(polygon, text, padding)
#                 if max_text_size > 1:
#                     place_text_inside_room(image, room, x, y, text, max_text_size)
#                     isPlaced = True
#                     break
#             if isPlaced:
#                 break

#         if not isPlaced:
#             max_text_size = calculate_max_text_size(polygon, text, padding)
#             place_text_inside_room(image, room, text_x, text_y, text, max_text_size)