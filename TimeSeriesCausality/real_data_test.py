#!/usr/bin/env python
# -*- coding: utf8 -*-
from collections import OrderedDict
import csv
from Util2 import calculate_difference3, calculate_difference4,change_to_zero_one
from Util import zero_change,normalize
import numpy as np
import math
import xlrd
from Util2 import zero_change
from snml import bernoulli2,cbernoulli2,bernoulli,cbernoulli
import datetime
import json
import requests
import matplotlib.pyplot as plt
from granger_test import granger

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


def read_hydraulic_pressure(name):
    worksheet = xlrd.open_workbook('data/2-20.xlsx')
    #sheet_names = worksheet.sheet_names()
    sheet = worksheet.sheet_by_name(name)
    time = sheet.col_values(0)[1:10000]
    control = sheet.col_values(1)[1:10000]
    valve_position = sheet.col_values(2)[1:10000]
    system_pressure = sheet.col_values(3)[1:10000]
    a_pressure = sheet.col_values(4)[1:10000]
    b_pressure = sheet.col_values(5)[1:10000]
    t_pressure = sheet.col_values(6)[1:10000]
    flow = sheet.col_values(7)[1:2000]
    valve_pressure = sheet.col_values(8)[1:10000]
    load = sheet.col_values(9)[1:10000]
    return time,control,valve_position,system_pressure,a_pressure,b_pressure,t_pressure,flow,valve_pressure,load


def read_cause_effect(file_name):
    worksheet = xlrd.open_workbook(file_name)
    sheet = worksheet.sheet_by_name('Sheet1')
    cause = sheet.col_values(1)[1:-1]
    effect = sheet.col_values(7)[1:-1]
    return cause,effect


def read_long_data(sub_length):
    cause1,effect1 = read_cause_effect('data/subsample.xlsx')
    #cause2, effect2 = read_cause_effect('data/5.0.xlsx')
    #cause3, effect3 = read_cause_effect('data/7.5.xlsx')
    #cause4, effect4 = read_cause_effect('data/10.xlsx')
    cause = []
    effect = []
    cause.extend(cause1)
    #cause.extend(cause2)
    #cause.extend(cause3)
    #cause.extend(cause4)
    effect.extend(effect1)
    #effect.extend(effect2)
    #effect.extend(effect3)
    #effect.extend(effect4)

    #cause_tmp = list(cause)
    #effect_tmp = list(effect)
    #for i in range(0,4):
    #    cause.extend(list(cause_tmp))
    #    effect.extend(list(effect_tmp))
    cause_sub = []
    effect_sub = []
    i=0
    while i < len(cause):
        #cause_sub.append(cause[i])
        #effect_sub.append(effect[i])

        if i+sub_length<len(cause):
            cause_sub.append(sum(cause[i:i+sub_length])/sub_length)
            effect_sub.append(sum(effect[i:i+sub_length])/sub_length)
        else:
            cause_sub.append(sum(cause[i:-1]) / (len(cause)-i))
            effect_sub.append(sum(effect[i:-1]) / (len(cause)-i))

        i+=sub_length
    return cause_sub,effect_sub




def read_sin_data():
    worksheet = xlrd.open_workbook('data/4.xlsx')
    sheet = worksheet.sheet_by_name('Sheet1')
    time = sheet.col_values(0)[1:-1]
    input = sheet.col_values(1)[1:-1]
    output1 = sheet.col_values(2)[1:-1]
    output2 = sheet.col_values(3)[1:-1]
    output3 = sheet.col_values(4)[1:-1]
    return input,output1,output2,output3


def collect_data2():
    date_time = []
    fremersdorf = []
    hanweiler = []
    sanktarnual = []
    with open('data/saar.csv', 'rb') as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        for row in f_csv:
            values = row[0].decode('utf-8').split(';')
            date_time.append(values[0])
            fremersdorf.append(values[1])
            hanweiler.append(values[2])
            sanktarnual.append(values[3])
    return date_time, fremersdorf, hanweiler, sanktarnual


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
    f = open("data/stock_price3.txt")
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


def river_test2():
    date_time, fremersdorf, hanweiler, sanktarnual = collect_data2()
    fremersdorf = map(float,fremersdorf)
    hanweiler = map(float, hanweiler)
    sanktarnual = map(float, sanktarnual)
    fremersdorf = zero_change(fremersdorf)
    hanweiler = zero_change(hanweiler)
    sanktarnual = zero_change(sanktarnual)
    delta_fr_to_hw = calculate_difference3(fremersdorf,hanweiler,10)
    delta_hw_to_fr = calculate_difference3(hanweiler,fremersdorf,10)
    print "fr->hw =", delta_fr_to_hw, " hw->fr =", delta_hw_to_fr

    delta_sa_to_hw =calculate_difference3(sanktarnual,hanweiler,10)
    delta_hw_to_sa = calculate_difference3(hanweiler,sanktarnual,10)
    print "sa->hw =", delta_sa_to_hw, " hw->sa =", delta_hw_to_sa

    delta_fr_to_sa = calculate_difference3(fremersdorf,sanktarnual,10)
    delta_sa_to_fr = calculate_difference3(sanktarnual,fremersdorf,10)
    print "fr->sa =", delta_fr_to_sa, " sa->fr =", delta_sa_to_fr


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
    #x, y = read_ozone()
    date_time, fremersdorf, hanweiler, sanktarnual = collect_data2()
    #date_time, speyer, mannheim, worms, mainz = collect_data()
    #speyer = map(float, speyer)
    #mannheim = map(float, mannheim)
    #worms = map(float, worms)
    #mainz = map(float, mainz)

    fremersdorf = map(float,fremersdorf)
    hanweiler = map(float,hanweiler)
    sanktarnual = map(float,sanktarnual)
    cause = hanweiler
    effect = sanktarnual
    #ce1 = grangercausalitytests([[effect[i], cause[i]] for i in range(0, len(cause))], 5)
    #ce2 = grangercausalitytests([[cause[i], effect[i]] for i in range(0, len(cause))], 5)
    p1 = granger(cause,effect,-1)
    p2 = granger(effect,cause,-1)
    print p1
    print p2


def stock_test():
    x, y = read_stock_price()
    cause = map(float,x)
    effect = map(float,y)
    #cause = zero_change(cause)
    #effect = zero_change(effect)
    for i in range(5,6):
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


def test_h():
    counter=0
    for i in range(1,2):
        time, control, valve_position, system_pressure, a_pressure, b_pressure, t_pressure, flow, valve_pressure, load = read_hydraulic_pressure('Sheet'+str(i))
        cause = control
        effect = valve_position

        #cause,effect = read_long_data(200)
        #cause = normalize(cause)
        cause = zero_change(cause)
        #effect = normalize(effect)
        effect = zero_change(effect)
        cause2effect = calculate_difference3(cause, effect, 10)
        effect2cause = calculate_difference3(effect, cause, 10)
        print 'cause' + ' -> ' + 'effect' + ':' + str(cause2effect)
        print 'effect' + ' -> ' + 'cause' + ':' + str(effect2cause)
        p = math.pow(2, -(cause2effect - effect2cause))
        if p<0.05:
            counter+=1
        print p
    #print counter


def test_granger_h():
    counter = 0
    for i in range(1, 2):
        time, control, valve_position, system_pressure, a_pressure, b_pressure, t_pressure, flow, valve_pressure, load = read_hydraulic_pressure(
            'Sheet' + str(i))
        cause = b_pressure
        effect = valve_pressure
        #cause, effect = read_long_data(200)
        p1 = granger(cause, effect, -1)
        p2 = granger(effect, cause, -1)
        print p1
        print p2
        if p1<0.05 and p2>0.05:
            counter+=1
    #print counter


def test_sin():
    input, output1, output2, output3 = read_sin_data()

    noise1 = np.random.normal(0, 0.1, 0)
    noise2 = np.random.normal(0, 0.1, 0)
    cause = list(input[0:112])
    # cause.extend(noise1)
    cause.extend(list(input[112:-1]))
    effect = list(output1[0:112])
    # effect.extend(noise2)
    effect.extend(list(output1[112:-1]))

    for i in range(0,len(effect)):
        effect[i] = effect[i]+np.random.normal(0, 0.1, 1)[0]


    #cause = input
    #effect = output3
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


def test_sin_granger():
    input, output1, output2, output3 = read_sin_data()


    cause = input
    effect = output2
    p1 = granger(cause, effect, -1)
    p2 = granger(effect, cause, -1)
    print p1
    print p2


def test_CUTE(length):
    #time, control, valve_position, system_pressure, a_pressure, b_pressure, t_pressure, flow, valve_pressure, load = read_hydraulic_pressure(
    #    'Sheet1')
    #input, output1, output2, output3 = read_sin_data()
    #cause = control
    #cause.extend(noise1)
    #effect = valve_position
    #for i in range(0,len(effect)):
        #effect[i] = effect[i]+np.random.normal(0, 0.1, 1)[0]
    #cause, effect = read_long_data(100)
    #plt.plot(cause)
    #plt.plot(effect)
    ozone,temp = read_ozone()
    cause = temp
    effect = ozone
    cause = change_to_zero_one(cause)
    effect = change_to_zero_one(effect)
    #cause2effect = bernoulli(effect) - cbernoulli(effect, cause)
    #effect2cause = bernoulli(cause) - cbernoulli(cause, effect)
    cause2effect = bernoulli2(effect,length) - cbernoulli2(effect, cause,length)
    effect2cause = bernoulli2(cause,length) - cbernoulli2(cause, effect,length)
    print cause2effect
    print effect2cause
    p = math.pow(2, -(cause2effect - effect2cause))
    print p
    plt.show()


#river_test()
ozone_granger_test()
#stock_test()
#causality_test()
#ozone_test()
#river_test2()
#read_hydraulic_pressure()

#test_h()
#test_granger_h()

#test_CUTE(5)
#test_sin()
#test_sin_granger()
