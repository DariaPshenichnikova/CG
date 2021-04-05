from draw_fig import *
from PIL import Image

if __name__ == "__main__":

    # 3 задание
    img = Image.new('L', (1000, 1000), "black")
    img1 = Image.new('L', (200, 200), "black")
    img2 = Image.new('L', (200, 200), "black")
    img3 = Image.new('L', (200, 200), "black")
    img4 = Image.new('L', (200, 200), "black")
    for i in range(12):
        drawLine1(100, 100, 100 + int(math.cos(i * 2 * math.pi / 13) * 95),
                  100 + int(math.sin(i * 2 * math.pi / 13) * 95), img1, 255)
    img1.show()
    for i in range(12):
        drawLine2(100, 100, 100 + int(math.cos(i * 2 * math.pi / 13) * 95),
                  100 + int(math.sin(i * 2 * math.pi / 13) * 95), img2, 255)
    img2.show("алгоритм 2")
    for i in range(12):
        drawLine3(100, 100, 100 + int(math.cos(i * 2 * math.pi / 13) * 95),
                  100 + int(math.sin(i * 2 * math.pi / 13) * 95), img3, 255)
    img3.show("алгоритм 3")
    for i in range(13):
        lineBres(100, 100, 100 + int(math.cos(i * 2 * math.pi / 13) * 95),
                 100 + int(math.sin(i * 2 * math.pi / 13) * 95), img4, 255)
    img4.show("алгоритм Брезенхема")

    # model = Model()
    # model.setPoints(model.parsOBJ())
    # points = model.getPoints()
    # count = 0
    # for i in range(len(model.getPoints())):
    #     img.putpixel(
    #         (int(50 * model.get2dPoint(count)[0]) + 500, int(50 * model.get2dPoint(count)[1] * (-1)) + 500), 255)
    #     count += 1
    # img.show()
