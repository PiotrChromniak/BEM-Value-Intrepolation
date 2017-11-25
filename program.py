import matplotlib.pyplot as plt
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

print('Generating plots...', end='')
plt.tripcolor(x, y, Sxx, cmap=plt.cm.hot_r, edgecolor='black')
# plt.tricontourf(x, y, z, 20, cmap=plt.cm.hot_r,edgecolor='black')
cbar = plt.colorbar()
path = args.plotdir
plt.savefig(os.path.join(path, 'Sxx'))


cbar.remove()
Syy = np.array(data['Syy'] + data['inSyy'] + ans['Syy'])
plt.tripcolor(x, y, Syy, cmap=plt.cm.hot_r, edgecolor='black')
# plt.tricontourf(x, y, z, 10, cmap=plt.cm.hot_r,edgecolor='black')
cbar = plt.colorbar()
plt.savefig(os.path.join(path, 'Syy'))

cbar.remove()
Sxy = np.array(data['Sxy'] + data['inSxy'] + ans['Sxy'])
plt.tripcolor(x, y, Sxy, cmap=plt.cm.hot_r, edgecolor='black')
# plt.tricontourf(x, y, z, 10, cmap=plt.cm.hot_r,edgecolor='black')
cbar = plt.colorbar()
plt.savefig(os.path.join(path, 'Sxy'))

cbar.remove()
UX = np.array(data['UX'] + data['inUX'] + ans['UX'])
plt.tripcolor(x, y, UX, cmap=plt.cm.hot_r, edgecolor='black')
# plt.tricontourf(x, y, z, 10, cmap=plt.cm.hot_r,edgecolor='black')
cbar = plt.colorbar()
plt.savefig(os.path.join(path, 'UX'))

cbar.remove()
UY = np.array(data['UY'] + data['inUY'] + ans['UY'])
plt.tripcolor(x, y, UY, cmap=plt.cm.hot_r, edgecolor='black')
# plt.tricontourf(x, y, z, 10, cmap=plt.cm.hot_r,edgecolor='black')
cbar = plt.colorbar()
plt.savefig(os.path.join(path, 'UY'))
print('done')

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
        file.write('ASCII\n')
        file.write('DATASET UNSTRUCTURED_GRID\n')
        file.write('POINTS {} double\n'.format(
            points_count + internal_count + grid_count))
        for pt_x, pt_y in zip(x, y):
            file.write('{0} {1} 0.0\n'.format(pt_x, pt_y))

        file.write('CELLS {0} {1}\n'.format(len(elements), len(elements) * 4))
        for el in elements:
            file.write('3 {0} {1} {2}\n'.format(el[0], el[1], el[2]))

        file.write('CELL_TYPES {}\n'.format(len(elements)))
        for _ in range(len(elements)):
            file.write('21\n')

        file.write('POINT_DATA {0}\nTENSORS stresses double\n'.format(
            points_count + internal_count + grid_count))

        for xx, yy, xy in zip(Sxx, Syy, Sxy):
            file.write(
                '{0} {2} 0.0\n{2} {1} 0.0\n0.0 0.0 0.0\n'.format(xx, yy, xy))
            file.write('\n')
    
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

        for xx, yy, xy in zip(Sxx, Syy, Sxy):
            file.write('{0} {2} 0.0\n{2} {1} 0.0\n0.0 0.0 0.0\n'.format(xx, yy, xy))
            file.write('\n')   

    print('done')
    
