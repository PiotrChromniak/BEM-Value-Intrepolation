import numpy as np
import math


class FunctionRange(object):
    def __init__(self, ans):
        self.A = float(ans[0])
        self.B = float(ans[1])
        self.C = float(ans[2])

    def is_in_range(self, x):
        raise NotImplementedError()

    def get_intersections_count(self, x, limit):
        raise NotImplementedError()


class StandardRange(FunctionRange):
    def __init__(self, points):
        (x1, y1, x2, y2, x3, y3) = (points[0][0], points[0][1],
                                    points[1][0], points[1][1],
                                    points[2][0], points[2][1])
        mat = np.array([[x1**2, x1, 1],
                        [x2**2, x2, 1],
                        [x3**2, x3, 1]])
        b = np.array([y1, y2, y3])
        ans = np.linalg.solve(mat, b)
        FunctionRange.__init__(self, ans)

        self.start = min(x1, x3)
        self.end = max(x1, x3)

    def _f(self, x):
        return ((self.A * x) + self.B) * x + self.C

    def is_in_range(self, x):
        return x >= self.start and x <= self.end
    
    def get_intersections_count(self, x, limit):
       y = self._f(x)
       return 0 if y < limit else 1

class OrthogonalRange(FunctionRange):
    def __init__(self, points):
        (x1, y1, x2, y2, x3, y3) = (points[0][0], points[0][1],
                                    points[1][0], points[1][1],
                                    points[2][0], points[2][1])
        mat = np.array([[y1**2, y1, 1],
                        [y2**2, y2, 1],
                        [y3**2, y3, 1]])
        b = np.array([x1, x2, x3])
        ans = np.linalg.solve(mat, b)
        FunctionRange.__init__(self, ans)

        symm_x = (4 * self.A * self.C - self.B**2) / (4 * self.A)
        (upper_x, lower_x) = (x1, x3) if y1 > y3 else (x3, x1)
        #upper_x = x1 if y1 > y3 else x3
        #lower_x = x3 if y1 > y3 else x1
        self.upper_end = max(symm_x, upper_x)
        self.upper_start = min(symm_x, upper_x)
        self.lower_end = max(symm_x, lower_x)
        self.lower_start = min(symm_x, lower_x)

    def is_in_range(self, x):
        in_upper_range = self.upper_end >= x >= self.upper_start
        #in_upper_range = x >= self.upper_start and x <= self.upper_end
        #in_lower_range = x >= self.lower_start and x <= self.lower_end
        in_lower_range = self.lower_end >= x >= self.lower_start 
        return in_lower_range or in_upper_range

    def get_intersections_count(self, x, limit):
        sqrt_delta = math.sqrt(self.B**2 - 4 * self.A * (self.C - x))
        (solution1, solution2) = ((-self.B - sqrt_delta) /
                                  (2 * self.A), (-self.B + sqrt_delta) / (2 * self.A))
        y1 = min(solution1, solution2)
        y2 = max(solution1, solution2)

        intersection_counter = 0

        if x >= self.lower_start and x <= self.lower_end and y1 >= limit:
            intersection_counter += 1

        if x >= self.upper_start and x <= self.upper_end and y2 >= limit:
            intersection_counter += 1

        return intersection_counter

class LinearRange(FunctionRange):
    def __init__(self, points):
        (x1, y1, x3, y3) = (points[0][0], points[0][1],
                            points[2][0], points[2][1])

        if x1 < x3:
            self.p1 = points[0]
            self.p2 = points[2]
        else:
            self.p1 = points[2]
            self.p2 = points[0]

    def is_in_range(self, x):
        return self.p1[0] <= x <= self.p2[0]

    def _f(self, x):
        lhs = (x - self.p1[0])/(self.p2[0] - self.p1[0])
        rhs = self.p2[1] - self.p1[1]
        fn_value = self.p1[1] + lhs / rhs
        return fn_value

    def get_intersections_count(self, x, limit):
        value = self._f(x)
        return 1 if limit <= value else 1
        

'''
a = OrthogonalRange([[2,3], [3,2], [1,1]])
ans1 = a.get_intersections_count(1.5, 0.5)
ans2 = a.get_intersections_count(1.5, 2)
ans3 = a.get_intersections_count(1.5, 3.5)

a1 = a.is_in_range(0.5)
a2 = a.is_in_range(1.5)
a3 = a.is_in_range(2.5)
a4 = a.is_in_range(4)

b = StandardRange([[-1,1], [0,0], [1,1]])
bans1 = b.get_intersections_count(0,1)
bans2 = b.get_intersections_count(0,-1)

b1 = b.is_in_range(-2)
b2 = b.is_in_range(0.5)
b3 = b.is_in_range(2)
print("a")
'''