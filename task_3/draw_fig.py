import numpy as np
import math


def drawLine1(x0, y0, x1, y1, img, color):
    t = .0
    while t < 1.0:
        x = x0 * (1. - t) + x1 * t
        y = y0 * (1. - t) + y1 * t
        img.putpixel((int(x), int(y)), color)
        t += 0.01


def drawLine2(x0, y0, x1, y1, img, color):
    x = x0
    while x <= x1:
        t = (x - x0) / (float)(x1 - x0)
        y = y0 * (1. - t) + y1 * t
        x += 1
        img.putpixel((int(x), int(y)), color)


def drawLine3(x0, y0, x1, y1, img, color):
    steep = False
    if math.fabs(x0 - x1) < math.fabs(y0 - y1):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        steep = True
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    x = x0
    while x <= x1:
        t = (x - x0) / (float)(x1 - x0)
        y = y0 * (1. - t) + y1 * t
        if steep:
            img.putpixel((int(x), int(y)), color)
        else:
            img.putpixel((int(y), int(x)), color)
        x += 1



def lineBres(x0, y0, x1, y1, img, color):
    steep = False
    if math.fabs(x0 - x1) < math.fabs(y0 - y1):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        steep = True
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    dx = x1 - x0
    dy = y1 - y0
    derror = math.fabs(dy / float(dx))
    error = 0
    y = y0
    x = x0
    while x <= x1:
        if steep:
            img.putpixel((int(x), int(y)), color)
        else:
            img.putpixel((int(y), int(x)), color)
        error += derror
        if error > .5:
            if y1 > y0:
                y += 1
            else:
                y += -1
            error -= 1.
        x += 1


def draw_line(x1, y1, x2, y2, img, color):
    change = False
    if (np.abs(x2 - x1) < np.abs(y2 - y1)):
        x1, y1 = y1, x1
        x2, y2 = y2, x2
        change = True
    if (x1 > x2):
        x1, x2 = x2, x1
        y1, y2 = y2, y1
    dx = x2 - x1
    y = y1
    if (y2 > y1):
        step_y = 1
    else:
        step_y = -1
    derror = 2 * np.abs(y2 - y1)
    dsum = 0
    for x in range(x1, x2):
        if change:
            img.putpixel((int(y), int(x)), color)
        else:
            img.putpixel((int(x), int(y)), color)
        dsum += derror
        if (dsum > dx):
            dsum -= 2 * dx
            y += step_y


def drawTr(x0, y0, z0, x1, y1, z1, x2, y2, z2, z_buf, im, color):
    for j in range(int(min([y0, y1, y2])), int(max([y0, y1, y2])) + 1):
        for i in range(int(min([x0, x1, x2])), int(max([x0, x1, x2])) + 1):
            l0 = ((j - y2) * (x1 - x2) - (i - x2) * (y1 - y2)) / ((y0 - y2) * (x1 - x2) - (x0 - x2) * (y1 - y2))
            l1 = ((j - y0) * (x2 - x0) - (i - x0) * (y2 - y0)) / ((y1 - y0) * (x2 - x0) - (x1 - x0) * (y2 - y0))
            l2 = ((j - y1) * (x0 - x1) - (i - x1) * (y0 - y1)) / ((y2 - y1) * (x0 - x1) - (x2 - x1) * (y0 - y1))
            z = z0 * l0 + z1 * l1 + z2 * l2
            if l0 >= 0 and l1 >= 0 and l2 >= 0 and z < z_buf[i, j]:
                im.putpixel((i, j), color)
                z_buf[i, j] = z
