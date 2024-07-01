room_dict = {
    0: 'LivingRoom',
    1: 'MasterRoom',
    2: 'Kitchen',
    3: 'Bathroom',
    4: 'BedRoom',
    5: 'BedRoom',
    6: 'BedRoom',
    7: 'BedRoom',
    8: 'BedRoom',
    9: 'Balcony',
    10: 'Entrance',
    11: 'Storage',
    12: 'Wall-in',
    13: 'External',
    14: 'ExteriorWall',
    15: 'FrontDoor',
    16: 'InteriorWall',
    17: 'InteriorDoor'
}

inverse_room_dict = {
    'LivingRoom': 0,
    'MasterRoom': 1,
    'Kitchen': 2,
    'Bathroom': 3,
    'DiningRoom': 4,
    'ChildRoom': 5,
    'StudyRoom': 6,
    'SecondRoom': 7,
    'GuestRoom': 8,
    'Balcony': 9,
    'Entrance': 10,
    'Storage': 11,
    'Wall-in': 12,
    'External': 13,
    'ExteriorWall': 14,
    'FrontDoor': 15,
    'InteriorWall': 16,
    'InteriorDoor': 17
}

monochrome_colors = {
    0: (150, 150, 150),
    1: (157, 157, 157),
    2: (164, 164, 164),
    3: (171, 171, 171),
    4: (178, 178, 178),
    5: (185, 185, 185),
    6: (192, 192, 192),
    7: (199, 199, 199),
    8: (206, 206, 206),
    9: (213, 213, 213),
    10: (220, 220, 220),
    11: (227, 227, 227),
    12: (234, 234, 234),
    13: (240, 240, 240),
    14: (240, 240, 240),
    15: (240, 240, 240)
}

directions = {
    "bed.svg": "South",
    "right_door.svg": "South",
    "left_door.svg": "South",
    "double_door.svg": "North",
    "sliding_door.svg": "North",
    "sofa.svg": "North",
    "coffetable.svg": "South",
    "toilet.svg": "South",
    "sink.svg": "South",
    "shower.svg": "South",
    "stove.svg": "South",
    "TV.svg": "South",
    "kitchen-sink.svg": "South",
    "fridge.svg": "East",
    "dish-washer.svg": "South",
    "closet.svg": "South",
    "dinning-table.svg": "North",
    "closet_vert.svg": "West",
}

dimensions = {
    "bed.svg": (200, 200), # random
    "right_door.svg": (303, 320),
    "left_door.svg": (485, 514),
    "double_door.svg": (508, 250),
    "sliding_door.svg": (798, 57),
}

room_assets = {
    0: ["door", "LivingRoom", "sofa", "TV", "chairs", "table"],
    1: ["door", "MasterRoom", "bed", "wardrobe", "dressing table"],
    2: ["door", "Kitchen", "stove", "counter", "sink", "fridge", "cabinets"],
    3: ["door", "Bathroom", "shower", "toilet", "sink", "mirror", "cabinet"],
    4: ["door", "BedRoom", "bed", "wardrobe", "desk"],
    5: ["door", "BedRoom", "bed", "wardrobe", "desk"],
    6: ["door", "BedRoom", "bed", "wardrobe", "desk"],
    7: ["door", "BedRoom", "bed", "wardrobe", "desk"],
    8: ["door", "BedRoom", "bed", "wardrobe", "desk"],
    9: ["door", "Balcony", "chair", "table", "plant", "grill"],
    10: ["door", "Entrance", "welcome mat", "coat rack", "shoe rack"],
    11: ["door", "Storage", "shelves", "boxes", "tools"],
    12: ["door", "Walk-in", "clothes rack", "shoe rack", "mirror"]
}

# annotation_dict = {
#     0: 'LivingRoom',
#     1: 'MasterRoom',
#     2: 'Kitchen',
#     3: 'BathRoom',
#     4: 'BedRoom',
#     5: 'BedRoom',
#     6: 'BedRoom',
#     7: 'BedRoom',
#     8: 'BedRoom',
#     9: 'Balcony',
#     10: 'Entrance',
#     11: 'Storage',
#     12: 'Wall-in',
#     13: 'External',
#     14: 'ExteriorWall',
#     15: 'FrontDoor',
#     16: 'InteriorWall',
#     17: 'InteriorDoor'
# }


annotation_dict = {
    0: 'LR',
    1: 'MR',
    2: 'Kc',
    3: 'Bt',
    4: 'BR',
    5: 'BR',
    6: 'BR',
    7: 'BR',
    8: 'BR',
    9: 'Bl',
    10: 'En',
    11: 'St',
    12: 'WI',
    13: 'External',
    14: 'ExteriorWall',
    15: 'FrontDoor',
    16: 'InteriorWall',
    17: 'InteriorDoor'
}