from math import hypot, isclose
import numpy as np
import grid

def interpolate2(results, grid_density, p=2):
    (points, elements) = (results['points'], results['elements'])

    ranges = grid.generate_ranges(points, elements)
    borders = grid.find_grid_borders(points)
    generated_points = grid.generate_grid_points(ranges, grid_density, borders)
    dx = (borders['max_x'] - borders['min_x']) / grid_density
    interpolated_vals = interpolate_values2(generated_points, results, dx, p)
    return { 'points': generated_points, 'values': interpolated_vals }

def interpolate(results, grid_density, p=2):
    (points, UX, UY, Sxx, Syy, Sxy) = (results['points'], results['UX'], results['UY'],
                                       results['Sxx'], results['Syy'], results['Sxy'])

    (internal_points, inUX, inUY, inSxx, inSyy, inSxy) = (results['internal_points'], 
                                                          results['inUX'], results['inUY'],
                                                          results['inSxx'], results['inSyy'],
                                                          results['inSxy'])
                                
    elements = results['elements']
    ranges = grid.generate_ranges(points, elements)
    borders = grid.find_grid_borders(points)
    generated_points = grid.generate_grid_points(ranges, grid_density, borders)
    dx = borders['max_x'] - borders['min_x']
    result = interpolate_values(generated_points, points, internal_points, Sxx, inSxx, dx, p)

    return { 'points': generated_points, 'values': result}

def interpolate_values(new_points, points, internal_points, input_vals, internal_vals, grid_dx, p):
    result_values = []
    
    for i in range(len(new_points)):
        x = new_points[i]
        weights = [ calculate_weight(x, xi, p) for xi in points ]
        nominator = np.dot(weights, input_vals)
        denominator = sum(weights)

        if internal_points:
            indices = filter_point_indices_in_proximity(x, internal_points, grid_dx)
            for idx in indices:
                weight = calculate_weight(x, internal_points[idx], p)
                nominator += weight * internal_vals[idx]
                denominator += weight

        result_values.append(nominator/denominator)
    
    return result_values
        

def interpolate_values2(new_points, data, grid_dx, p):
    basic_values = [data['Sxx'], data['Syy'], data['Sxy'], data['UX'], data['UY']]
    internal_values = [data['inSxx'], data['inSyy'], data['inSxy'], data['inUX'], data['inUY']] if data['internal_points'] else None
    points = data['points']
    internal_points = data['internal_points'] if internal_values else None

    results = [[], [], [], [], []]
    for i in range(len(new_points)):
        x = new_points[i]
        weights = [ calculate_weight(x, xi, p) for xi in points ]
        indices = None
        internal_weights = None
        if internal_points:
            indices = get_point_indices_in_proximity(x, internal_points, grid_dx)
            if indices:
                print('for point {:.2} {:.2} there are {} internal point neighbours'.format(x[0], x[1], len(indices)))
            internal_weights = [calculate_weight(x, internal_points[idx], p) for idx in indices]

        for j in range(len(basic_values)):
            nominator = np.dot(weights, basic_values[j])
            denominator = sum(weights)
            if internal_points:
                denominator += sum(internal_weights)
                for idx, weight in zip(indices, internal_weights):
                    nominator += internal_values[j][idx] * weight
            results[j].append(nominator/denominator)

    return { 'Sxx': results[0], 'Syy': results[1], 
             'Sxy': results[2], 'UX': results[3], 
             'UY': results[4] }

def calculate_weight(x, xi, p):
    denominator = hypot(x[0]-xi[0], x[1]-xi[1]) ** p
    if isclose(denominator, 0):
        return 1
    weight = 1 / denominator
    return weight

def filter_point_indices_in_proximity(point, internal_points, grid_dx):
    for i in range(len(internal_points)):
        if abs(point[0] - internal_points[i][0]) <= grid_dx and abs(point[1] - internal_points[i][1]) <= grid_dx:
            yield i


def get_point_indices_in_proximity(point, internal_points, grid_dx):
    indices = []
    for i in range(len(internal_points)):
        if abs(point[0] - internal_points[i][0]) <= grid_dx and abs(point[1] - internal_points[i][1]) <= grid_dx:
        #if hypot(point[0] - internal_points[i][0], point[1] - internal_points[i][1]) <= 0.4:
            indices.append(i)
    
    return indices