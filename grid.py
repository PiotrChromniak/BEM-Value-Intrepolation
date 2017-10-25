import ranges as rg

def generate_ranges(points, elements):

  ranges = []
  for element in elements:
    (p1, p2, p3) = (points[element[0]], 
                    points[element[1]], 
                    points[element[2]])
    
    on_the_same_side = (p1[0] > p2[0] and p3[0] > p2[0]) or (p1[0] < p2[0] and p3[0] < p2[0])

    if on_the_same_side:
      ranges.append(rg.OrthogonalRange([p1, p2, p3]))
    else:
      ranges.append(rg.StandardRange([p1, p2, p3]))
    
  return ranges

def find_grid_borders(points):
  max_x = points[0][0]
  min_x = points[0][0]
  max_y = points[0][1]
  min_y = points[0][1]

  for point in points[1:]:
    max_x = max(max_x, point[0])
    min_x = min(min_x, point[0])
    max_y = max(max_y, point[1])
    min_y = min(min_y, point[1])

  return { 'min_x': min_x, 'max_x': max_x, 'min_y': min_y, 'max_y': max_y }

def generate_grid_points(ranges, grid_density, grid_borders):
  (min_x, max_x, min_y, max_y) = (grid_borders['min_x'], grid_borders['max_x'], 
                                  grid_borders['min_y'], grid_borders['max_y'])

  dx = (max_x - min_x) / grid_density
  y_density = int((max_y - min_y) / dx)

  points = []
  for i in range(grid_density):
    current_x = min_x + dx/2 + i * dx
    for j in range(y_density):
      current_y = min_y + dx/2 + j * dx
      
      valid_ranges = [f_range for f_range in ranges if f_range.is_in_range(current_x)]
      intersection_count = sum([f_range.get_intersections_count(current_x, current_y) for f_range in valid_ranges])
      if intersection_count % 2 is 1:
        points.append([current_x, current_y])
        
  return points

def split_points(points, elements):
  pass

'''
#przykład
import math
a = 0.785398163397
r = 5
points = [[math.cos(i*a) * r, math.sin(i*a) * r] for i in range(8)]
elements = [[7,0,1],
            [3,4,5],
            [5,6,7],
            [1,2,3]]

ranges = generate_ranges(points, elements)
borders = find_grid_borders(points)
grid_points = generate_grid_points(ranges,10,borders)

for point in grid_points:
  print("r: {0}".format(math.sqrt(point[0]**2 + point[1]**2)))
'''