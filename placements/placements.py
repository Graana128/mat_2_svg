from utils import split_rooms
from placements.doors import door_asset_placement
from placements.bed import bed_asset_placement
from placements.sofa import sofa_asset_placement
from placements.balcony import balcony_asset_placement
from placements.bathroom import bathroom_asset_placement

def placements(image, walls, exterior_walls, data, room_to_doors):
    rooms = split_rooms(walls)

    for rm_idx, room in enumerate(rooms):
        room_type = data["types"][rm_idx]
        used_space = []

        if room_type==0: # Living Room
            door_asset_placement(image, exterior_walls, room_type, data, [0], used_space)
            sofa_asset_placement(image, exterior_walls, rooms, data, used_space)
        elif room_type in [1,5,7,8]: # Matser Room + Rooms
            door_asset_placement(image, room, room_type, data, room_to_doors[rm_idx], used_space)
            bed_asset_placement(image, room, data, used_space)
        elif room_type==2: # Kitchen
            door_asset_placement(image, room, room_type, data, room_to_doors[rm_idx], used_space)
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