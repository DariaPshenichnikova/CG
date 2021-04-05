import numpy as np
from PIL import Image


class Model():
    def __init__(self):
        self.massivv = []

    def setarray(self, massiv):
        self.massivv = np.array(massiv)

    def getarray(self, i):
        return self.massivv[i]


def scale(position):
    position[0][0] = 4000 * position[0][0] + 500
    position[0][1] = -4000 * position[0][1] + 500
    return position


def draw_image(points, edges, color):
    image = Image.new(mode='RGB', size=(1000, 1000))
    pixels = image.load()
    #for i in points:
     #   pixels[8000 * i[0] + 500, -8000 * i[1] + 800] = color
    for triple in edges:
        vertex = np.empty((0, 3), dtype=np.int)
        for i in range(0, 3):
            vertex = np.append(vertex, [points[triple[i]]], axis=0)
        v0 = [vertex[0][0] * 8000 + 500, -vertex[0][1] * 8000 + 800, vertex[0][2]]
        v1 = [vertex[1][0] * 8000 + 500, -vertex[1][1] * 8000 + 800, vertex[1][2]]
        v2 = [vertex[2][0] * 8000 + 500, -vertex[2][1] * 8000 + 800, vertex[2][2]]
        # line_v3(v0[0], v0[1], v1[0], v1[1], image, color)
        # line_v3(v1[0], v1[1], v2[0], v2[1], image, color)
        # line_v3(v2[0], v2[1], v0[0], v0[1], image, color)
        n = normal(vertex[0][0], vertex[0][1], vertex[0][2], vertex[1][0], vertex[1][1], vertex[1][2], vertex[2][0], vertex[2][1], vertex[2][2])
        print(n)
        norm = np.sqrt(n[0]**2 + n[1]**2 + n[2]**2)
        mult = n[2]/norm

        if n[2] < 0:
            triangle(v0[0], v0[1], v1[0], v1[1], v2[0], v2[1], image, (int(-255*mult), int(-255*mult), int(-255*mult)))
    image.show()


def parse_file(filename):
    file = open(filename, 'r')
    points = np.empty((0, 3), dtype=np.float)
    edges = np.empty((0, 3), dtype=np.int)
    flag = False
    while True:
        line = file.readline()
        line_array = line.split(' ')
        if line_array[0] == 'v':
            line_array = [float(i) for i in line_array[1:]]
            points = np.append(points, [line_array], axis=0)
        elif line_array[0] == 'f':
            line_array = [(int(i[0:i.find("/")]) - 1) for i in line_array[1:]]
            edges = np.append(edges, [line_array], axis=0)
            flag = True
        elif flag == True:
            break
    return points, edges


def line_v1(x0, y0, x1, y1, image, color):
    pixels = image.load()
    for t in np.arange(0.0, 1.0, 0.01):
        x = x0 * (1.0 - t) + x1 * t
        y = y0 * (1.0 - t) + y1 * t
        pixels[x, y] = color


def line_v2(x0, y0, x1, y1, image, color):
    pixels = image.load()

    steep = abs(x0 - x1) < abs(y0 - y1)
    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    for x in range(x0, x1, 1):
        t = (x - x0) / (x1 - x0)
        y = y0 * (1 - t) + y1 * t
        if steep:
            pixels[y, x] = color
        else:
            pixels[x, y] = color


def line_v3(x0, y0, x1, y1, image, color):
    x0 = int(x0)
    y0 = int(y0)
    x1 = int(x1)
    y1 = int(y1)

    pixels = image.load()
    steep = abs(x0 - x1) < abs(y0 - y1)
    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dx = x1 - x0
    dy = y1 - y0
    derror = abs(dy) * 2
    error = 0
    sy = 1 if (y1 > y0) else -1
    y = y0

    for x in range(x0, x1):
        if steep:
            pixels[y, x] = color
        else:
            pixels[x, y] = color
        error += derror
        if error > dx:
            y += sy
            error -= 2 * dx


def to_rectangular(phi, r, center):
    return int(r * np.cos(phi) + center[0]), int(r * np.sin(phi) + center[1])


def triangle(x0, y0, x1, y1, x2, y2, image, color):
    center = (500, 500)
    pixels = image.load()
    #random.seed(version=2)
    #color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    line_v3(x0, y0, x1, y1, image, color)
    line_v3(x1, y1, x2, y2, image, color)
    line_v3(x0, y0, x2, y2, image, color)
    a = [x0,  x1, x2]
    b = [y0,  y1, y2]
    xmin = min(a)
    xmax = max(a)
    ymin = min(b)
    ymax = max(b)
    denominator1 = (y0-y2) * (x1-x2) - (x0-x2) * (y1-y2)
    denominator2 = ((y1-y0) * (x2-x0) - (x1 - x0) * (y2-y0))
    denominator3 = ((y2-y1) * (x0-x1) - (x2-x1) * (y0-y1))
    x0x1 = x0 - x1
    x1x2 = x1 - x2
    y1y2 = y1 - y2
    y0y2 = y0 - y2
    x0x2 = x0 - x2
    y0y1 = y0 - y1
    for x in range(int(xmin), int(xmax)+1):
        for y in range(int(ymin), int(ymax)+1):
            lyam0 = ((y - y2) * x1x2 - (x - x2) * y1y2) / denominator1
            lyam1 = ((y - y0) * (-x0x2) - (x - x0) * (-y0y2)) / denominator2
            lyam2 = ((y - y1) * x0x1 - (x - x1) * y0y1) / denominator3
            if lyam0 >= 0 and lyam1 >= 0 and lyam2 >= 0:
                pixels[x, y] = color

def normal(x0, y0, z0, x1, y1, z1, x2, y2, z2):
    norm = (((y2-y0)*(z1-z0)-(z2-z0)*(y1-y0)), -((x2-x0)*(z1-z0)-(z2-z0)*(x1-x0)), ((x2-x0)*(y1-y0)-(y2-y0)*(x1-x0)))
    return norm
    #scalar = norm[0]*v[0] + norm[1]*v[1] + norm[2]*v[2]




# 1
image = Image.new(mode='RGB', size=(1000, 1000))
center = (500, 500)
white = (255, 255, 255)

# for phi in np.arange(0, 2 * np.pi, 1.0 / 9.0 * np.pi):
#   (x, y) = to_rectangular(phi, 500, center)
#  line_v3(center[0], center[1], x, y, image, white)


# 2
(points, edges) = parse_file("../file.obj")
draw_image(points, edges, white)
x0 = 500
y0 = 500
x1 = 300
y1 = 300
x2 = 700
y2 = 300
# triangle(x0, y0, x1, y1, x2, y2, image, white);
# image.show()



# m1 = Model()
# m1.setarray(np.array([[1,2,3],[4,5,6]]))
# print(m1.getarray(1))
# draw_image()
