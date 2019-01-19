#!/usr/bin/env python
# -*- coding: utf8 -*-
from collections import OrderedDict
import csv
from Util2 import calculate_difference3, calculate_difference4
from Util import zero_change,normalize
import numpy as np
import math
import datetime
import json
import requests


def collect_data():
    date_time = []
    speyer = []
    mannheim = []
    worms = []
    mainz = []
    with open('data/rhein.csv', 'rb') as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        for row in f_csv:
            values = row[0].decode('utf-8').split(';')
            date_time.append(values[0])
            speyer.append(values[1])
            mannheim.append(values[2])
            worms.append(values[3])
            mainz.append(values[4])
    return date_time, speyer, mannheim, worms, mainz


def read_temperature():
    data = np.loadtxt("data/temperature.txt", delimiter="  ")
    indoor_temp = data[:, 0]
    outdoor_temp = data[:, 1]
    return indoor_temp, outdoor_temp


def read_daily_temperature():
    data = np.loadtxt("data/daily_temperature.txt", delimiter="	")
    index = data[:, 0]
    temp = data[:, 1]
    return index, temp

def as_num(x):
    y='{:.5f}'.format(x)
    return(y)


def conver_num(element):
    strings = element.split('e')
    base = float(strings[0])
    pow = math.pow(10,float(strings[1]))
    return base*pow



def read_stock_price():
    f = open("data/stock_price.txt")
    line = f.readline()
    x_price = []
    y_price = []
    while line:
        strings = line.split(" ")
        while len(strings)>2:
            for element in strings:
                if element=='':
                    strings.remove(element)
        x_price.append(conver_num(strings[0]))
        if strings[1][len(strings[1])-2]=='\n':
            y_price.append(conver_num(strings[1][0:len(strings[1])-1]))
        else:
            y_price.append(conver_num(strings[1][0:len(strings[1])]))
        line = f.readline()
    f.close()
    #for i in range(0,len(x_price)):
    #    x_price[i]=math.log(x_price[i],2)
    #    y_price[i] = math.log(y_price[i], 2)
    return x_price, y_price


def read_snow():
    f = open("data/snow.txt")
    line = f.readline()
    temp = []
    snow = []
    while line:
        strings = line.split("  ")
        while len(strings) > 2:
            for element in strings:
                if element == '' or element==' ':
                    strings.remove(element)
        temp.append(conver_num(strings[0]))
        if strings[1][len(strings[1]) - 2] == '\n':
            snow.append(conver_num(strings[1][0:len(strings[1]) - 1]))
        else:
            snow.append(conver_num(strings[1][0:len(strings[1])]))
        line = f.readline()
    f.close()
    return temp, snow


def read_solar():
    f = open("data/solar.txt")
    line = f.readline()
    temp = []
    solar = []
    while line:
        strings = line.split(" ")
        temp.append(float(strings[0]))
        if strings[1][len(strings[1]) - 2] == '\n':
            solar.append(float(strings[1][0:len(strings[1]) - 1]))
        else:
            solar.append(float(strings[1][0:len(strings[1])]))
        line = f.readline()
    f.close()
    return temp, solar


def read_ozone():
    data = np.loadtxt("data/ozone3.txt", delimiter="	")
    ozone = data[:, 0]
    temp = data[:, 1]
    return ozone, temp


def river_test():
    date_time, speyer, mannheim, worms, mainz = collect_data()
    counter = 0
    speyer_low = []
    mannheim_low = []
    worms_low = []
    mainz_low = []
    while counter<2880:
        speyer_low.append(speyer[counter])
        mannheim_low.append(mannheim[counter])
        worms_low.append(worms[counter])
        mainz_low.append(mainz[counter])
        counter+=1
    speyer = map(float,speyer_low)
    mannheim = map(float, mannheim_low)
    worms = map(float,worms_low)
    mainz = map(float,mainz_low)
    cause = speyer
    effect = mannheim
    cause = zero_change(cause)
    effect = zero_change(effect)
    sp2ma = calculate_difference3(cause, effect, 10)
    ma2sp = calculate_difference3(effect, cause, 10)
    print 'sp' + ' -> ' + 'ma' + ':' + str(sp2ma)
    print 'ma' + ' -> ' + 'sp' + ':' + str(ma2sp)
    print
    cause = speyer
    effect = worms
    cause = zero_change(cause)
    effect = zero_change(effect)
    sp2wo = calculate_difference3(cause, effect, 10)
    wo2sp = calculate_difference3(effect, cause, 10)
    print 'sp' + ' -> ' + 'wo' + ':' + str(sp2wo)
    print 'wo' + ' -> ' + 'sp' + ':' + str(wo2sp)
    print
    cause = speyer
    effect = mainz
    cause = zero_change(cause)
    effect = zero_change(effect)
    sp2mz = calculate_difference3(cause, effect, 10)
    mz2sp = calculate_difference3(effect, cause, 10)
    print 'sp' + ' -> ' + 'mz' + ':' + str(sp2mz)
    print 'mz' + ' -> ' + 'sp' + ':' + str(mz2sp)
    print
    cause = mannheim
    effect = worms
    cause = zero_change(cause)
    effect = zero_change(effect)
    ma2wo = calculate_difference3(cause, effect, 10)
    wo2ma = calculate_difference3(effect, cause, 10)
    print 'ma' + ' -> ' + 'wo' + ':' + str(ma2wo)
    print 'wo' + ' -> ' + 'ma' + ':' + str(wo2ma)
    print
    cause = mannheim
    effect = mainz
    cause = zero_change(cause)
    effect = zero_change(effect)
    ma2mz= calculate_difference3(cause, effect, 10)
    mz2ma = calculate_difference3(effect, cause, 10)
    print 'ma' + ' -> ' + 'mz' + ':' + str(ma2mz)
    print 'mz' + ' -> ' + 'ma' + ':' + str(mz2ma)
    print
    cause = worms
    effect = mainz
    cause = zero_change(cause)
    effect = zero_change(effect)
    wo2mz = calculate_difference3(cause, effect, 10)
    mz2wo = calculate_difference3(effect, cause, 10)
    print 'wo' + ' -> ' + 'mz' + ':' + str(wo2mz)
    print 'mz' + ' -> ' + 'wo' + ':' + str(mz2wo)
    print



def temperature_test():
    indoor_temp, outdoor_temp = read_temperature()
    cause = outdoor_temp
    effect = indoor_temp
    cause = zero_change(cause)
    effect = zero_change(effect)
    cause2effect = calculate_difference3(cause, effect, 10)
    effect2cause = calculate_difference3(effect, cause, 10)
    print 'cause' + ' -> ' + 'effect' + ':' + str(cause2effect)
    print 'effect' + ' -> ' + 'cause' + ':' + str(effect2cause)


def ozone_test():
    ozone, temp = read_ozone()
    cause = temp
    effect = ozone
    #cause = zero_change(cause)
    #effect = zero_change(effect)
    for i in range(5,6):
        cause2effect = calculate_difference3(cause, effect, i)
        effect2cause = calculate_difference3(effect, cause, i)
        print 'cause' + ' -> ' + 'effect' + ':' + str(cause2effect)
        print 'effect' + ' -> ' + 'cause' + ':' + str(effect2cause)
        p = math.pow(2, -(cause2effect - effect2cause))
        print p
from statsmodels.tsa.stattools import grangercausalitytests


def ozone_granger_test():
    x, y = read_stock_price()
    cause = x
    effect = y
    ce1 = grangercausalitytests([[effect[i], cause[i]] for i in range(0, len(cause))], 5)
    ce2 = grangercausalitytests([[cause[i], effect[i]] for i in range(0, len(cause))], 5)


def stock_test():
    x, y = read_stock_price()
    cause = map(float,x)
    effect = map(float,y)
    #cause = zero_change(cause)
    #effect = zero_change(effect)
    for i in range(3,5):
        cause2effect = calculate_difference3(cause, effect, i)
        effect2cause = calculate_difference3(effect, cause, i)
        print 'cause' + ' -> ' + 'effect' + ':' + str(cause2effect)
        print 'effect' + ' -> ' + 'cause' + ':' + str(effect2cause)
        p = math.pow(2, -(cause2effect - effect2cause))
        print p


def test_daily_temperature():
    index,temp = read_daily_temperature()
    counter = 0
    index_low = []
    temp_low = []
    while counter<len(index):
        index_low.append(index[counter])
        temp_low.append(temp[counter])
        counter+=30
    cause = index
    effect = temp
    cause = zero_change(cause)
    effect = zero_change(effect)
    cause2effect = calculate_difference4(cause, effect, 5)
    effect2cause = calculate_difference4(effect, cause, 5)
    print 'cause' + ' -> ' + 'effect' + ':' + str(cause2effect)
    print 'effect' + ' -> ' + 'cause' + ':' + str(effect2cause)


def test_solar():
    temp, solar = read_solar()
    cause = map(float, solar)
    effect = map(float, temp)
    cause = zero_change(cause)
    effect = zero_change(effect)
    cause2effect = calculate_difference3(cause, effect, 5)
    effect2cause = calculate_difference3(effect, cause, 5)
    print 'cause' + ' -> ' + 'effect' + ':' + str(cause2effect)
    print 'effect' + ' -> ' + 'cause' + ':' + str(effect2cause)


def test_snow():
    temp,snow = read_snow()
    cause = map(float, temp)
    effect = map(float, snow)
    cause = normalize(cause)
    cause = zero_change(cause)
    effect = normalize(effect)
    effect = zero_change(effect)
    cause2effect = calculate_difference3(cause, effect, 10)
    effect2cause = calculate_difference3(effect, cause, 10)
    print 'cause' + ' -> ' + 'effect' + ':' + str(cause2effect)
    print 'effect' + ' -> ' + 'cause' + ':' + str(effect2cause)


def no_causality_test():
    x, y = read_stock_price()
    a,b = read_ozone()
    cause = x[0:300]
    effect = a[0:300]
    ce1 = grangercausalitytests([[effect[i], cause[i]] for i in range(0, len(cause))], 5)
    ce2 = grangercausalitytests([[cause[i], effect[i]] for i in range(0, len(cause))], 5)


def causality_test():
    x, y = read_stock_price()
    a, b = read_ozone()
    cause = y[0:300]
    effect = b[0:300]
    cause = normalize(cause)
    cause = zero_change(cause)
    effect = normalize(effect)
    effect = zero_change(effect)
    cause2effect = calculate_difference3(cause, effect, 10)
    effect2cause = calculate_difference3(effect, cause, 10)
    print 'cause' + ' -> ' + 'effect' + ':' + str(cause2effect)
    print 'effect' + ' -> ' + 'cause' + ':' + str(effect2cause)
    p = math.pow(2, -(cause2effect - effect2cause))
    print p

#river_test()
#ozone_granger_test()
#stock_test()
causality_test()
