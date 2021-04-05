import numpy as np
from PIL import Image


class Model:

    def __init__(self):
        #4
        self.points = np.array((None, 3))
        #6
        self.faces = np.array((None, 3))
        self.normals = np.array((None, 3))
        self.k = np.array([[10000, 0, 1000],
                           [0, -10000, 1000],
                           [0, 0, 1]])

    def set_k(self, arr):
        self.k = arr

    def get_k(self):
        return self.k

    def set_points_array(self, points):
        self.points = np.array(points)

    def get_points_array(self):
        return self.points

    def get_point(self, index):
        return self.points[index]

    def get_face(self, index):
        return self.faces[index]

    def set_normals(self, array):
        self.normals = array

    def get_normals(self):
        return self.normals

    def draw_line(self, image, color, x0, y0, x1, y1):
        pixels = image.load()
        steep = False
        x0 = int(x0)
        x1 = int(x1)
        y0 = int(y0)
        y1 = int(y1)
        if (np.abs(x0 - x1) < np.abs(y0 - y1)):
            x0, y0 = y0, x0
            x1, y1 = y1, x1
            steep = True
        if (x0 > x1):
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        for x in range(x0, x1, 1):
            t = (x - x0) / (x1 - x0)
            y = int(y0 * (1. - t) + y1 * t)
            if x >= 0 and x < image.size[0] and y >= 0 and y < image.size[1]:
                if (steep):
                    pixels[x, y] = color
                else:
                    pixels[y, x] = color

    def parse_file(self, filename):
        file = open(filename, 'r')
        res_p = np.empty((0, 3), dtype=np.float)
        res_f = np.empty((0, 3), dtype=np.int)
        while True:
            line = file.readline()
            if line == '':
                break
            line_array = line.split(' ')
            #4
            if (line_array[0] == 'v'):
                line_array = [float(i) for i in line_array[1:]]
                res_p = np.append(res_p, [line_array], axis=0)
            #6
            elif (line_array[0] == 'f'):
                line_array = [int(i) for i in [j.split('/')[0] for j in line_array[1:]]]
                res_f = np.append(res_f, [line_array], axis=0)
        self.points, self.faces = res_p, res_f

    #5
    def draw_points(self, image, color):
        pixels = image.load()
        for i in self.points:
            # применить умножение матриц
            pixels[self.k[0][0] * i[0] + self.k[0][2], self.k[1][1] * i[1] + self.k[1][2]] = color
        image.show()

    #7
    def draw_faces(self, image, color):
        tmp_point = self.points
        tmp_point[:, 2] = 1
        tmp_point = np.dot(self.points, self.k.T)
        for i in self.faces:
            Model.draw_line(image, color, tmp_point[i[0] - 1][0], tmp_point[i[0] - 1][1], tmp_point[i[1] - 1][0],
                            tmp_point[i[1] - 1][1])
            Model.draw_line(image, color, tmp_point[i[1] - 1][0], tmp_point[i[1] - 1][1], tmp_point[i[2] - 1][0],
                            tmp_point[i[2] - 1][1])
            Model.draw_line(image, color, tmp_point[i[0] - 1][0], tmp_point[i[0] - 1][1], tmp_point[i[2] - 1][0],
                            tmp_point[i[2] - 1][1])

    def draw_triangle(self, image, color, x0, y0, x1, y1, x2, y2):
        pixels = image.load()
        a0 = 1 / ((y0 - y2) * (x1 - x2) - (x0 - x2) * (y1 - y2))
        a1 = 1 / ((y1 - y0) * (x2 - x0) - (x1 - x0) * (y2 - y0))
        a2 = 1 / ((y2 - y1) * (x0 - x1) - (x2 - x1) * (y0 - y1))
        for x in range(int(max(0, (min([x0, x1, x2]) - 1))), int(min(image.size[0], (max([x0, x1, x2]) + 1)))):
            for y in range(int(max(0, (min([y0, y1, y2]) - 1))), int(min(image.size[1], (max([y0, y1, y2]) + 1)))):
                l0 = ((y - y2) * (x1 - x2) - (x - x2) * (y1 - y2)) * a0
                l1 = ((y - y0) * (x2 - x0) - (x - x0) * (y2 - y0)) * a1
                l2 = ((y - y1) * (x0 - x1) - (x - x1) * (y0 - y1)) * a2
                if l0 > 0 and l1 > 0 and l2 > 0:
                    pixels[x, y] = color

    def draw_polygons(self, image):
        tmp_point = np.array(self.points)
        nrmls = np.array((None, 3))
        tmp_point[:, 2] = 1  # проекция на плоскость z=1
        tmp_point = np.dot(tmp_point, self.k.T)
        for i in self.faces:
            v0 = (tmp_point[i[0] - 1][0], tmp_point[i[0] - 1][1], tmp_point[i[0] - 1][2])
            v1 = (tmp_point[i[1] - 1][0], tmp_point[i[1] - 1][1], tmp_point[i[1] - 1][2])
            v2 = (tmp_point[i[2] - 1][0], tmp_point[i[2] - 1][1], tmp_point[i[2] - 1][2])
            d1 = self.points[i[1] - 1] - self.points[i[0] - 1]
            d2 = self.points[i[2] - 1] - self.points[i[0] - 1]
            n = np.cross(d1, d2)
            n /= np.linalg.norm(n)
            if n[2] <= 0:
                np.append(nrmls, n)
            else:
                continue
            self.draw_triangle(image, (int(round(n[2] * (-255))), int(round(n[2] * (-255))), int(round(n[2] * (-255)))),
                               v0[0], v0[1], v1[0], v1[1], v2[0], v2[1])
        self.normals = nrmls


pink = (255, 192, 203)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

if __name__ == '__main__':
    image1 = Image.new(mode='RGB', size=(2000, 2000))
    bunny = Model()
    bunny.parse_file('file.obj')
    bunny.draw_polygons(image1)
    image1.save("bunny.jpg")
    image1.show()
