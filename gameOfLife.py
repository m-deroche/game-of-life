#! /bin/python3

import pyglet
from pyglet import shapes
import sys
import time


class board():
    white = (255, 255, 255)
    black = (0, 0, 0)
    grey = (122, 122, 122)

    def __init__(self, filePath):
        with open(filePath) as file:
            lines = file.readlines()

        self.canvasSquareSize = 10
        self.height = len(lines)
        self.width = len(lines[1]) - 1
        self.canvasHeight = self.height * self.canvasSquareSize
        self.canvasWidth = self.width * self.canvasSquareSize
        self.array = []


        self.batch = pyglet.graphics.Batch()
        self.window = pyglet.window.Window(self.canvasWidth, self.canvasHeight)

        for i in range(self.height):
            row = []
            for j in range(self.width):
                if lines[i][j] == '0':
                    alive = False
                    col = self.black
                else:
                    alive = True
                    col = self.white
                square = shapes.BorderedRectangle(self.canvasSquareSize * j, \
                                                  self.canvasSquareSize * (self.height - i - 1), \
                                                  self.canvasSquareSize, \
                                                  self.canvasSquareSize, \
                                                  color=col, \
                                                  border_color=self.black, \
                                                  batch=self.batch)
                row.append((alive, square))
            self.array.append(row)

    def changeCell(self, x, y):
        irgb = 255 - self.array[y][x][1].color[0]
        irgb = (irgb, irgb, irgb)
        self.array[y][x][1].color = irgb
        self.array[y][x] = (not self.array[y][x][0], self.array[y][x][1])

    def countNeighbours(self, x, y):
        count = 0

        for i in range(-1, 2, 1):
            for j in range(-1, 2, 1):
                if i != 0 or j != 0:
                    try:
                        val = self.alive(x + j, y + i)
                    except:
                        val = 0
                    count += val
        return count

    def alive(self, x, y):
        return self.array[y][x][0]

    def nextBoard(self):
        toChange = []
        for y in range(self.height):
            for x in range(self.width):
                neighbours = self.countNeighbours(x, y)

                if not self.alive(x, y):
                    if neighbours == 3:
                        toChange.append((x, y))
                else:
                    if neighbours != 2 and neighbours != 3:
                        toChange.append((x, y))
        for coord in toChange:
            self.changeCell(coord[0], coord[1])

def gameOfLife(file):
    b = board(file)

    @b.window.event
    def on_draw():
        b.batch.draw()
        b.nextBoard()
        time.sleep(0.05)

    pyglet.app.run()


if __name__ == "__main__":
    gameOfLife(sys.argv[1])
