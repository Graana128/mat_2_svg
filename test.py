class Rectangle:
    def __init__(self, upper_left, width, height, orientation='horizontal'):
        self.upper_left = upper_left
        self.width = width
        self.height = height
        self.orientation = orientation
        self.update_corners()

    def update_corners(self):
        x, y = self.upper_left
        if self.orientation == 'horizontal':
            self.lower_right = (x + self.width, y + self.height)
        else:
            self.lower_right = (x + self.height, y + self.width)

    def rotate(self):
        if self.orientation == 'horizontal':
            self.orientation = 'vertical'
        else:
            self.orientation = 'horizontal'
        self.update_corners()

    def intersects(self, other):
        return not (self.lower_right[0] <= other.upper_left[0] or
                    self.upper_left[0] >= other.lower_right[0] or
                    self.lower_right[1] <= other.upper_left[1] or
                    self.upper_left[1] >= other.lower_right[1])


def is_within_polygon(rect, polygon):
    # Check if rectangle corners are within the polygon
    for point in [rect.upper_left, rect.lower_right]:
        if not (polygon[0][0] <= point[0] <= polygon[2][0] and
                polygon[0][1] <= point[1] <= polygon[2][1]):
            return False
    return True


def can_place_rectangle(rect, used_space, polygon, padding):
    if not is_within_polygon(rect, polygon):
        return False
    for used_rect in used_space:
        if rect.intersects(used_rect):
            return False
    return True


def fill_polygon_with_rectangles(polygon, rectangles, padding=1, allow_orientation_change=True):
    used_space = []

    for rect in rectangles:
        placed = False

        if can_place_rectangle(rect, used_space, polygon, padding):
            used_space.append(rect)
            placed = True
        elif allow_orientation_change:
            rect.rotate()
            if can_place_rectangle(rect, used_space, polygon, padding):
                used_space.append(rect)
                placed = True
        
        if not placed:
            # Discard rectangle if it cannot be placed
            continue

    return used_space


# Example Usage
polygon = [(0, 0), (0, 10), (10, 10), (10, 0)]  # Define the polygon vertices
rectangles = [
    Rectangle((0, 0), 3, 2),
    Rectangle((0, 0), 5, 2),
    Rectangle((0, 0), 1, 3),
    # Add more rectangles as needed
]

filled_space = fill_polygon_with_rectangles(polygon, rectangles, padding=1, allow_orientation_change=True)
for rect in filled_space:
    print(f"Placed rectangle at {rect.upper_left} with size ({rect.width}x{rect.height}) oriented {rect.orientation}")
