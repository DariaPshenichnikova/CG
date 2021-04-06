from drawer import *
from PIL import Image

from model import Model

if __name__ == "__main__":
    # 1 задание
    H = 100
    W = 100

    black_matrix = np.zeros((H, W), dtype=np.uint8)
    black_img = Image.fromarray(black_matrix, "L")
    black_img.show("Black image")

    white_matrix = np.full((H, W), 255, dtype=np.uint8)
    white_img = Image.fromarray(white_matrix, "L")
    white_img.show("White image")

    red_matrix = np.zeros((H, W, 3), dtype=np.uint8)
    for x in range(H):
        for y in range(W):
            red_matrix[x][y][0] = 255
    red_img = Image.fromarray(red_matrix, "RGB")
    red_img.show("Red image")

    gradient_matrix = np.zeros((H, W, 3), dtype=np.uint8)
    for x in range(H):
        for y in range(W):
            for z in range(3):
                gradient_matrix[x][y][z] = (x + y + z) % 256
    gradient_img = Image.fromarray(gradient_matrix, "RGB")
    gradient_img.show("Gradient image")

    # 3 задание
    img1 = Image.new('L', (200, 200), "black")
    img2 = Image.new('L', (200, 200), "black")
    img3 = Image.new('L', (200, 200), "black")
    img4 = Image.new('L', (200, 200), "black")

    for i in range(13):
        drawLine1(100, 100, 100 + int(math.cos(i * 2 * math.pi / 13) * 95),
                  100 + int(math.sin(i * 2 * math.pi / 13) * 95), img1, 255)
    img1.show("Aлгоритм 1")

    for i in range(13):
        drawLine2(100, 100, 100 + int(math.cos(i * 2 * math.pi / 13) * 95),
                  100 + int(math.sin(i * 2 * math.pi / 13) * 95), img2, 255)
    img2.show("Aлгоритм 2")

    for i in range(13):
        drawLine3(100, 100, 100 + int(math.cos(i * 2 * math.pi / 13) * 95),
                  100 + int(math.sin(i * 2 * math.pi / 13) * 95), img3, 255)
    img3.show("Aлгоритм 3")

    for i in range(13):
        lineBres(100, 100, 100 + int(math.cos(i * 2 * math.pi / 13) * 95),
                 100 + int(math.sin(i * 2 * math.pi / 13) * 95), img4, 255)
    img4.show("Aлгоритм Брезенхема")

    # задания 4-7
    model = Model()
    model.parse_file('../file.obj')

    vertex_image = Image.new(mode='RGB', size=(1000, 1000))
    model.draw_vertexes(vertex_image, (255, 0, 0))

    faces_image = Image.new(mode='RGB', size=(2000, 2000))
    model.draw_faces(faces_image, (255, 0, 0))
