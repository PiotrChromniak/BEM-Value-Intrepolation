import numpy as np
import file_loading
import interpolation
import argparse
import os.path

parser = argparse.ArgumentParser(description="Arguments for paser")
parser.add_argument('-p', default=2, type=int,
                    help='[uint] Factor for interpolation', metavar='COUNT')
parser.add_argument('-grid', type=int, required=True,
                    help='[uint] Grid density', metavar='COUNT')
parser.add_argument('-file', type=argparse.FileType('r'),
                    required=True, help='Input file', metavar='PATH')
parser.add_argument('-plotdir', type=str, default='',
                    help='Folder to hold output plots', metavar='DIRPATH')
parser.add_argument('-out', type=str, help='Name of vtk output file')
args = parser.parse_args()

if args.plotdir and not os.path.isdir(args.plotdir):
    print('plotdir doesn\'t exist or is not a directory')
    exit()

data = file_loading.load_data_from_file(args.file)

ans2 = interpolation.interpolate(data, args.grid, args.p)

ans = ans2['values']

x = np.array([i[0] for i in data['points']] + [i[0]
             for i in data['internal_points']] + [i[0] for i in ans2['points']])
y = np.array([i[1] for i in data['points']] + [i[1]
             for i in data['internal_points']] + [i[1] for i in ans2['points']])
Sxx = np.array(data['Sxx'] + data['inSxx'] + ans['Sxx'])
Syy = np.array(data['Syy'] + data['inSyy'] + ans['Syy'])
Sxy = np.array(data['Sxy'] + data['inSxy'] + ans['Sxy'])
Szz = np.array(data['Szz'] + data['inSzz'] + ans['Szz'])
SE = np.array(data['SE'] + data['inSE'] + ans['SE'])
UX = np.array(data['UX'] + data['inUX'] + ans['UX'])
UY = np.array(data['UY'] + data['inUY'] + ans['UY'])
if args.out:
    points = data['points']
    points_count = len(points)
    internal = data['internal_points']
    internal_count = len(internal)
    grid = ans2['points']
    grid_count = len(grid)
    elements = data['elements']

    print('Writing vtk files..', end='')
    with open(args.out + '0' + '.vtk', 'w', encoding='utf-8') as file:
        file.write('# vtk DataFile Version 2.0\n')
        file.write('Initial mesh\n')
        file.write('ASCII\n')
        file.write('DATASET UNSTRUCTURED_GRID\n')
        file.write('POINTS {} double\n'.format(
            points_count + internal_count + grid_count))
        for pt_x, pt_y in zip(x, y):
            file.write('{0} {1} 0.0\n'.format(pt_x, pt_y))

        file.write('CELLS {0} {1}\n'.format(len(elements) + grid_count + internal_count , len(elements) * 4 + (grid_count + internal_count) * 2))
        for el in elements:
            file.write('3 {0} {1} {2}\n'.format(el[0], el[1], el[2]))
        for i in range(internal_count):
            file.write('1 {}\n'.format(i + points_count))
        for i in range(grid_count):
            file.write('1 {}\n'.format(i + points_count + internal_count))

        file.write('CELL_TYPES {}\n'.format(len(elements) + grid_count + internal_count))
        for _ in range(len(elements)):
            file.write('21\n')
        for _ in range(grid_count + internal_count):
            file.write('1\n')

        file.write('POINT_DATA {0}\nTENSORS stresses double\n'.format(
            points_count + internal_count + grid_count))

        for xx, yy, xy, zz in zip(Sxx, Syy, Sxy, Szz):
            file.write(
                '{0} {2} 0.0\n{2} {1} 0.0\n0.0 0.0 {3}\n'.format(xx, yy, xy, zz))
            file.write('\n')
        
        file.write('VECTORS displacements double\n')
        for ux, uy in zip(UX, UY):
            file.write('{} {} 0.0\n'.format(ux, uy))

        file.write('\nSCALARS Mises double\nLOOKUP_TABLE tableName\n')
        for se in SE:
            file.write('{}\n'.format(se))

    
    x = x + UX
    y = y + UY
    with open(args.out + '1' + '.vtk', 'w', encoding = 'utf-8') as file:
        file.write('# vtk DataFile Version 2.0\n')
        file.write('Deformed mesh\n')
        file.write('ASCII\n')
        file.write('DATASET UNSTRUCTURED_GRID\n')
        file.write('POINTS {} double\n'.format(points_count + internal_count + grid_count))
        for pt_x, pt_y in zip(x,y):
            file.write('{0} {1} 0.0\n'.format(pt_x, pt_y))

        file.write('CELLS {0} {1}\n'.format(len(elements), len(elements) * 4))
        for el in elements:
            file.write('3 {0} {1} {2}\n'.format(el[0], el[1], el[2]))

        file.write('CELL_TYPES {}\n'.format(len(elements)))
        for _ in range(len(elements)):
            file.write('21\n')

        file.write('POINT_DATA {0}\nTENSORS stresses double\n'.format(points_count + internal_count + grid_count))

        for xx, yy, xy, zz in zip(Sxx, Syy, Sxy, Szz):
            file.write('{0} {2} 0.0\n{2} {1} 0.0\n0.0 0.0 {3}\n'.format(xx, yy, xy, zz))
            file.write('\n')   

        file.write('VECTORS displacements double\n')
        for ux, uy in zip(UX, UY):
            file.write('{} {} 0.0\n'.format(ux, uy))

        file.write('\nSCALARS Mises double\nLOOKUP_TABLE tableName\n')
        for se in SE:
            file.write('{}\n'.format(se))
    print('done')
    
