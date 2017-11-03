import matplotlib.pyplot as plt
import numpy as np
import file_loading
import interpolation


data = file_loading.load_data_from_file('C:/Users/Viator/Documents/GitHub/BEM-Value-Intrepolation/2.out')
#ans = interpolation.interpolate(data, 10, p=3)
ans2 = interpolation.interpolate2(data, 50, p=3)
ans = ans2['values']

x = np.array([ i[0] for i in data['points']] + [ i[0] for i in data['internal_points']] + [ i[0] for i in ans2['points']])
y = np.array([ i[1] for i in data['points']] + [ i[1] for i in data['internal_points']] + [ i[1] for i in ans2['points']])
z = np.array(data['Sxx'] + data['inSxx'] + ans['Sxx'])

plt.tripcolor(x, y, z, cmap=plt.cm.hot_r, edgecolor='black')
#plt.tricontourf(x, y, z, 10, cmap=plt.cm.hot_r,edgecolor='black')
cbar = plt.colorbar()
path = 'C:/Users/Viator/Documents/GitHub/BEM-Value-Intrepolation/wyniki/'
plt.savefig(path + 'Sxx')


cbar.remove()
z = np.array(data['Syy'] + data['inSyy'] + ans['Syy'])
plt.tripcolor(x, y, z, cmap=plt.cm.hot_r, edgecolor='black')
#plt.tricontourf(x, y, z, 10, cmap=plt.cm.hot_r,edgecolor='black')
cbar = plt.colorbar()
plt.savefig(path + 'Syy')

cbar.remove()
z = np.array(data['Sxy'] + data['inSxy'] + ans['Sxy'])
plt.tripcolor(x, y, z, cmap=plt.cm.hot_r, edgecolor='black')
#plt.tricontourf(x, y, z, 10, cmap=plt.cm.hot_r,edgecolor='black')
cbar = plt.colorbar()
plt.savefig(path + 'Sxy')

cbar.remove()
z = np.array(data['UX'] + data['inUX'] + ans['UX'])
plt.tripcolor(x, y, z, cmap=plt.cm.hot_r, edgecolor='black')
#plt.tricontourf(x, y, z, 10, cmap=plt.cm.hot_r,edgecolor='black')
cbar = plt.colorbar()
plt.savefig(path + 'UX')

cbar.remove()
z = np.array(data['UY'] + data['inUY'] + ans['UY'])
plt.tripcolor(x, y, z, cmap=plt.cm.hot_r, edgecolor='black')
#plt.tricontourf(x, y, z, 10, cmap=plt.cm.hot_r,edgecolor='black')
cbar = plt.colorbar()
plt.savefig(path + 'UY')