from PIL import Image
import numpy as np

from task_3.draw_fig import drawTr


class Model:

    def __init__(self):
        self.__points = np.empty(shape=[0, 3], dtype=np.float32)
        self.__polyg = np.empty(shape=[0, 3], dtype=np.int)

    def parsOBJ(self):
        with open('../file.obj', 'r') as objFile:
            for line in objFile:
                split = line.split()
                # считываем из файла для №4
                if split[0] == "v":
                    self.__points = np.append(self.__points, [[float(split[1]), float(split[2]), float(split[3])]],
                                              axis=0)
                # считываем из файла для №6
                if split[0] == "f":
                    new_split1 = split[1].split('/')
                    new_split2 = split[2].split('/')
                    new_split3 = split[3].split('/')
                    self.__polyg = np.append(self.__polyg,
                                             [[int(new_split1[0]), int(new_split2[0]), int(new_split3[0])]], axis=0)

    def getPoints(self):
        return self.__points

    def getPolygon(self):
        return self.__polyg

    def setPoints(self, points):
        self.__points = points

    def setPolygon(self, polyg):
        self.__polyg = polyg

    def get3dPoint(self, id):
        return self.__points[id]

    def get2dPoint(self, id):
        return self.__points[id, (0, 1)]

    def drawModel(self):
        n, m = 1000, 1000
        im = Image.new('L', (n, m), "black")
        z_buf = np.full((n, m), np.Inf, dtype=np.float)

        for poly in self.__polyg:
            x0 = 5000 * self.__points[poly[0] - 1][0] + 500
            y0 = -(5000 * self.__points[poly[0] - 1][1] + 500)
            z0 = 5000 * self.__points[poly[0] - 1][2] + 500
            x1 = 5000 * self.__points[poly[1] - 1][0] + 500
            y1 = -(5000 * self.__points[poly[1] - 1][1] + 500)
            z1 = 5000 * self.__points[poly[1] - 1][2] + 500
            x2 = 5000 * self.__points[poly[2] - 1][0] + 500
            y2 = -(5000 * self.__points[poly[2] - 1][1] + 500)
            z2 = 5000 * self.__points[poly[2] - 1][2] + 500

            d1 = self.__points[poly[1] - 1] - self.__points[poly[0] - 1]
            d2 = self.__points[poly[2] - 1] - self.__points[poly[0] - 1]

            n = np.cross(d1, d2)
            n /= np.linalg.norm(n)

            if n[2] <= 0:
                drawTr(x0, y0, z0, x1, y1, z1, x2, y2, z2, z_buf, im, int(n[2] * (-255)))
            else:
                continue
        im.show()
        im.save('Rabbit.jpg')
