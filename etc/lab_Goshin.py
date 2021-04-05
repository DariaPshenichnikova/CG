import PIL.Image
import numpy as np
import random
import math


class Shader:

    def __init__(self):
        self.temporary_solution = np.zeros((3, 3), np.float)
        self.intensity = 0
        self.back = True

    def vertex_shader(self, model, poly_number, vertex_number, camera):
        vertex = model.vertices[model.polygon_vertices[poly_number][vertex_number] - 1]
        # vertex[0][0:2] = (-0.046146 0.050437 0.002961)
        # (X,Y,Z) -> (4000*X + 500, -4000*Y + 500)
        camera_vertex = np.array(
            [vertex[0] * camera.scale + camera.dx, -vertex[1] * camera.scale + camera.dy, vertex[2]])

        self.temporary_solution[vertex_number] = np.array(vertex)

        if (vertex_number == 2):
            # Ребра полигона
            d1 = self.temporary_solution[1] - self.temporary_solution[0]
            d2 = self.temporary_solution[2] - self.temporary_solution[0]
            # Нормаль к полигона
            normal = np.cross(d1, d2)
            normal = normal / np.linalg.norm(normal)
            # z-координата определяет, направлена ли грань полигона к наблюдателю или от него
            if (normal[2] > 0):
                self.back = True
            else:
                self.back = False
            self.intensity = int(round(-255.0 * normal[2]))
        return camera_vertex

    def fragment_shader(self, barycentric, camera, model):
        color = (self.intensity, self.intensity, self.intensity)
        return self.back, color


class SmoothShader:

    def __init__(self):
        # Яркости трёх вершин полигона
        self.vertex_intensity = np.zeros(3, np.float)

    def vertex_shader(self, model, poly_number, vertex_number, camera):
        vertex = model.vertices[model.polygon_vertices[poly_number][vertex_number] - 1]
        # vertex[0][0:2] = (-0.046146 0.050437 0.002961)
        # (X,Y,Z) -> (4000*X + 500, -4000*Y + 500)

        new_vertex = model.rotation @ vertex + model.translation
        new_vertex = new_vertex / new_vertex[2]
        # new_vertex[2] = 1.0
        camera_vertex = camera.intrinsic @ new_vertex
        camera_vertex[2] = vertex[2]

        # camera_vertex = np.array([vertex[0]*camera.scale + camera.dx, -vertex[1]*camera.scale + camera.dy, vertex[2]])

        # При повороте модели необходимо поворачивать нормали
        self.vertex_intensity[vertex_number] = \
            model.normals[model.polygon_normals[poly_number][vertex_number] - 1][2]

        return camera_vertex

    def fragment_shader(self, barycentric, camera, model):
        # z-координата нормали к конкретному пикселю
        intensity = int(round(-255 * np.dot(barycentric, self.vertex_intensity)))
        if (intensity < 0):
            return True, (0, 0, 0)
        else:
            return False, (intensity, intensity, intensity)


class Model:

    def __init__(self, filename):
        self.vertices = np.empty((0, 3), np.float)
        self.normals = np.empty((0, 3), np.float)
        self.polygon_vertices = np.empty((0, 3), np.int)
        self.polygon_normals = np.empty((0, 3), np.int)

        # Сдвиг и поворот модели
        self.translation = np.array([0.0, -0.05, 0.1], dtype=np.float)
        self.rotation = np.eye(3, dtype=np.float)

        handle = open(filename, "r")
        for line in handle:
            values = line.split()
            if len(values) == 0:
                continue
            if values[0] == "v":
                self.vertices = np.append(self.vertices,
                                          np.array([[float(values[1]), float(values[2]), float(values[3])]]), axis=0)
            if values[0] == "vn":
                self.normals = np.append(self.normals,
                                         np.array([[float(values[1]), float(values[2]), float(values[3])]]), axis=0)
            elif values[0] == "f":
                f0 = values[1].split('/')
                f1 = values[2].split('/')
                f2 = values[3].split('/')
                self.polygon_vertices = np.append(self.polygon_vertices,
                                                  np.array([[int(f0[0]), int(f1[0]), int(f2[0])]]), axis=0)
                self.polygon_normals = np.append(self.polygon_normals, np.array([[int(f0[2]), int(f1[2]), int(f2[2])]]),
                                                 axis=0)
        handle.close()


class Camera:
    def __init__(self, width, height, scale, dx, dy):
        self.canvas = np.zeros((height, width, 3), dtype=np.uint8)
        self.z_buffer = np.full((height, width), np.Inf, dtype=np.float)
        self.width = width
        self.height = height
        self.scale = float(scale)
        self.dx = dx
        self.dy = dy
        #
        self.intrinsic = np.array([[self.scale, 0.0, width / 2], [0.0, -self.scale, height / 2], [0.0, 0.0, 1.0]],
                                  np.float)

    def show_image(self):
        im = PIL.Image.fromarray(self.canvas, mode='RGB')
        im.show()

    def save_image(self, filename):
        im = PIL.Image.fromarray(self.canvas, mode='RGB')
        im.save(filename)


def barycentric(v0, v1, v2, x, y):
    x0, y0 = v0[0], v0[1]
    x1, y1 = v1[0], v1[1]
    x2, y2 = v2[0], v2[1]

    l0 = ((y - y2) * (x1 - x2) - (x - x2) * (y1 - y2)) / ((y0 - y2) * (x1 - x2) - (x0 - x2) * (y1 - y2))
    l1 = ((y - y0) * (x2 - x0) - (x - x0) * (y2 - y0)) / ((y1 - y0) * (x2 - x0) - (x1 - x0) * (y2 - y0))
    l2 = ((y - y1) * (x0 - x1) - (x - x1) * (y0 - y1)) / ((y2 - y1) * (x0 - x1) - (x2 - x1) * (y0 - y1))
    return np.array([l0, l1, l2], dtype=np.float)


if __name__ == "__main__":
    m = Model("Duck.obj")
    # cam = Camera(1920, 1080, 9000.0, 960, 1000)
    cam = Camera(640, 480, 300.0, 320, 400)

    # sh = Shader()
    sh = SmoothShader()

    c_vertex = np.zeros((3, 3), np.float)
    # Для каждого полигона
    for poly_number in range(m.polygon_vertices.shape[0]):
        # Возвращаем экранные координаты трёх вершин
        # в формате (x-экранная, y-экранная, z-исходная)
        c_vertex[0] = sh.vertex_shader(m, poly_number, 0, cam)
        c_vertex[1] = sh.vertex_shader(m, poly_number, 1, cam)
        c_vertex[2] = sh.vertex_shader(m, poly_number, 2, cam)

        # В наличии 3 пары экранных координат (x,y)
        # В шейдере хранятся сведения о необходимости отрисовки и интенсивности

        # min(c_vertex[0][0], c_vertex[1][0], c_vertex[2][0]) – определение "левой" границы
        # max(левая граница, 0)

        x_min = max(int(math.floor(min(c_vertex[0][0], c_vertex[1][0], c_vertex[2][0]))), 0)
        y_min = max(int(math.floor(min(c_vertex[0][1], c_vertex[1][1], c_vertex[2][1]))), 0)

        x_max = min(int(math.ceil(max(c_vertex[0][0], c_vertex[1][0], c_vertex[2][0]))), cam.width)
        y_max = min(int(math.ceil(max(c_vertex[0][1], c_vertex[1][1], c_vertex[2][1]))), cam.height)

        for x in range(x_min, x_max):
            for y in range(y_min, y_max):
                l = barycentric(c_vertex[0], c_vertex[1], c_vertex[2], x, y)
                # Вычисление z-координаты точки, соответсвующей пикселю
                z = l[0] * c_vertex[0, 2] + l[1] * c_vertex[1, 2] + l[2] * c_vertex[2, 2]
                if (l[0] > 0 and l[1] > 0 and l[2] > 0 and cam.z_buffer[y][x] > z):
                    discard, color = sh.fragment_shader(l, cam, m)
                    if (not discard):
                        cam.canvas[y][x] = color
                        cam.z_buffer[y][x] = z

    cam.show_image()
    cam.save_image("result.png")