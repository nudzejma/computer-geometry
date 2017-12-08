import random

import time

from tkinter import *

from math import sqrt

from modules.primitives import get_simple_polygon
from structures.point import Point


class Tacka(object):
    # brojac=0
    def __init__(self, x1, y1):
        self.x = x1
        self.y = y1

    def pomjeri_se(self, dx, dy):
        self.x += dx
        self.y += dy

    def __str__(self):
        return "Tacka(%s,%s)" % (self.x, self.y)

    def dajX(self):
        return self.x

    def dajY(self):
        return self.y

    def udaljenost(self, p):
        dx = self.x - p.x
        dy = self.y - p.y
        return math.sqrt(dx ** 2 + dy ** 2)
#
# kP = Tk()
# kP.title("Primitive kompjuterske geometrije")
# kP.geometry("500x500")
# ok = Frame(kP)
# ok.pack()
# sirina_platna = 500
# visina_platna = 500
#
# tac = Tacka(0, 0)

canvas_width = 500
canvas_height = 500
point = Point(0,0)



def clean_canvas():
    canvas.delete("all")
    # lab1.configure(text="")


def generate():
    color = "red"
    points[:] = []

    for i in range(10):
        point = Point(random.randint(10, canvas_width-10), random.randint(10, canvas_height-10))
        while point in points:
            point =  Point(random.randint(10, canvas_width-10), random.randint(10, canvas_height-10))

        points.append(point)
        canvas.create_oval(int(point.get_x() - 3), int(point.get_y() - 3), int(point.get_x() + 3), int(point.get_y() + 3), fill=color)

    # p = Point(250,350)
    # canvas.create_oval(int(p.get_x() - 3), int(p.get_y() - 3), int(p.get_x() + 3), int(p.get_y() + 3), fill="green")
    # print('generating', points)

def draw_point(event):
    boja = "#476042"
    global point
    x1, y1 = (event.x - 10), (event.y - 10)
    x2, y2 = (event.x + 10), (event.y + 10)
    canvas.create_oval(x1, y1, x2, y2, fill="yellow")
    point = Point(event.x, event.y)

points = []

def simple_polygon(points):
    print(points)
    points = get_simple_polygon(points)
    i = 0
    length = len(points)
    while i<length:
        canvas.create_line(points[i].x, points[i].y, points[(i + 1)%length].x, points[(i + 1)%length].y)
        i += 1
    # canvas.create_polygon(points)

window = Tk()
window.title('Computer geometry framework')
window.geometry("600x600")
frame = Frame(window)
frame.pack()

canvas = Canvas(window, width=canvas_width, height=canvas_height, borderwidth=0, highlightthickness=10, bg="yellow")
# canvas.bind("<Button-1>", draw_point())
canvas.pack()

clean_button = Button(frame)
clean_button.configure(text="Clean canvas")
clean_button["command"] = clean_canvas
clean_button.pack()

generate_button = Button(frame)
generate_button.configure(text="Generate")
generate_button["command"] = generate
generate_button.pack()

simple_polygon_button = Button(frame)
simple_polygon_button.configure(text="Generate simple polygon")
simple_polygon_button["command"] = simple_polygon(points)
simple_polygon_button.pack()


window.mainloop()

