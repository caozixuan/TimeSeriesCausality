# encoding:utf-8
from sklearn import preprocessing
import numpy as np
from scipy import *
import scipy.stats
import math
import xlrd

from simulate import generate_continue_data

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
    title_name = ['GDP_monthly', 'house_price_index_monthly', 'unemployment_rate', 'CPI_core_monthly', 'CPI_monthly',
                  'trade_monthly', 'sell', 'new house', 'brent', 'WTI']
    title = []
    with open("data/gdpLongReal.dat", "r") as reader:
        for i in range(len(title_name)):
            title.append(map(float, reader.readline().rstrip().split()))
            # print max(title[i])
            # print min(title[i])
    return title, title_name


# get Canada economy data
def get_economy_data():
    workbook = xlrd.open_workbook("data/data.xlsx")
    table = workbook.sheets()[3]
    result = {}

    for i in range(1, 11):
        cols = table.col_values(i)
        result[cols[0]] = cols[1:113]
    return result


def normalize(a):
    result = []
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


def decide_type2(value):
    if value < -0.3:
        return 0
    elif value >= -0.3 and value < -0.1:
        return 1
    elif value >= -0.1 and value <= 0.1:
        return 2
    elif value > 0.1 and value <=0.3:
        return 3
    else:
        return 4


def get_type_array(a):
    result = []
    mean, sigma = calculate_mean_and_std(a)
    for element in a:
        result.append(decide_type(element, sigma)+2)
    return result


def get_type_array2(a):
    result = []
    mean, sigma = calculate_mean_and_std(a)
    for element in a:
        result.append(decide_type2(element))
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


def calculate_mean_and_std2(data):
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
    length = len(data)
    use_array = data[length - 10:]
    return np.mean(use_array), np.std(use_array,ddof=1)


def mix_array(data1, type_array1, data2, type_array2, next_value):
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
        mean, std = calculate_mean_and_std(arrays[i])
        p = decide_p(arrays[i], decide_type(next_value, sigma=std))
        if p > max_p:
            max_p = p
            target_index = i
    # min_difference = 1000
    # for i in range(0,len(arrays)):
    #    mean, std = calculate_mean_and_std(arrays[i])
    #    if abs(mean-next_value)<min_difference:
    #        min_difference = abs(mean-next_value)
    #        target_index = i
    return arrays[target_index]


def decide_p(data, next_type):
    mean, std = calculate_mean_and_std(data)
    normal_distribution = scipy.stats.norm(mean, std)
    p = 0
    if next_type == -2:
        p = normal_distribution.cdf(-0.3)
    elif next_type == -1:
        p = normal_distribution.cdf(-0.1) - normal_distribution.cdf(-0.3)
    elif next_type == 0:
        p = normal_distribution.cdf(0.1) - normal_distribution.cdf(-0.1)
    elif next_type == 1:
        p = normal_distribution.cdf(0.3) - normal_distribution.cdf(0.1)
    elif next_type == 2:
        p = 1 - normal_distribution.cdf(0.3)
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
    effect_p_array = []
    for i in range(10, len(effect) - 1):
        effect_p_array.append(decide_p(effect[0:i], effect_type[i]))
    effect_length = calculate_compress_length(effect_p_array)
    cause_effect_p_array = []
    for i in range(10, len(effect) - 1):
        target_array = mix_array(effect[i - 10:i], effect_type[i - 10:i], cause[i - 10:i], cause_type[i - 10:i],
                                 effect[i])
        cause_effect_p_array.append(decide_p(target_array, effect_type[i]))
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
    for i in range(0,100):
        cause, effect = generate_continue_data(100,random.randint(1,5))
        cause = normalize(cause)
        cause = zero_change(cause)
        effect = normalize(effect)
        effect = zero_change(effect)
        cause2effect = calculate_difference(cause, effect)
        effect2cause = calculate_difference(effect, cause)
        print 'cause' + ' -> ' + 'effect' + ':' + str(cause2effect)
        print 'effect' + ' -> ' + 'cause'+ ':' + str(effect2cause)
        if cause2effect>effect2cause:
            counter+=1
    print
    print counter


#test_simulation()
#real_data_test()
