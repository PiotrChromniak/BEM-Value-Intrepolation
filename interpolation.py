from math import (hypot, isclose)
import numpy as np
import grid

def interpolate(results, grid_density, p=2):
    (points, elements) = (results['points'], results['elements'])

    ranges = grid.generate_ranges(points, elements)
    borders = grid.find_grid_borders(points)
    generated_points = grid.generate_grid_points(ranges, grid_density, borders)
    dx = (borders['max_x'] - borders['min_x']) / grid_density
    interpolated_vals = interpolate_values(generated_points, results, dx, p)
    return { 'points': generated_points, 'values': interpolated_vals }     

def interpolate_values(new_points, data, grid_dx, p):
    basic_values = [
                    data['Sxx'], data['Syy'], data['Sxy'],
                    data['UX'], data['UY']
                    ]
    internal_values = [
                        data['inSxx'], data['inSyy'], data['inSxy'],
                        data['inUX'], data['inUY']
                      ] if data['internal_points'] else None
    points = data['points']
    internal_points = data['internal_points'] if internal_values else None

    results = [[], [], [], [], []]
    for x in new_points:
        weights = [ calculate_weight(x, xi, p) for xi in points ]
        indices = None
        internal_weights = None
        if internal_points:
            indices = get_point_indices_in_proximity(x, internal_points, grid_dx)
            internal_weights = [calculate_weight(x, internal_points[idx], p) for idx in indices]
        
        for j, (basic_vals, result) in enumerate(zip(basic_values, results)):
            nominator = np.dot(weights, basic_vals)
            denominator = sum(weights)
            if internal_points:
                denominator += sum(internal_weights)
                for idx, weight in zip(indices, internal_weights):
                    nominator += internal_values[j][idx] * weight
            result.append(nominator/denominator)

    return { 'Sxx': results[0], 'Syy': results[1], 
             'Sxy': results[2], 'UX': results[3], 
             'UY': results[4] }

def calculate_weight(x, xi, p):
    denominator = hypot(x[0]-xi[0], x[1]-xi[1]) ** p
    if isclose(denominator, 0):
        return 1
    weight = 1 / denominator
    return weight

def get_point_indices_in_proximity(point, internal_points, grid_dx):
    indices = []
    for i in range(len(internal_points)):
        if (abs(point[0] - internal_points[i][0]) <= grid_dx 
            and abs(point[1] - internal_points[i][1]) <= grid_dx):
        #if hypot(point[0] - internal_points[i][0], point[1] - internal_points[i][1]) <= 0.4:
            indices.append(i)
    
    return indices