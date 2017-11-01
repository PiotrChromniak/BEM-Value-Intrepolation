
import re


def load_data_from_file(filepath):
    with open(filepath, encoding = 'utf-8') as file:
        #read points
        next(file)
        points = []
        while file.read(1) is '\t':
            lines = file.readline().split()[1:]
            points.append([float(lines[0]), float(lines[1])])

        #read elements
        next(file)
        elements = []
        line = file.readline()
        while re.search(r'\d', line):
            lines = line.split()[1:]
            elements.append([int(lines[0]), int(lines[1]), int(lines[2])])
            line = file.readline()
        
        #skip untill internal points section
        while file.read(1) is not 'I':
            next(file)
        next(file)

        #read optional internal points
        next(file)
        internal_points = []
        line = file.readline()
        while re.search(r'\d', line):
            lines = line.split()[1:]
            internal_points.append([float(lines[0]), float(lines[1])])
            line = file.readline()

        #skip untill calculation results
        while not re.search(r'Node', file.read(7)):
            next(file)
        next(file)

        #read point results
        UX = []
        UY = []
        Un = []
        Us = []
        for _ in range(len(points)):
            line = file.readline()
            lines = line.split()[3:]
            UX.append(float(lines[0]))
            UY.append(float(lines[1]))
            Un.append(float(lines[2]))
            Us.append(float(lines[3]))
        
        #skip until stesses table
        while not re.search(r'Node', file.read(7)):
            next(file)
        next(file)

        #read point stresses
        Sxx = []
        Syy = []
        Sxy = []
        for _ in range(len(points)):
            line = file.readline()
            lines = line.split()[1:4]
            Sxx.append(float(lines[0]))
            Syy.append(float(lines[1]))
            Sxy.append(float(lines[2]))

        #skip until internal point results
        while not re.search(r'Internal', file.read(10)):
            next(file)
        next(file)
        next(file)

        inUX = []
        inUY = []
        for _ in range(len(internal_points)):
            line = file.readline()
            lines = line.split()[3:]
            inUX.append(float(lines[0]))
            inUY.append(float(lines[1]))

        next(file)
        next(file)

        inSxx = []
        inSyy = []
        inSxy = []
        for _ in range(len(internal_points)):
            line = file.readline()
            lines = line.split()[3:]
            inSxx.append(float(lines[0]))
            inSyy.append(float(lines[1]))
            inSxy.append(float(lines[2]))
            
        return { 'points': points, 'internal_points': internal_points,
                 'elements': elements, 'UX': UX, 'UY': UY, 'inUX': inUX,
                 'inUY': inUY, 'Sxx': Sxx, 'Syy': Syy, 'Sxy': Sxy,
                 'inSxx': inSxx, 'inSyy': inSxy, 'inSxy': inSxy}


pts = load_data_from_file('C:/Users/Viator/Documents/GitHub/BEM-Value-Intrepolation/1.out')