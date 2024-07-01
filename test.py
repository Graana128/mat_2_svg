from shapely.geometry import Polygon, MultiPolygon

def subtract_polygons(main_coords, subtractor_coords):
    # Convert list of coordinates into Polygon objects
    main_polygon = Polygon(main_coords)
    subtractor_polygon = Polygon(subtractor_coords)
    
    # Calculate the difference between the main polygon and the subtractor polygon
    result = main_polygon.difference(subtractor_polygon)
    
    # Check if the result is a MultiPolygon or a single Polygon
    if isinstance(result, MultiPolygon):
        return [list(poly.exterior.coords) for poly in result.geoms]
    elif isinstance(result, Polygon):
        return [list(result.exterior.coords)]
    else:
        return []  # No polygon to return if the difference is empty or not a polygon

# Example coordinates for the polygons
main_polygon_coords = [(5, 5), (22, 5), (22, 13), (5, 13)]
subtractor_polygon_coords = [(10, 10), (15, 10), (15, 5), (18, 5), (18, 15), (20, 15), (20, 10), (30, 10), (30, 30), (10, 30)]

# Calculating the resultant polygons after subtraction
resultant_polygons = subtract_polygons(main_polygon_coords, subtractor_polygon_coords)

for i, polygon in enumerate(resultant_polygons, 1):
    print(f"Resultant Polygon {i} Coordinates:", polygon)
