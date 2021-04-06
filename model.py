import numpy as np

from drawer import lineBres


class Model:

    def __init__(self):
        self.vertexes = np.array((None, 3))
        self.faces = np.array((None, 3))
        self.k = np.array([[10000, 0, 1000],
                           [0, -10000, 1000],
                           [0, 0, 1]])

    def parse_file(self, filename):
        file = open(filename, 'r')
        res_p = np.empty((0, 3), dtype=np.float64)
        res_f = np.empty((0, 3), dtype=np.int64)
        while True:
            line = file.readline()
            if line == '':
                break
            line_array = line.split(' ')
            if line_array[0] == 'v':
                line_array = [float(i) for i in line_array[1:]]
                res_p = np.append(res_p, [line_array], axis=0)
            elif line_array[0] == 'f':
                line_array = [int(i) for i in [j.split('/')[0] for j in line_array[1:]]]
                res_f = np.append(res_f, [line_array], axis=0)
        self.vertexes, self.faces = res_p, res_f

    def draw_vertexes(self, img, color):
        pixels = img.load()
        for i in self.vertexes:
            pixels[4000 * i[0] + 500, -4000 * i[1] + 500] = color
        img.show()

    def draw_faces(self, img, color):
        tmp_point = self.vertexes
        tmp_point[:, 2] = 1
        tmp_point = np.dot(self.vertexes, self.k.T)
        for i in self.faces:
            lineBres(tmp_point[i[0] - 1][0], tmp_point[i[0] - 1][1], tmp_point[i[1] - 1][0],
                     tmp_point[i[1] - 1][1], img, color)
            lineBres(tmp_point[i[1] - 1][0], tmp_point[i[1] - 1][1], tmp_point[i[2] - 1][0],
                     tmp_point[i[2] - 1][1], img, color)
            lineBres(tmp_point[i[0] - 1][0], tmp_point[i[0] - 1][1], tmp_point[i[2] - 1][0],
                     tmp_point[i[2] - 1][1], img, color)
        img.show()
