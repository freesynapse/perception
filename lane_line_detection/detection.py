#!/usr/bin/python3

from application import Application

if __name__ == '__main__':

    # constants
    WIN_WIDTH, WIN_HEIGHT = 960, 540
    app = Application(WIN_WIDTH, WIN_HEIGHT)
    app.main_loop()

    exit()
