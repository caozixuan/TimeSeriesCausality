from scipy import *
import scipy.stats
import math
import random
from collections import defaultdict
import numpy as np
from Util import calculate_mean_and_std2, decide_type, get_type_array, get_data, get_economy_data, map_data, normalize, \
    zero_change, calculate_compress_length, count_type, calculate_mean_and_std_with_weight, get_wights,get_all_weights,get_type_array3,get_type_array2,get_type_array4
from simulate import generate_continue_data, generate_continue_data2
from snml import bernoulli, cbernoulli,bernoulli2,cbernoulli2


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


def mix_array2(effect_type, cause_type, next_type, extra_array):
    count_0 = 0
    count_2 = 0
    target_array = []
    counter = 0
    target_array.extend(list(extra_array))
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
                if count_0 < count_2:
                    cur_element = 0
                elif count_0 > count_2:
                    cur_element = 2
                else:
                    cur_element = 1
        target_array.append(cur_element)
        if cur_effect_type != cur_element:
            counter += 1
        if cur_element == 0:
            count_0 += 1
        elif cur_element == 2:
            count_2 += 1
    # print counter
    return target_array


def mix_array3(effect_type, cause_type, next_type, extra_array):
    total_length = len(effect_type) + len(effect_type)
    counter_0_0 = 0
    counter_0_1 = 0
    counter_0_2 = 0
    counter_2_0 = 0
    counter_2_1 = 0
    counter_2_2 = 0
    is_0_2_happen = False
    target_array = []
    for element in extra_array:
        if element == 0:
            counter_0_0 += 1
            counter_2_0 += 1
        elif element == 2:
            counter_0_2 += 1
            counter_2_2 += 1
        elif element == 1:
            counter_0_1 += 1
            counter_2_1 +=1
    for i in range(0, len(effect_type)):
        cur_effect_type = effect_type[i]
        cur_cause_type = cause_type[i]
        if cur_effect_type == cur_cause_type:
            if cur_effect_type == 0:
                counter_0_0 += 1
                counter_2_0 += 1
            elif cur_effect_type == 2:
                counter_0_2 += 1
                counter_2_2 += 1
            elif cur_effect_type == 1:
                counter_0_1 += 1
                counter_2_1 += 1
        else:
            if (cur_cause_type == 0 and cur_effect_type == 1) or (cur_cause_type == 1 and cur_effect_type == 0):
                counter_0_0 += 1
                counter_2_1 += 1
            elif (cur_cause_type == 0 and cur_effect_type == 2) or (cur_cause_type == 2 and cur_effect_type == 0):
                is_0_2_happen = True
                counter_0_0 += 1
                counter_2_2 += 1
            elif (cur_cause_type == 1 and cur_effect_type == 2) or (cur_cause_type == 2 and cur_effect_type == 1):
                counter_2_2 += 1
                counter_0_1 += 1
    if next_type == 0:
        for i in range(0, counter_0_0):
            target_array.append(0)
        for i in range(0, counter_0_1):
            target_array.append(1)
        for i in range(0, counter_0_2):
            target_array.append(2)
    elif next_type == 2:
        for i in range(0, counter_2_0):
            target_array.append(0)
        for i in range(0, counter_2_1):
            target_array.append(1)
        for i in range(0, counter_2_2):
            target_array.append(2)
    elif next_type == 1:
        x0 = counter_0_2 - counter_0_0
        x2 = counter_2_2 - counter_2_0
        if x0 * x2 > 0:
            if abs(x0) < abs(x2):
                for i in range(0, counter_0_0):
                    target_array.append(0)
                for i in range(0, counter_0_1):
                    target_array.append(1)
                for i in range(0, counter_0_2):
                    target_array.append(2)
            else:
                for i in range(0, counter_2_0):
                    target_array.append(0)
                for i in range(0, counter_2_1):
                    target_array.append(1)
                for i in range(0, counter_2_2):
                    target_array.append(2)
        else:
            if not is_0_2_happen:
                return [0, 0, 0, 1, 1, 1, 2, 2, 2]
            else:
                if abs(x0) % 2 == 0:
                    return [0, 0, 0, 1, 1, 1, 2, 2, 2]
                else:
                    k = abs(x0) / 2
                    for i in range(0, counter_0_0 - k):
                        target_array.append(0)
                    for i in range(0, counter_0_2 + k):
                        target_array.append(2)
                    for i in range(0, counter_0_1):
                        target_array.append(1)
    return target_array


def mix_array_with_weight(effect_type, cause_type, next_type, extra_array):
    length_0 = 0
    length_2 = 0
    weights = get_all_weights(len(effect_type)+len(extra_array),0.7)
    weights.reverse()
    target_length = sum(weights)
    counter = 0
    values = []
    while counter<len(extra_array):
        length_0 = length_0 + weights[counter]*extra_array[counter]
        length_2 = length_2 + weights[counter]*extra_array[counter]
        counter+=1
    counter = 0
    while counter<len(effect_type):
        cause_type_value = weights[counter+len(extra_array)]*cause_type[counter]
        effect_type_value = weights[counter+len(extra_array)]*effect_type[counter]
        if abs(cause_type_value-effect_type_value)<0.00001:
            length_0 = length_0 + cause_type_value
            length_2 = length_2 + cause_type_value
        else:
            length_0 = length_0 + min([cause_type_value, effect_type_value])
            length_2 = length_2 + max([cause_type_value, effect_type_value])
            values.append(abs(cause_type_value-effect_type_value)*10)
        counter += 1
    imbalance_0 = length_0 - target_length
    imbalance_2 = length_2 - target_length
    if next_type==0:
        return length_0/target_length, target_length
    elif next_type==2:
        return length_2/target_length, target_length
    else:
        if imbalance_0*imbalance_2>0:
            if abs(imbalance_0)<abs(imbalance_2):
                return length_0/target_length, target_length
            else:
                return length_2 / target_length, target_length
        else:
            """
            target = abs(imbalance_0)
            values = map(round,values)
            values = map(int,values)
            down_min = target - float(bag_problem(int(target*10),values))/10.0
            target2 = abs(imbalance_2)
            up_min = target2 - float(bag_problem(int(target2*10),values))/10.0
            if up_min<down_min:
                return (target_length+up_min)/target_length, target_length
            else:
                return (target_length-down_min)/target_length, target_length
            """
            target = abs(imbalance_0)
            for i in range(0,len(values)):
                values[i]=values[i]/10.0
            values.sort(reverse=True)
            down_min = greedy(target,values)
            target2 = abs(imbalance_2)
            up_min = greedy(target2,values)
            if up_min < down_min:
                return (target_length + up_min) / target_length, target_length
            else:
                return (target_length - down_min) / target_length, target_length



def greedy(target,values):
    sum = 0
    for i in range(0,len(values)):
        if sum+values[i]<target:
            sum = sum+values[i]
    return sum

def bag_problem(target,values):
    n = len(values)
    dp = [0 for i in range(target+1)]
    for i in range(0,n):
        j = target
        while j>=values[i]:
            dp[j]=max(dp[j],dp[j-values[i]]+values[i])
            j-=1
    return dp[target]


def bag_problem2(target,values):
    n = len(values)
    dp = [0 for i in range(target+1)]
    for i in range(0,n):
        j = target
        while j<=values[i]:
            dp[j]=min(dp[j],dp[j-values[i]]+values[i])
            j+=1
    return dp[target]




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
    cause_type = get_type_array3(cause, length)
    effect_type = get_type_array3(effect, length)
    print count_type(cause_type)
    print count_type(effect_type)
    effect_p_array = []
    cause_effect_p_array = []
    for i in range(length, len(effect) - 1):
        #mean, std = calculate_mean_and_std2(effect_type[i-length:i], length)
        #parameter_p = mean / 2.0
        #effect_p_array.append(get_b_p(2, effect_type[i], parameter_p))
        effect_p_array.append(snml_b(effect_type[i - length:i], effect_type[i]))
        target_array = mix_array3(effect_type[i - length:i], cause_type[i - length:i], effect_type[i],[])  #
        #print target_array
        #mean2, std2 = calculate_mean_and_std2(target_array, length)
        #parameter_p2 = mean2 / 2.0
        #p2 = get_b_p(2, effect_type[i], parameter_p2)
        #cause_effect_p_array.append(p2)
        cause_effect_p_array.append(snml_b(target_array, effect_type[i]))
    effect_length = sum(effect_p_array)  #calculate_compress_length(effect_p_array)#
    cause_effect_length = sum(cause_effect_p_array)  #calculate_compress_length(cause_effect_p_array)#
    return effect_length - cause_effect_length


def calculate_difference4(cause, effect, length):
    cause_type = get_type_array(cause, length)
    effect_type = get_type_array(effect, length)
    #print count_type(cause_type)
    #print count_type(effect_type)
    effect_p_array = []
    cause_effect_p_array = []
    for i in range(length, len(effect) - 1):
        mean2, ll = calculate_mean_and_std_with_weight(
            effect_type[0:i])  # calculate_mean_and_std2(effect_type[i-length:i], length)
        #parameter_p = mean / 2.0
        #effect_p_array.append(get_b_p(2, effect_type[i], parameter_p))
        effect_p_array.append(snml_b2(mean2,ll,effect_type[i]))
        #target_array = mix_array2(effect_type[0:i], cause_type[0:i], effect_type[i], [])
        # print target_array
        #mean2, std2 = calculate_mean_and_std_with_weight(target_array)  # calculate_mean_and_std2(target_array, length)
        #parameter_p2 = mean2 / 2.0
        #p2 = get_b_p(2, effect_type[i], parameter_p2)
        mean,l = mix_array_with_weight(effect_type[0:i], cause_type[0:i], effect_type[i], [])
        p2 = snml_b2(mean,l,effect_type[i])
        cause_effect_p_array.append(p2)
        # cause_effect_p_array.append(snml_b(target_array,effect_type[i]))
    effect_length = sum(effect_p_array)#calculate_compress_length(effect_p_array)
    cause_effect_length = sum(cause_effect_p_array)#calculate_compress_length(cause_effect_p_array)
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
    economy_data = get_economy_data()
    data_name = []
    data = []
    for key in economy_data:
        # for x in range(0, len(economy_data[key])):
        # economy_data[key][x] = economy_data[key][x] + 1
        # print map(int, economy_data[key])
        # data.append(map(int, economy_data[key]))
        data_name.append(key)
        # print key
        # print get_type_array(economy_data[key],length)
        # x = normalize()
        """
        if key!='D.UE' and key!='D.WTI' and key!='D.Brent':
            x = zero_change(x)
        else:
            x=x[1:len(x)]
        """
        # print get_type_array(x,length)
        print get_type_array(economy_data[key], length)
        data.append(economy_data[key])
    """
    for i in range(0, len(data)):
        if i == 8 or i == 9:
            data[i] = map_data(data[i])
        data[i] = normalize(data[i])
        data[i] = zero_change(data[i])
    """
    for i in range(1, 10):
        cause2effect = calculate_difference4(data[i], data[0], length)
        effect2cause = calculate_difference4(data[0], data[i], length)
        print data_name[i] + ' -> ' + data_name[0] + ':' + str(cause2effect)
        print data_name[0] + ' -> ' + data_name[i] + ':' + str(effect2cause)
        print math.pow(2, -abs(cause2effect - effect2cause))
        print
        print


def log(x):
    if x == 0:
        return 0
    return math.log(x, 2)


def snml_b(data, next_value):
    p = 0
    log_f_0 = 0
    log_f_1 = 0
    log_f_2 = 0
    data_sum = sum(data)
    double_length = 2 * len(data)
    try:
        log_f_0 = data_sum * log(data_sum) + (double_length - data_sum + 2) * log(double_length - data_sum + 2)
        # f_0 = math.pow(data_sum,data_sum)*math.pow(double_length-data_sum+2,double_length-data_sum+2)
        log_f_1 = log(2) + (data_sum + 1) * log(data_sum + 1) + (double_length - data_sum + 1) * log(
            double_length - data_sum + 1)
        # f_1 = 2*math.pow(data_sum+1,data_sum+1)*math.pow(double_length-data_sum+1,double_length-data_sum+1)
        log_f_2 = (data_sum + 2) * log(data_sum + 2) + (double_length - data_sum) * log(double_length - data_sum)
        # f_2 = math.pow(data_sum+2,data_sum+2)*math.pow(double_length-data_sum,double_length-data_sum)
        max_value = max([log_f_0, log_f_1, log_f_2])
        lg_denom = max_value + math.log(
            math.pow(2, log_f_0 - max_value) + math.pow(2, log_f_1 - max_value) + math.pow(2, log_f_2 - max_value))
    except ValueError:
        print data_sum
        print double_length
    if next_value == 0:
        lg_numer = log_f_0
    elif next_value == 1:
        lg_numer = log_f_1
    elif next_value == 2:
        lg_numer = log_f_2
    return lg_denom - lg_numer


def snml_b2(mean,length,next_value):
    p = 0
    log_f_0 = 0
    log_f_1 = 0
    log_f_2 = 0
    data_sum = mean*length
    double_length = 2 * length
    try:
        log_f_0 = data_sum * log(data_sum) + (double_length - data_sum + 2) * log(double_length - data_sum + 2)
        # f_0 = math.pow(data_sum,data_sum)*math.pow(double_length-data_sum+2,double_length-data_sum+2)
        log_f_1 = log(2) + (data_sum + 1) * log(data_sum + 1) + (double_length - data_sum + 1) * log(
            double_length - data_sum + 1)
        # f_1 = 2*math.pow(data_sum+1,data_sum+1)*math.pow(double_length-data_sum+1,double_length-data_sum+1)
        log_f_2 = (data_sum + 2) * log(data_sum + 2) + (double_length - data_sum) * log(double_length - data_sum)
        # f_2 = math.pow(data_sum+2,data_sum+2)*math.pow(double_length-data_sum,double_length-data_sum)
        max_value = max([log_f_0, log_f_1, log_f_2])
        lg_denom = max_value + math.log(
            math.pow(2, log_f_0 - max_value) + math.pow(2, log_f_1 - max_value) + math.pow(2, log_f_2 - max_value))
    except ValueError:
        print data_sum
        print double_length
    if next_value == 0:
        lg_numer = log_f_0
    elif next_value == 1:
        lg_numer = log_f_1
    elif next_value == 2:
        lg_numer = log_f_2
    return lg_denom - lg_numer

from statsmodels.tsa.stattools import grangercausalitytests


def granger_test():
    data, data_name = get_data()
    economy_data = get_economy_data()
    data = []
    for key in economy_data:
        for x in range(0, len(economy_data[key])):
            economy_data[key][x] = economy_data[key][x] + 1
        # print map(int, economy_data[key])
        data.append(map(int, economy_data[key]))
    """
    for i in range(0, len(data)):
        if i == 8 or i == 9:
            data[i] = map_data(data[i])
        data[i] = normalize(data[i])
        data[i] = zero_change(data[i])
    """
    for i in range(1, 9):
        print "Continuous data, Granger causality test"
        print "cause->effect"
        p_value_cause_to_effect1 = []
        flag1 = False
        ce1 = grangercausalitytests([[data[i][j], data[0][j]] for j in range(0, len(data[0]))], 3)
        for key in ce1:
            p_value_cause_to_effect1.append(ce1[key][0]["params_ftest"][1])
            if ce1[key][0]["params_ftest"][1] < 0.05:
                flag1 = True
        print "effect->cause"
        p_value_effect_to_cause2 = []
        flag2 = False
        ce2 = grangercausalitytests([[data[0][j], data[i][j]] for j in range(0, len(data[i]))], 3)
        for key in ce2:
            p_value_effect_to_cause2.append(ce2[key][0]["params_ftest"][1])
            if ce2[key][0]["params_ftest"][1] < 0.05:
                flag2 = True
        if flag1 and flag2:
            print "two way course and effect" + data_name[i]
        elif flag1 and not flag2:
            print "gdp to " + data_name[i]
        elif not flag1 and flag2:
            print data_name[i] + " to gdp"
        elif not flag1 and not flag2:
            print "no effect" + data_name[i]


def bh_procedure(p_array, alpha):
    p_array.sort()
    counter = 0
    for k in range(1, len(p_array) + 1):
        if p_array[k - 1] <= float(k) / float((len(p_array))) * alpha:
            counter = k
        else:
            counter = k-1
            break
    return counter


def test_simulation(length):
    counter = 0
    p_array = []
    for i in range(0, 1000):
        cause, effect = generate_continue_data(200, 3)  # random.randint(1,5)
        #effect, test2 = generate_continue_data(200, 3)  # random.randint(1,5)
        cause = normalize(cause)
        cause = zero_change(cause)
        effect = normalize(effect)
        effect = zero_change(effect)
        cause2effect = calculate_difference4(cause, effect, length)
        effect2cause = calculate_difference4(effect, cause, length)
        print 'cause' + ' -> ' + 'effect' + ':' + str(cause2effect)
        print 'effect' + ' -> ' + 'cause' + ':' + str(effect2cause)
        p = math.pow(2, -(cause2effect - effect2cause))
        p_array.append(p)
        if cause2effect > effect2cause and (cause2effect - effect2cause) >= -log(0.05):
            counter += 1
    print
    print counter
    print bh_procedure(p_array, 0.05)
    return counter / 100.0


#result = []
#for i in range(6, 7):
#    result.append(test_simulation(i))
#print result

# get_wights(0.6)
#real_data_test(6)
# granger_test()
"""
x = [0,1,0,1,2,2,0,1,1,0,0]
y = [0,1,1,2,2,1,0,0,1,0,2]

a = mix_array(x,x,y,y,1,1,11,[])
b = mix_array2(x,y,1)

print a
print b
"""

def change_to_zero_one(data):
    result = []
    for i in range(1,len(data)):
        if data[i]>data[i-1]:
            result.append(1)
        else:
            result.append(0)
    return result

def change_to_zero_one2(data):
    result = []
    tmp = list(data)
    tmp.sort()
    mid = tmp[int(0.5*len(data))]
    for i in range(1,len(data)):
        if data[i]>mid:
            result.append(1)
        else:
            result.append(0)
    return result

from GMM import GMM
def cute_test(length):
    p_array = []
    counter=0
    for i in range(0, 1000):
        #cause, effect = generate_continue_data(200, random.randint(1,3))  # random.randint(1,5)
        cause = GMM(5,200)
        effect = GMM(8,200)
        #effect, test2 = generate_continue_data(200, 3)  # random.randint(1,5)
        cause = change_to_zero_one(cause)
        effect = change_to_zero_one(effect)

        cause2effect = bernoulli2(effect,length) - cbernoulli2(effect, cause,length)
        effect2cause = bernoulli2(cause,length) - cbernoulli2(cause, effect,length)
        #print 'cause' + ' -> ' + 'effect' + ':' + str(cause2effect)
        #print 'effect' + ' -> ' + 'cause' + ':' + str(effect2cause)
        p = math.pow(2, -(cause2effect - effect2cause))
        p_array.append(p)
        if cause2effect > effect2cause:
            counter += 1
    print
    print counter
    print bh_procedure(p_array, 0.05)
    return counter / 100.0


#cute_test(6)

