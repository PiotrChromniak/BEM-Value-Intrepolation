from math import hypot, isclose
import matplotlib.pyplot as plt
import numpy as np
import grid
import file_loading



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
'''
data = file_loading.load_data_from_file('C:/Users/Viator/Documents/GitHub/BEM-Value-Intrepolation/2.out')
ans = interpolate(data, 50, p=3)

x = np.array([ i[0] for i in data['points']] + [ i[0] for i in data['internal_points']] + [ i[0] for i in ans['points'] ])
y = np.array([ i[1] for i in data['points']] + [ i[1] for i in data['internal_points']] + [ i[1] for i in ans['points']])
z = np.array(data['Sxx'] + data['inSxx'] + ans['values'])

plt.tripcolor(x,y,z,cmap=plt.cm.hot_r,edgecolor='black')
#plt.tricontourf(x, y, z, 10, cmap=plt.cm.hot_r,edgecolor='black')
x = plt.colorbar()
plt.show()
#plt.savefig('test.png')
'''