import re


def load_data_from_file(file):
    #read points
    print('Loading points...')
    next(file)
    points = []
    while file.read(1) is '\t':
        lines = file.readline().split()[1:]
        points.append([float(lines[0]), float(lines[1])])

    #read elements
    print('Loading elements...')
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
    print('Loading internal points...')
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
    print('Loading values for points...')
    UX = []; UY = []; Un = []; Us = []
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
    print('Loading stresses for points...')
    Sxx = []; Syy = []; Sxy = []
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

    print('Loading values for internal points...')
    inUX = []; inUY = []
    for _ in range(len(internal_points)):
        line = file.readline()
        lines = line.split()[3:]
        inUX.append(float(lines[0]))
        inUY.append(float(lines[1]))
    
    next(file)
    next(file)

    print('Loading stresses for internal points...')
    inSxx = []; inSyy = []; inSxy = []
    for _ in range(len(internal_points)):
        line = file.readline()
        lines = line.split()[3:]
        inSxx.append(float(lines[0]))
        inSyy.append(float(lines[1]))
        inSxy.append(float(lines[2]))

    print('\nLoaded:\n{} points'.format(len(points)))
    print('{} elements'.format(len(elements)))
    print('{} internal points'.format(len(internal_points)))
    print('{0} UX\t{1} UY\t{2} Un\t{3} Us'.format(len(UX), len(UY), len(Un), len(Us)))
    print('{0} Sxx\t{1} Syy\t{2} Sxy'.format(len(Sxx), len(Syy), len(Sxy)))
    print('{0} UX\t {1} UY'.format(len(inUX), len(inUY)))
    print('{0} Sxx\t{1} Syy\t{2} Sxy'.format(len(inSxx), len(inSyy), len(inSxy)))

    return { 'points': points, 'internal_points': internal_points,
             'elements': elements, 'UX': UX, 'UY': UY, 'inUX': inUX,
             'inUY': inUY, 'Sxx': Sxx, 'Syy': Syy, 'Sxy': Sxy,
             'inSxx': inSxx, 'inSyy': inSxy, 'inSxy': inSxy}
