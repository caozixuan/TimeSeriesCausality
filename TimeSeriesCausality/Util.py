# encoding:utf-8
from sklearn import preprocessing
import numpy as np
from scipy import *
import os
import scipy.stats
import math
import xlrd

from simulate import generate_continue_data
from fastn_cdf import fastncdf


def asymmetricKL(P, Q):
    return sum(P * log(P / Q))  # calculate the kl divergence between P and Q


from math import log


def lg(x):
    res = 0
    try:
        res = log(x, 2)
    except ValueError:
        pass
    return res


def exp(x):
    return 2 ** x


def reverse_argsort(X):
    indices = range(len(X))
    indices.sort(key=X.__getitem__, reverse=True)
    return indices


def symmetricalKL(P, Q):
    return (asymmetricKL(P, Q) + asymmetricKL(Q, P)) / 2.00


# 读取的是近十年加拿大的经济各个指标数据
def get_data():
    title_name = ['GDP', 'CPI', 'CCPI', 'RS', 'HS',
                  'NHPI', 'CA', 'D.UE', 'D.Brent', 'D.WTI']
    title = []
    with open("data/gdpLongReal.dat", "r") as reader:
        for i in range(len(title_name)):
            title.append(map(float, reader.readline().rstrip().split()))
            # print max(title[i])
            # print min(title[i])
    return title, title_name


# get Canada economy data
def get_economy_data():
    workbook = xlrd.open_workbook("data/data2.xlsx")
    table = workbook.sheets()[3]
    result = {}

    for i in range(1, 11):
        cols = table.col_values(i)
        result[cols[0]] = cols[1:113]
    return result


def normalize(a):
    result = []
    tmp1= np.max(a)
    tmp2 =  np.min(a)
    for element in a:
        x = float(element - np.min(a)) / (np.max(a) - np.min(a))
        result.append(x)
    return result


def map_data(array):
    result = []
    max_value = max(array)
    min_value = min(array)
    for i in range(0, len(array)):
        if i == 1:
            continue
        x = 2.0 / (max_value - min_value) * (array[i] - min_value) - 1
        result.append(x)
    return result


def zero_change(a):
    # result = []
    # mean = np.mean(a)
    # for element in a:
    #    result.append(element - mean)
    # return result
    result = []
    for i in range(1, len(a)):
        result.append(a[i] - a[i - 1])
    return result


def decide_type(value, sigma):
    if value < -1.5 * sigma:
        return -2
    elif value >= -1.5 * sigma and value < -0.5 * sigma:
        return -1
    elif value >= -0.5 * sigma and value <= 0.5 * sigma:
        return 0
    elif value > 0.5 * sigma and value <= 1.5 * sigma:
        return 1
    else:
        return 2


def decide_type2(value,sigma):
    if value < -0.84* sigma:
        return -2
    elif value >=-0.84 * sigma and value < -0.26 * sigma:
        return -1
    elif value >= -0.26 * sigma and value <= 0.26 * sigma:
        return 0
    elif value > 0.26 * sigma and value <= 0.84 * sigma:
        return 1
    else:
        return 2


def decide_type3(value,sigma,mean):
    if value < mean-0.68*sigma:
        return 0
    elif value >=mean-0.68*sigma and value <mean+0.68*sigma:
        return 1
    elif value >= mean+0.68*sigma:
        return 2
    return 0





def get_type_array(a,length):
    result = []
    mean, sigma= calculate_mean_and_std2(a,length)
    for element in a:
        result.append(decide_type3(element, sigma,mean))
        #result.append(decide_type2(element,sigma))
    return result


def get_type_array2(a,length):
    result = []
    mean, sigma = calculate_mean_and_std2(a,length)
    for element in a:
        result.append(decide_type2(element,sigma))
    return result


def count_type(type_array):
    count_type_array = [0, 0, 0, 0, 0]
    for element in type_array:
        count_type_array[element] += 1
    return count_type_array


def calculate_mean_and_std(data):
    length = len(data)
    use_array = data[length - 10:]
    counter = 10
    mean = 0
    std = 0
    while counter > 0:
        mean += 0.1 * counter * use_array[counter - 1]
        counter -= 1
    mean = mean / 5.5
    counter = 10
    while counter > 0:
        std += 0.1 * counter * math.pow(use_array[counter - 1] - mean, 2)
        counter -= 1
    std = std / 5.5
    std = math.pow(std, 0.5)
    return mean, std


def calculate_mean_and_std2(data,length):
    """
    length = len(data)
    use_array = data[length - 10:]
    counter = 10
    mean = 0
    std = 0
    while counter > 5:
        mean += 0.1 * counter * use_array[counter - 1]
        counter -= 1
    mean = mean / 4.0
    counter = 10
    while counter > 5:
        std += 0.1 * counter * math.pow(use_array[counter - 1] - mean, 2)
        counter -= 1
    std = std / 4.0
    std = math.pow(std, 0.5)
    """
    #use_array = data[len(data)-length:len(data)]
    #use_array = data
    #print len(use_array)
    return np.mean(data), np.std(data, ddof=1)


weights = [1,0.969571,0.938187,0.905785	,0.872299,0.837652,0.801762	,0.764536,0.725869,0.685648,0.643741,0.6]
coe = 0.8


def get_wights(lower_coe):
    weights = []
    x = (math.pow(math.e,1)- math.pow(math.e,lower_coe))/11
    for i in range(0,12):
        weight = math.log(math.e-i*x,math.e)
        weights.append(weight)
    return weights


def get_all_weights(length,lower_coe):
    weights = get_wights(lower_coe)
    result = []
    for i in range(0,length):
        c =  math.pow(coe,(i+1)/12)*weights[(i+1)%12]
        result.append(c)
    return result


def calculate_mean_and_std_with_weight(data):
    weights = get_wights(0.7)#0.7
    data_length = len(data)
    coe_sum = 0
    sum = 0
    std = 0
    sigma_sum = 0
    for i in range(0,data_length):
        tmp_coe = math.pow(coe,(i+1)/12)*weights[(i+1)%12]
        sum = sum + tmp_coe*data[data_length-i-1]
        coe_sum = tmp_coe + coe_sum
    average = sum/coe_sum
    for i in range(0,data_length):
        tmp_coe = math.pow(coe,(i+1)%12)*weights[(i+1)%12]
        sigma_sum = sigma_sum + tmp_coe*math.pow(data[data_length-i-1]-average,2)
    std = math.pow(sigma_sum,0.5)
    return average,coe_sum


def mix_array(data1, type_array1, data2, type_array2, next_value, next_type):
    arrays = [[]]
    for i in range(0, len(type_array2)):
        if type_array1[i] == type_array2[i]:
            for array in arrays:
                array.append(data1[i])
        else:
            for j in range(0, len(arrays)):
                arrays.append(list(arrays[j]))
            for k in range(0, len(arrays)):
                if k <= len(arrays) / 2 - 1:
                    arrays[k].append(data1[i])
                else:
                    arrays[k].append(data2[i])
    target_index = 0
    max_p = 0
    for i in range(0, len(arrays)):
        p = decide_p2(arrays[i], next_type)
        if p > max_p:
            max_p = p
            target_index = i
    # min_difference = 1000
    # for i in range(0,len(arrays)):
    #    mean, std = calculate_mean_and_std(arrays[i])
    #    if abs(mean-next_value)<min_difference:
    #        min_difference = abs(mean-next_value)
    #        target_index = i
    return arrays[target_index], max_p


def change_to_normal_distribution(data, mean, std):
    for i in range(0, len(data)):
        data[i] = ((data[i]) - mean) / std
    return data


"""
def decide_p(data, next_type):
    mean, std = calculate_mean_and_std(data)
    p = 0
    normal = scipy.stats.norm(mean,std)
    #print (-0.5 * std - mean) / std
    if next_type == -2:
        p = fastncdf((-1.5*std-mean)/std)
    elif next_type == -1:
        p = fastncdf((-0.5*std-mean)/std) - fastncdf((-1.5*std-mean)/std)
    elif next_type == 0:
        p = fastncdf((0.5*std-mean)/std) - fastncdf((-0.5*std-mean)/std)
    elif next_type == 1:
        p = fastncdf((1.5*std-mean)/std) - fastncdf((0.5*std-mean)/std)
    elif next_type == 2:
        p = 1 - fastncdf((1.5*std-mean)/std)
    return p
"""


def decide_p(data, next_type,length):
    mean, std = calculate_mean_and_std2(data,length)
    p = 0
    # normal = scipy.stats.norm(mean,std)
    # print (-0.5 * std - mean) / std
    if next_type == -2:
        p = fastncdf((-1.5 * std - mean) / std)
    elif next_type == -1:
        p = fastncdf((-0.5 * std - mean) / std) - fastncdf((-1.5 * std - mean) / std)
    elif next_type == 0:
        p = fastncdf((0.5 * std - mean) / std) - fastncdf((-0.5 * std - mean) / std)
    elif next_type == 1:
        p = fastncdf((1.5 * std - mean) / std) - fastncdf((0.5 * std - mean) / std)
    elif next_type == 2:
        p = 1 - fastncdf((1.5 * std - mean) / std)
    return p


def decide_p2(data, next_type,length):
    mean, std = calculate_mean_and_std2(data,length)
    p = 0
    # normal = scipy.stats.norm(mean,std)
    # print (-0.5 * std - mean) / std
    if next_type == -2:
        p = fastncdf((-0.84 * std - mean) / std)
    elif next_type == -1:
        p = fastncdf((-0.26 * std - mean) / std) - fastncdf((-0.84 * std - mean) / std)
    elif next_type == 0:
        p = fastncdf((0.26 * std - mean) / std) - fastncdf((-0.26 * std - mean) / std)
    elif next_type == 1:
        p = fastncdf((0.84 * std - mean) / std) - fastncdf((0.26 * std - mean) / std)
    elif next_type == 2:
        p = 1 - fastncdf((0.84 * std - mean) / std)
    return p


def calculate_compress_length(p_value_array):
    length = 0
    for p in p_value_array:
        if p <= 0:
            p = 0.0001
        length = length - math.log(p, 2)

    return length


def calculate_difference(cause, effect):
    cause_type = get_type_array(cause)
    effect_type = get_type_array(effect)
    print count_type(cause_type)
    print count_type(effect_type)
    effect_p_array = []
    cause_effect_p_array = []
    for i in range(10, len(effect) - 1):
        p1 = decide_p2(effect[i - 10:i], effect_type[i])
        effect_p_array.append(p1)
        target_array,p2 = mix_array(effect[i - 10:i], effect_type[i - 10:i], cause[i - 10:i], cause_type[i - 10:i],
                                 effect[i], effect_type[i])
        cause_effect_p_array.append(p2)
    effect_length = calculate_compress_length(effect_p_array)
    cause_effect_length = calculate_compress_length(cause_effect_p_array)
    return effect_length - cause_effect_length


def real_data_test():
    data, data_name = get_data()
    economy_data = get_economy_data()
    data = []
    for key in economy_data:
        data.append(economy_data[key])
    for i in range(0, len(data)):
        if i == 8 or i == 9:
            data[i] = map_data(data[i])
        data[i] = normalize(data[i])
        data[i] = zero_change(data[i])
    for i in range(1, 9):
        cause2effect = calculate_difference(data[i], data[0])
        effect2cause = calculate_difference(data[0], data[i])
        print data_name[i] + ' -> ' + data_name[0] + ':' + str(cause2effect)
        print data_name[0] + ' -> ' + data_name[i] + ':' + str(effect2cause)
        print
        print


def exception_test():
    data, data_name = get_data()
    economy_data = get_economy_data()
    data = []
    for key in economy_data:
        print key
        data.append(economy_data[key])
    for i in range(0, len(data)):
        data[i] = normalize(data[i])
        data[i] = zero_change(data[i])
    cause2effect = calculate_difference(data[9], data[0])
    effect2cause = calculate_difference(data[0], data[9])
    print cause2effect
    print effect2cause
    print cause2effect - effect2cause


def test_simulation():
    counter = 0
    for i in range(0, 100):
        cause, effect = generate_continue_data(100, 20)
        cause = normalize(cause)
        cause = zero_change(cause)
        effect = normalize(effect)
        effect = zero_change(effect)
        cause2effect = calculate_difference(cause, effect)
        effect2cause = calculate_difference(effect, cause)
        print 'cause' + ' -> ' + 'effect' + ':' + str(cause2effect)
        print 'effect' + ' -> ' + 'cause' + ':' + str(effect2cause)
        if cause2effect > effect2cause:
            counter += 1
    print
    print counter

#test_simulation()
# real_data_test()
