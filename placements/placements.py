from utils import split_rooms
from placements.doors import door_asset_placement
from placements.livingroom import livingroom_asset_placement
from placements.bedroom import bedroom_asset_placement
from placements.balcony import balcony_asset_placement
from placements.bathroom import bathroom_asset_placement
from placements.kitchen import kitchen_asset_placement

def placements(image, walls, exterior_walls, data, room_to_doors):
    rooms = split_rooms(walls)

    for rm_idx, room in enumerate(rooms):
        room_type = data["types"][rm_idx]
        used_space = []

        if room_type==0: # Living Room
            door_asset_placement(image, exterior_walls, room_type, data, [0], used_space)
            livingroom_asset_placement(image, room, data, used_space)
        elif room_type in [1,5,7,8]: # Matser Room + Rooms
            door_asset_placement(image, room, room_type, data, room_to_doors[rm_idx], used_space)
            bedroom_asset_placement(image, room, data, used_space)
        elif room_type==2: # Kitchen
            door_asset_placement(image, room, room_type, data, room_to_doors[rm_idx], used_space)
            kitchen_asset_placement(image, room, room_type, data, used_space)
        elif room_type==3: # Bathroom
            door_asset_placement(image, room, room_type, data, room_to_doors[rm_idx], used_space)
            bathroom_asset_placement(image, room, room_type, data, used_space)
        elif room_type==4: # Dining Room
            door_asset_placement(image, room, room_type, data, room_to_doors[rm_idx], used_space)
        elif room_type==6: # Study Room
            door_asset_placement(image, room, room_type, data, room_to_doors[rm_idx], used_space)
        elif room_type==9: # Balcony
            door_asset_placement(image, room, room_type, data, room_to_doors[rm_idx], used_space)
            balcony_asset_placement(image, room, data, used_space)
        elif room_type==10: # Entrance Room
            door_asset_placement(image, room, room_type, data, room_to_doors[rm_idx], used_space)
        elif room_type==11: # Storage Room
            door_asset_placement(image, room, room_type, data, room_to_doors[rm_idx], used_space)





# The provided code snippet sets up the necessary imports and the beginning of a function named `placements` designed to handle the placement of various assets (such as doors, beds, sofas, balconies, and bathroom fixtures) within a room layout. Here is a detailed summary of the code:

# The function starts by importing several modules and functions necessary for its operation. These include `split_rooms` from the `utils` module and several asset placement functions (`door_asset_placement`, `bed_asset_placement`, `sofa_asset_placement`, `balcony_asset_placement`, `bathroom_asset_placement`) from their respective modules within the `placements` package. These imports suggest that the `placements` function will utilize these tools to place different assets in various rooms.

# The `placements` function is defined to take five parameters: `image`, `walls`, `exterior_walls`, `data`, and `room_to_doors`. The `image` parameter likely refers to an SVG or other graphical representation of the floor plan. The `walls` and `exterior_walls` parameters represent the interior and exterior boundaries of the rooms. The `data` parameter is expected to contain relevant information about the objects to be placed, such as dimensions and positions. The `room_to_doors` parameter probably maps each room to its associated doors, aiding in the accurate placement of door assets.

# Though the provided snippet does not include the complete function body, it is clear that the `placements` function will call the imported asset placement functions to arrange various objects within the room layout. By organizing these elements, the function aims to create a coherent and functional interior design for the rooms depicted in the `image`.

# In summary, the `placements` function is a high-level orchestrator that leverages specialized placement functions to arrange different assets within a room layout, ensuring that all objects are positioned correctly and efficiently based on the provided data and room boundaries.