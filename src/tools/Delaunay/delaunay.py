import math

err = math.exp(-5)

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def cross_product_2d(vec1, vec2):
        return vec1.x * vec2.y - vec2.y * vec2.x

    def __eq__(self, other):
        if not isinstance(other, Vector):
            raise TypeError("Second operand type doesnt match type Vector(Point too)")
        return self.x == other.x and self.y == other.y

    def __sub__(self, other):
        if not isinstance(other, Vector):
            raise TypeError("Second operand type doesnt match type Vector(Point too)")
        return Vector(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        if not isinstance(other, Vector):
            raise TypeError("Second operand type doesnt match type Vector(Point too)")
        return Vector(self.x + other.x, self.y + other.y)

    def mul_num(self, number):
        return Vector(self.x * number, self.y * number)

    def normalize(self):
        length = math.sqrt(self.x ** 2 + self.y ** 2)
        if length == 0:
            length = 1
        return Vector(self.x / length, self.y / length)


class Triangle:
    def __init__(self, p1, p2, p3, p4):
        self._p1 = p1
        self._p2 = p2
        self._p3 = p3
        self._p4 = p4

    def make_triangle(self):
        pass


class Edge:
    def __init__(self, fp=None, sp=None):
        # Indexes first and second point in array of points
        self.inx_fst_point = fp
        self.inx_snd_point = sp


class PairVertexes:
    def __init__(self, fv=None, sv=None):
        # Indexes first and second point in array of points
        self.first_v = fv
        self.second_v = sv

    def insert_vert(self, nv):
        if self.first_v is None or self.second_v is None:
            return
        if self.first_v is None:
            self.first_v = nv
        else:
            self.second_v = nv

    def remove_vert(self, rv):
        if self.first_v == rv:
            self.first_v = None
        elif self.second_v == rv:
            self.second_v = rv

    def replace_vertexes(self, v1, v2):
        if self.first_v == v1:
            self.first_v = v2
        elif self.second_v == v1:
            self.second_v = v2
        else:
            self.insert_vert(v2)

    def max_from_two_vert(self):
        return max(self.first_v, self.second_v)

    def min_from_two_vert(self):
        return min(self.first_v, self.second_v)


class DelaunayTriangulation:
    def __init__(self, points):
        self.points = points
        # Dictionary <Edge, PairVertexes>
        self.triangulations_graph = dict()
        # For detecting visual edges in minimum convex hull from point
        self.minimum_convex_hull = dict()

    def __init_first_triangle(self):
        # List vertexes in the left and right side from vertex
        # index -> points[index] => left_vertex and right_vertex ->
        # points[left_vertex] and points[right_vertex] =>
        # this points around vertex(points[index])

        self.minimum_convex_hull[0] = {'left_vertex': 1, 'right_vertex': 1}
        self.minimum_convex_hull[1] = {'left_vertex': 0, 'right_vertex': 0}
        self.triangulations_graph[Edge(0, 1)] = PairVertexes()
        self.triangulations_graph[Edge(0, 1)].insert_vert(2)

    def __check_triangles(self):
        pass

    def __to_right_direction(self, last_vec, next_vec, ix_point, prev_ix_mch, next_ix_mch):
        while Vector.cross_product_2d(last_vec, next_vec) > -err:
            self.__check_triangles()


    def do_triangulation(self):
        sorted(self.points, key=lambda point: point.x)
        self.__init_first_triangle()

        for i in range(2, len(self.points)):
            prev_ix_mch_vert = i - 1
            next_ix_mch_vert = self.minimum_convex_hull[prev_ix_mch_vert]['right_vertex']
            last_vec = self.points[prev_ix_mch_vert] - self.points[i]
            next_vec = self.points[next_ix_mch_vert] - self.points[i]


