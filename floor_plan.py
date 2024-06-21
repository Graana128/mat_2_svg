import svgwrite
from glob import glob

from utils import *
from annot_data import *
from placements.utils import find_direction
from placements.placements import placements

class FloorplanGenerator:
    def __init__(self, mat_data, output_file="output.svg"):
        self.data = mat_data
        self.image_size = 1080

        self.image = svgwrite.Drawing(output_file, size=(f"{self.image_size}px", f"{self.image_size}px"), profile="tiny")
        self.image.add(self.image.rect(insert=(0, 0), size=(f"{self.image_size}px", f"{self.image_size}px"), fill='white'))

    def get_interior_walls(self):
        interior_walls = []

        for rooms in self.data["walls"]:
            for i, point in enumerate(rooms):
                point1 = point
                point2 = rooms[0] if i==len(rooms)-1 else rooms[i+1]
                interior_walls.append([point1, point2])

            interior_walls.append(None)

        return interior_walls

    def get_exterior_walls(self):
        exteriorWalls, exterior_walls = self.data["exterior_walls"], []
        
        for i, wall in enumerate(exteriorWalls):
            point1 = wall[:2]
            point2 = exteriorWalls[0][:2] if i == len(exteriorWalls)-1 else exteriorWalls[i+1][:2]
            exterior_walls.append([point1, point2])

        return exterior_walls

    def draw_exterior_walls(self, exterior_walls):
        points = [wall[0] for wall in exterior_walls]
        self.image.add(self.image.polygon(points, fill='none', stroke='black', stroke_width=9))

    def draw_interior_walls(self, walls):
        rooms = split_rooms(walls, None)
        room_types = self.data["types"]

        for i, room in enumerate(rooms):
            points = [tuple(map(int, wall[0])) for wall in room]
            room_color = svgwrite.rgb(*monochrome_colors[room_types[i]])
            self.image.add(self.image.polygon(points, fill=room_color, stroke='black', stroke_width=9))
    
    def draw_windows(self, exterior_walls, windows_indices):
        pad = 3
        stroke_width = 3
        color = svgwrite.rgb(255,255,255)
        # color = "gray" 

        for idx, window in enumerate(self.data["windows"]):
            _, x, y, w, h, _ = window
            direction = find_direction(exterior_walls, windows_indices[idx])
            start_point, end_point = [x, y], [x+w, y+h]
 
            if w == 0:
                if direction == "West":
                    start_point[0] += pad
                    end_point[0] += pad
                    self.image.add(self.image.line(start=start_point, end=end_point, stroke=color, stroke_width=stroke_width))
                    
                    start_point[0] -= pad*2
                    end_point[0] -= pad*2
                    self.image.add(self.image.line(start=start_point, end=end_point, stroke=color, stroke_width=stroke_width))
                else: # East
                    start_point[0] -= pad
                    end_point[0] -= pad
                    self.image.add(self.image.line(start=start_point, end=end_point, stroke=color, stroke_width=stroke_width))
                    
                    start_point[0] += pad*2
                    end_point[0] += pad*2
                    self.image.add(self.image.line(start=start_point, end=end_point, stroke=color, stroke_width=stroke_width))
            elif h == 0:
                if direction == "North":
                    start_point[1] += pad
                    end_point[1] += pad
                    self.image.add(self.image.line(start=start_point, end=end_point, stroke=color, stroke_width=stroke_width))
                    
                    start_point[1] -= pad*2
                    end_point[1] -= pad*2
                    self.image.add(self.image.line(start=start_point, end=end_point, stroke=color, stroke_width=stroke_width))
                else: # South
                    start_point[1] -= pad
                    end_point[1] -= pad 
                    self.image.add(self.image.line(start=start_point, end=end_point, stroke=color, stroke_width=stroke_width))
                    
                    start_point[1] += pad*2
                    end_point[1] += pad*2
                    self.image.add(self.image.line(start=start_point, end=end_point, stroke=color, stroke_width=stroke_width))
            else:
                continue

    def draw_door_edges(self, room_to_doors, exterior_walls):
        for key, indices in room_to_doors.items():
            room_type = self.data["types"][key]

            door = self.data["doors"][indices[0]]
            start_point = door[1:3]
            end_point = [door[1]+door[3], door[2]+door[4]]

            door_edge_color = svgwrite.rgb(*monochrome_colors[room_type])
            self.image.add(self.image.line(start=tuple(map(int, start_point)), end=tuple(map(int, end_point)), stroke=door_edge_color, stroke_width=9))

        start_point = exterior_walls[0][0]
        end_point = exterior_walls[0][1]
        color = svgwrite.rgb(*monochrome_colors[0])
        self.image.add(self.image.line(start=tuple(map(int, start_point)), end=tuple(map(int, end_point)), stroke=color, stroke_width=9))

    def draw_doors(self, walls, exterior_walls):
        room_to_doors = dict()
        rooms = split_rooms(walls, None)

        # finding door indices for each room
        for rm_idx, room in enumerate(rooms):
            if self.data["types"][rm_idx] != 0: # skip livingroom
                indices = get_object_indices(room, self.data["doors"], isMultiple=True)
                room_to_doors[rm_idx] = indices

        room_to_doors = remove_duplicate_objects(room_to_doors)
        self.draw_door_edges(room_to_doors, exterior_walls)

        return room_to_doors
        
    def draw(self):
        # getting relevant data for drawing
        walls = self.get_interior_walls()
        exterior_walls = self.get_exterior_walls()

        door_indices = get_object_indices(walls, self.data["doors"])
        windows_indices = get_object_indices(exterior_walls, self.data["windows"])
        
        # scaling vectors
        walls = scale_walls(walls, 4)
        exterior_walls = scale_walls(exterior_walls, 4)

        self.data["doors"] = scale_objects(walls, self.data["doors"], door_indices, 4)
        self.data["windows"] = scale_objects(exterior_walls, self.data["windows"], windows_indices, 4)
        
        # drawing vectors
        self.draw_interior_walls(walls)
        self.draw_exterior_walls(exterior_walls)
        self.draw_windows(exterior_walls, windows_indices)
        room_to_doors = self.draw_doors(walls, exterior_walls)

        # asset placements
        placements(self.image, walls, exterior_walls, self.data, room_to_doors)

        # saving vectors
        self.image.save()

if __name__ == "__main__":
    mat_files_paths = glob("data/*.mat")

    i = 0
    print(mat_files_paths, mat_files_paths[i])
    mat_data = load_matlab_file(mat_files_paths[i])

    floor_plan = FloorplanGenerator(mat_data)
    floor_plan.draw()





# The provided code defines a `FloorplanGenerator` class designed to create a floorplan drawing from MATLAB data, and it outputs this drawing as an SVG file. The class is initialized with MATLAB data and sets up an SVG drawing canvas, specifying the size and background color. The initialization function, `__init__`, also takes an optional parameter for the output file name, defaulting to "output.svg".

# The class has methods to process walls, both interior and exterior. The `get_interior_walls` method extracts the interior walls from the data, looping through each room's points to form wall segments. Similarly, the `get_exterior_walls` method extracts the exterior walls, ensuring to connect the points to form continuous wall segments around the exterior of the building.

# Drawing methods form a significant part of the class. The `draw_exterior_walls` method draws the exterior walls as a polygon on the SVG canvas, setting the stroke and stroke width for visibility. The `draw_interior_walls` method handles the drawing of interior walls, where each room is filled with a color based on its type, and the walls are outlined with a stroke. The `draw_windows` method is responsible for drawing windows on the exterior walls, adjusting their position based on the wall's orientation (North, South, East, West).

# Doors are managed through two methods: `draw_door_edges` and `draw_doors`. The `draw_door_edges` method draws the edges of doors for each room and the exterior walls, using the room type to determine the door edge color. The `draw_doors` method first identifies door locations for each room and then calls `draw_door_edges` to render them.

# The primary drawing process is coordinated by the `draw` method. This method retrieves interior and exterior walls, determines door and window indices, scales the wall and object data for better visualization, and calls the respective drawing methods for walls, windows, and doors. It also invokes the `placements` function to add additional assets to the floorplan, and finally, it saves the completed SVG image.

# The main execution block of the script loads MATLAB files and initializes the `FloorplanGenerator` with the data from the first file. It then calls the `draw` method to generate the floorplan. The script uses several supporting functions and constants, such as `split_rooms`, `get_object_indices`, `scale_walls`, `scale_objects`, and `remove_duplicate_objects`, to aid in the processing and scaling of data. The `monochrome_colors` constant provides color mapping for different room types, while the `find_direction` function determines the direction of windows relative to walls. The `placements` function, imported from `placements.placements`, is used to place additional assets on the floorplan.

# Overall, this class effectively transforms data from a MATLAB file into a visual floorplan representation using SVG, allowing for clear and scalable visualization of architectural layouts.