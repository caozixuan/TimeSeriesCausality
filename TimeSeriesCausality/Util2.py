from scipy import *
import scipy.stats
import math
import random
from collections import defaultdict
import numpy as np
from Util import calculate_mean_and_std2, decide_type, get_type_array, get_data, get_economy_data, map_data, normalize, \
    zero_change, calculate_compress_length, count_type, calculate_mean_and_std_with_weight
from simulate import generate_continue_data
from snml import bernoulli, cbernoulli


def CnkD(n, k):
    C = defaultdict(int)
    for row in range(n + 1):
        C[row, 0] = 1
        for col in range(1, k + 1):
            if col <= row:
                C[row, col] = C[row - 1, col - 1] + C[row - 1, col]
    return C[n, k]


def get_b_p(n, k, p):
    coe = CnkD(n, k)
    p_result = coe * math.pow(p, k) * math.pow(1 - p, n - k)
    return p_result


def mix_array(data1, type_array1, data2, type_array2, next_value, next_type, length, effect_type_before):
    # arrays = [list(effect_type_before)]
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
        mean, std = calculate_mean_and_std2(arrays[i], length)
        parameter_p = mean / 2.0
        p = get_b_p(2, next_type, parameter_p)
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


def mix_array2(effect_type, cause_type, next_type):
    count_0 = 0
    count_2 = 0
    target_array = []
    for i in range(0, len(effect_type)):
        cur_element = 0
        cur_effect_type = effect_type[i]
        cur_cause_type = cause_type[i]
        if cur_effect_type == cur_cause_type:
            cur_element = cur_effect_type
        else:
            if next_type == 0:
                cur_element = min([cur_effect_type, cur_cause_type])
            elif next_type == 2:
                cur_element = max([cur_effect_type, cur_cause_type])
            else:
                if cur_effect_type == 1 or cur_cause_type == 1:
                    cur_element = 1
                else:
                    if count_0 <= count_2:
                        cur_element = 0
                    else:
                        cur_element = 2
        target_array.append(cur_element)
        if cur_element == 0:
            count_0 += 1
        elif cur_element == 2:
            count_2 += 1
    return target_array


def calculate_difference(cause, effect, length):
    cause_type = get_type_array(cause, length)
    effect_type = get_type_array(effect, length)
    print count_type(cause_type)
    print count_type(effect_type)
    effect_p_array = []
    for i in range(length, len(effect) - 1):
        mean, std = calculate_mean_and_std2(effect_type[i - length:i], length)
        # print mean
        # print np.mean(effect_type[i-length:i])
        parameter_p = mean / 2.0
        effect_p_array.append(get_b_p(2, effect_type[i], parameter_p))
    effect_length = calculate_compress_length(effect_p_array)
    cause_effect_p_array = []
    for i in range(length, len(effect) - 1):
        target_array = mix_array(effect_type[i - length:i], effect_type[i - length:i], cause_type[i - length:i],
                                 cause_type[i - length:i],
                                 effect_type[i], effect_type[i], length, effect_type[0:i - length])
        mean, std = calculate_mean_and_std2(target_array, length)
        parameter_p = mean / 2.0
        p = get_b_p(2, effect_type[i], parameter_p)
        cause_effect_p_array.append(get_b_p(2, effect_type[i], parameter_p))
        # mean, std = calculate_mean_and_std2(cause_type[0:i], length)
        # parameter_p = mean / 2.0
    # p = get_b_p(2, effect_type[i], parameter_p)
    # if p > effect_p_array[i-length]:
    #    cause_effect_p_array.append(get_b_p(2, effect_type[i], parameter_p))
    # else:
    #    cause_effect_p_array.append(effect_p_array[i-length])
    cause_effect_length = calculate_compress_length(cause_effect_p_array)
    return effect_length - cause_effect_length


def calculate_difference2(cause, effect, length):
    cause_type = get_type_array(cause, length)
    effect_type = get_type_array(effect, length)
    cause_zero_one = change_type_to_zero_one_code(cause_type)
    effect_zero_one = change_type_to_zero_one_code(effect_type)
    print cause_zero_one
    print effect_zero_one
    delta_x_to_y = bernoulli(effect_zero_one) - cbernoulli(effect_zero_one, cause_zero_one)
    return delta_x_to_y


def calculate_difference3(cause, effect, length):
    cause_type = get_type_array(cause, length)
    effect_type = get_type_array(effect, length)
    print count_type(cause_type)
    print count_type(effect_type)
    effect_p_array = []
    cause_effect_p_array = []
    for i in range(length, len(effect) - 1):
        mean, std = calculate_mean_and_std2(effect_type[i - length:i], length)
        parameter_p = mean / 2.0
        effect_p_array.append(get_b_p(2, effect_type[i], parameter_p))
        target_array = mix_array2(effect_type[i - length:i], cause_type[i - length:i], effect_type[i])
        # print target_array
        mean2, std2 = calculate_mean_and_std2(target_array, length)
        parameter_p2 = mean2 / 2.0
        p2 = get_b_p(2, effect_type[i], parameter_p2)
        cause_effect_p_array.append(p2)
    effect_length = calculate_compress_length(effect_p_array)
    cause_effect_length = calculate_compress_length(cause_effect_p_array)
    return effect_length - cause_effect_length


def change_type_to_zero_one_code(a):
    result = []
    for element in a:
        if element == 0:
            result.extend([1, 1, 0])
        elif element == 1:
            result.extend([1, 1, 1])
        elif element == 2:
            result.extend([0, 0, 0])
        elif element == 3:
            result.extend([0, 0, 1])
        elif element == 4:
            result.extend([0, 1, 0])
    return result


def real_data_test(length):
    data, data_name = get_data()
    economy_data = get_economy_data()
    data = []
    for key in economy_data:
        for x in range(0, len(economy_data[key])):
            economy_data[key][x] = economy_data[key][x] + 1
        #print map(int, economy_data[key])
        data.append(map(int, economy_data[key]))
    """
    for i in range(0, len(data)):
        if i == 8 or i == 9:
            data[i] = map_data(data[i])
        data[i] = normalize(data[i])
        data[i] = zero_change(data[i])
    """
    for i in range(1, 9):
        cause2effect = calculate_difference3(data[i], data[0], length)
        effect2cause = calculate_difference3(data[0], data[i], length)
        print data_name[i] + ' -> ' + data_name[0] + ':' + str(cause2effect)
        print data_name[0] + ' -> ' + data_name[i] + ':' + str(effect2cause)
        print
        print


def test_simulation(length):
    counter = 0
    for i in range(0, 100):
        cause, effect = generate_continue_data(200, random.randint(1, 5))  # random.randint(1,5)
        cause = normalize(cause)
        cause = zero_change(cause)
        effect = normalize(effect)
        effect = zero_change(effect)
        cause2effect = calculate_difference3(cause, effect, length)
        effect2cause = calculate_difference3(effect, cause, length)
        print 'cause' + ' -> ' + 'effect' + ':' + str(cause2effect)
        print 'effect' + ' -> ' + 'cause' + ':' + str(effect2cause)
        if cause2effect > effect2cause:
            counter += 1
    print
    print counter
    return counter / 100.0


result = []
for i in range(6, 7):
    result.append(test_simulation(i))
print result

#real_data_test(6)
"""
x = [0,1,0,1,2,2,0,1,1,0,0]
y = [0,1,1,2,2,1,0,0,1,0,2]

a = mix_array(x,x,y,y,1,1,11,[])
b = mix_array2(x,y,1)

print a
print b
"""
