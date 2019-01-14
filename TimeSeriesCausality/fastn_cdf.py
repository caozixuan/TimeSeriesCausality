from fastncdf_data import *


def fastncdf_pos(x):
    if x>=fastncdf_max:
        return 1.0
    i = int(x*fastncdf_hinv)
    w = (x-fastncdf_x[i])*fastncdf_hinv
    return w*fastncdf_y[i+1]+(1.0-w)*fastncdf_y[i]


def fastncdf(x):
    if x<0:
        return 1.0 - fastncdf_pos(-x)
    return fastncdf_pos(x)