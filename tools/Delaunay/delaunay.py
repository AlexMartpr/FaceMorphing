import math

err = 1 / 10**9
# err = 0

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def cross_product_2d(vec1, vec2):
        return vec1.x * vec2.y - vec1.y * vec2.x

    def __str__(self):
        return f"x : {self.x}  y : {self.y}"

    def __lt__(self, other):
        if self.x == other.x:
            return self.y < other.y
        return self.x < other.x

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
    def __init__(self, fp=-1, sp=-1):
        # Indexes first and second point in array of points
        self.inx_fst_point = fp
        self.inx_snd_point = sp

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.inx_fst_point == other.inx_fst_point and self.inx_snd_point == other.inx_snd_point

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.inx_fst_point, self.inx_snd_point))


class PairVertexes:
    def __init__(self, fv=-1, sv=-1):
        # Indexes first and second point in array of points
        self.first_v = fv
        self.second_v = sv

    def insert_vert(self, nv):
        if self.first_v == nv or self.second_v == nv:
            return
        if self.first_v == -1:
            self.first_v = nv
        else:
            self.second_v = nv

    def remove_vert(self, rv):
        if self.first_v == rv:
            self.first_v = -1
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
        self.minimum_convex_hull = dict().fromkeys((range(len(self.points))))
        self.recursion = dict()
        for ix in range(len(self.points)):
            self.minimum_convex_hull[ix] = {'left_vertex': -1, 'right_vertex': -1}

    def __init_first_triangle(self):
        # List vertexes in the left and right side from vertex
        # index -> points[index] => left_vertex and right_vertex ->
        # points[left_vertex] and points[right_vertex] =>
        # this points around vertex(points[index])

        self.minimum_convex_hull[0] = {'left_vertex': 1, 'right_vertex': 1}
        self.minimum_convex_hull[1] = {'left_vertex': 0, 'right_vertex': 0}
        self.triangulations_graph[Edge(0, 1)] = PairVertexes()
        self.triangulations_graph[Edge(0, 1)].insert_vert(2)

    def __check_convex(self, vec1, vec2, vec3):
        return Vector.cross_product_2d(vec1, vec2) < 0 or Vector.cross_product_2d(vec3, vec2) > 0

    def __delaunay_cond(self, left_v, right_v, out_v, inn_v):
        if out_v == inn_v:
            return True

        left_vert = self.points[left_v]
        right_vert = self.points[right_v]
        top_vert = self.points[out_v]
        bottom_vert = self.points[inn_v]

        vec_1 = left_vert - top_vert
        vec_2 = bottom_vert - top_vert
        vec_3 = right_vert - top_vert

        if self.__check_convex(vec_1, vec_2, vec_3):
            return True

        s_alpha = (top_vert.x - right_vert.x) * (top_vert.x - left_vert.x) + (top_vert.y - right_vert.y) * (
                top_vert.y - left_vert.y)
        s_beta = (bottom_vert.x - right_vert.x) * (bottom_vert.x - left_vert.x) + (bottom_vert.y - right_vert.y) * (
                bottom_vert.y - left_vert.y)

        if s_alpha > -err and s_beta > -err:
            return True

        if not (s_alpha < 0 and s_beta < 0):
            edge_1, edge_2 = top_vert - right_vert, top_vert - left_vert
            edge_3, edge_4 = bottom_vert - right_vert, bottom_vert - left_vert

            help_coeff_1 = Vector.cross_product_2d(edge_1, edge_2)
            help_coeff_2 = Vector.cross_product_2d(edge_3, edge_4)

            help_coeff_1 = -help_coeff_1 if help_coeff_1 < 0 else help_coeff_1
            help_coeff_2 = -help_coeff_2 if help_coeff_2 < 0 else help_coeff_2

            check_cond = help_coeff_1 * s_beta + s_alpha * help_coeff_2

            if check_cond > -err:
                return True

        return False

    def __flip(self, left, right, out_v, min_vert_in_hull):
        key = Edge(right, out_v)
        if key not in self.triangulations_graph:
            self.triangulations_graph[key] = PairVertexes()
        self.triangulations_graph[key].replace_vertexes(left, min_vert_in_hull)
        key = Edge(left, out_v)
        if key not in self.triangulations_graph:
            self.triangulations_graph[key] = PairVertexes()
        self.triangulations_graph[key].replace_vertexes(right, min_vert_in_hull)
        _min, _max = min(min_vert_in_hull, left), max(min_vert_in_hull, left)
        key = Edge(_min, _max)
        if key not in self.triangulations_graph:
            self.triangulations_graph[key] = PairVertexes()
        self.triangulations_graph[key].replace_vertexes(right, out_v)
        _min, _max = min(min_vert_in_hull, right), max(min_vert_in_hull, right)
        key = Edge(_min, _max)
        if key not in self.triangulations_graph:
            self.triangulations_graph[key] = PairVertexes()
        self.triangulations_graph[key].replace_vertexes(left, out_v)

        _min, _max = min(left, right), max(left, right)
        try:
            del self.triangulations_graph[Edge(_min, _max)]
        except KeyError:
            raise KeyError("Given key doesnt exists in triangulations_graph")
        except Exception as e:
            raise Exception(e.__str__())

    def __legalize_triangles(self, left_v, right_v, out_v):
        self.recursion[0] = Edge(left_v, right_v)
        sz_stack = 1

        while sz_stack > 0:
            # print(sz_stack)
            ix_prev = sz_stack - 1
            left, right = self.recursion[ix_prev].inx_fst_point, self.recursion[ix_prev].inx_snd_point
            sz_stack -= 1
            _min, _max = min(left, right), max(left, right)
            key = Edge(_min, _max)
            if key not in self.triangulations_graph:
                self.triangulations_graph[key] = PairVertexes()
            min_vert_in_hull = self.triangulations_graph[key].min_from_two_vert()
            if self.__delaunay_cond(left, right, out_v, min_vert_in_hull):
                key = Edge(right, out_v)
                if key not in self.triangulations_graph:
                    self.triangulations_graph[key] = PairVertexes()
                self.triangulations_graph[key].insert_vert(left)
                key = Edge(left, out_v)
                if key not in self.triangulations_graph:
                    self.triangulations_graph[key] = PairVertexes()
                self.triangulations_graph[key].insert_vert(right)
                if right < left:
                    right, left = left, right
                key = Edge(left, right)
                if key not in self.triangulations_graph:
                    self.triangulations_graph[key] = PairVertexes()
                self.triangulations_graph[key].insert_vert(out_v)
                continue

            self.__flip(left, right, out_v, min_vert_in_hull)
            self.recursion[sz_stack], self.recursion[sz_stack + 1] = Edge(left, min_vert_in_hull), Edge(
                min_vert_in_hull, right)
            sz_stack += 2

    def __to_right_direction(self, last_vec, next_vec, ix_point, prev_ix_mch, next_ix_mch):
        while Vector.cross_product_2d(last_vec, next_vec) >= 0:
            # print(str(last_vec))
            # print(str(next_vec))
            # exit(-1)
            # print(Vector.cross_product_2d(last_vec, next_vec))
            self.__legalize_triangles(prev_ix_mch, next_ix_mch, ix_point)
            prev_ix_mch = next_ix_mch
            last_vec = next_vec
            next_ix_mch = self.minimum_convex_hull[prev_ix_mch]['right_vertex']
            next_vec = self.points[next_ix_mch] - self.points[ix_point]

        self.minimum_convex_hull[ix_point]['right_vertex'] = prev_ix_mch

    def __to_left_direction(self, last_vec, next_vec, ix_point, prev_ix_mch, next_ix_mch):
        while Vector.cross_product_2d(last_vec, next_vec) <= 0:
            print(str(last_vec))
            print(str(next_vec))
            self.__legalize_triangles(next_ix_mch, prev_ix_mch, ix_point)
            prev_ix_mch = next_ix_mch
            last_vec = next_vec
            next_ix_mch = self.minimum_convex_hull[prev_ix_mch]['left_vertex']
            next_vec = self.points[next_ix_mch] - self.points[ix_point]

        self.minimum_convex_hull[ix_point]['left_vertex'] = prev_ix_mch

    def do_triangulation(self):
        self.points = sorted(self.points)
        # print(self.points)
        self.__init_first_triangle()

        for i in range(2, len(self.points)):
            prev_ix_mch_vert = i - 1
            next_ix_mch_vert = self.minimum_convex_hull[prev_ix_mch_vert]['right_vertex']
            last_vec = self.points[prev_ix_mch_vert] - self.points[i]
            next_vec = self.points[next_ix_mch_vert] - self.points[i]
            print(i)
            self.__to_right_direction(last_vec, next_vec, i, prev_ix_mch_vert, next_ix_mch_vert)
            print(i)
            prev_ix_mch_vert = i - 1
            next_ix_mch_vert = self.minimum_convex_hull[prev_ix_mch_vert]['left_vertex']
            last_vec = self.points[prev_ix_mch_vert] - self.points[i]
            next_vec = self.points[next_ix_mch_vert] - self.points[i]
            self.__to_left_direction(last_vec, next_vec, i, prev_ix_mch_vert, next_ix_mch_vert)

            ix = self.minimum_convex_hull[i]['right_vertex']
            self.minimum_convex_hull[ix]['left_vertex'] = i
            self.minimum_convex_hull[prev_ix_mch_vert]['right_vertex'] = i
