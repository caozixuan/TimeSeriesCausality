# encoding:utf-8
import random
import math
from Util import generate_continue_data, get_type_array,normalize,zero_change
from Util2 import calculate_difference,calculate_difference3,calculate_difference4
from statsmodels.tsa.stattools import grangercausalitytests


# test causal continue data
def test_data(length):
    txtName = "causal_continue_noise_0.1_normal_sample_100_length_100.txt"
    f = file(txtName, "a+")
    counter11 = 0
    counter10 = 0
    counter01 = 0
    counter00 = 0
    counter11_01 = 0
    counter10_01 = 0
    counter01_01 = 0
    counter00_01 = 0
    counter_undecided = 0
    counter_true = 0
    counter_false = 0
    for i in range(0, 100):
        write_str = ""
        p = random.randint(1, 5)
        #effect, test1 = generate_continue_data(100, p)
        cause, effect = generate_continue_data(1000, 3)
        #effect, test2 = generate_continue_data(200, 3)
        cause = normalize(cause)
        cause = zero_change(cause)
        effect = normalize(effect)
        effect = zero_change(effect)
        for ii in range(0, len(cause)):
            write_str = write_str + " " + str(cause[ii])
        for jj in range(0, len(effect)):
            write_str = write_str + " " + str(effect[jj])
        print "cause:" + str(cause)
        print "effect:" + str(effect)
        # effect, test2 = ge_normal_data(p,200)
        print "Continuous data, Granger causality test"
        print "cause->effect"
        p_value_cause_to_effect1 = []
        flag1 = False
        ce1 = grangercausalitytests([[effect[i], cause[i]] for i in range(0, len(cause))], 5)
        for key in ce1:
            p_value_cause_to_effect1.append(ce1[key][0]["params_ftest"][1])
            if ce1[key][0]["params_ftest"][1] < 0.05:
                flag1 = True
        print "effect->cause"
        p_value_effect_to_cause2 = []
        flag2 = False
        ce2 = grangercausalitytests([[cause[i], effect[i]] for i in range(0, len(cause))], 5)
        for key in ce2:
            p_value_effect_to_cause2.append(ce2[key][0]["params_ftest"][1])
            if ce2[key][0]["params_ftest"][1] < 0.05:
                flag2 = True
        if flag1 and flag2:
            print "Continuous data，Granger two-way cause and effect"
            write_str = write_str + " " + "连续数据，格兰杰双向因果"
            counter11 += 1
        elif flag1 and not flag2:
            print "Continuous data，Granger correct cause and effect"
            write_str = write_str + " " + "连续数据，格兰杰正确因果"
            counter10 += 1
        elif not flag1 and flag2:
            print "Continuous data，Granger wrong cause and effect"
            write_str = write_str + " " + "连续数据，格兰杰错误因果"
            counter01 += 1
        elif not flag1 and not flag2:
            print "Continuous data，Granger no cause and effect"
            write_str = write_str + " " + "连续数据，格兰杰没有因果"
            counter00 += 1
        write_str = write_str + " " + str(min(p_value_cause_to_effect1)) + " " + str(min(p_value_effect_to_cause2))
        print
        print cause
        print effect
        print cause
        print effect
        cause2 = get_type_array(cause,length)
        effect2 = get_type_array(effect,length)
        print "01 data, Granger causality test"
        print "cause->effect"
        p_value_cause_to_effect3 = []
        flag3 = False
        ce3 = grangercausalitytests([[effect2[i], cause2[i]] for i in range(0, len(cause2))], 5)
        for key in ce3:
            p_value_cause_to_effect3.append(ce3[key][0]["params_ftest"][1])
            if ce3[key][0]["params_ftest"][1] < 0.05:
                flag3 = True
        print "effect->cause"
        p_value_effect_to_cause4 = []
        flag4 = False
        ce4 = grangercausalitytests([[cause2[i], effect2[i]] for i in range(0, len(cause2))], 5)
        for key in ce4:
            p_value_effect_to_cause4.append(ce4[key][0]["params_ftest"][1])
            if ce4[key][0]["params_ftest"][1] < 0.05:
                flag4 = True
        if flag3 and flag4:
            print "01 data，Granger two-way cause and effect"
            write_str = write_str + " " + "01数据，格兰杰双向因果"
            counter11_01 += 1
        elif flag3 and not flag4:
            print "01 data，Granger correct cause and effect"
            write_str = write_str + " " + "01数据，格兰杰正确因果"
            counter10_01 += 1
        elif not flag3 and flag4:
            print "01 data，Granger wrong cause and effect"
            write_str = write_str + " " + "01数据，格兰杰错误因果"
            counter01_01 += 1
        elif not flag3 and not flag4:
            print "01 data，Granger no cause and effect"
            write_str = write_str + " " + "01数据，格兰杰没有因果"
            counter00_01 += 1
        write_str = write_str + " " + str(min(p_value_cause_to_effect3)) + " " + str(min(p_value_effect_to_cause4))
        print

        delta_ce = calculate_difference3(cause, effect,length)
        delta_ec = calculate_difference3(effect, cause,length)
        print 'cause' + ' -> ' + 'effect' + ':' + str(delta_ce)
        print 'effect' + ' -> ' + 'cause' + ':' + str(delta_ec)
        if delta_ce > delta_ec and delta_ce - delta_ec >= -math.log(0.05, 2):
            print "CUTE，correct cause and effect"
            write_str = write_str + " " + "CUTE，正确因果"
            counter_true += 1
        elif delta_ec > delta_ce and delta_ec - delta_ce >= -math.log(0.05, 2):
            print "CUTE，wrong cause and effect"
            write_str = write_str + " " + "CUTE，错误因果"
            counter_false += 1
        else:
            print "CUTE，undecided"
            write_str = write_str + " " + "CUTE，未决定"
            counter_undecided += 1
        write_str = write_str + " " + str(pow(2, -abs(delta_ce - delta_ec)))
        f.write(write_str)
        f.write("\n")
        print
        print "*****************************cut line*****************************"
        print
    f.close()
    print "连续数据，格兰杰因果关系检验："
    print "双向因果:" + str(counter11)
    print "正确因果:" + str(counter10)
    print "错误因果:" + str(counter01)
    print "没有因果" + str(counter00)
    print "-----------------"
    print "01数据，格兰杰因果关系检验："
    print "双向因果:" + str(counter11_01)
    print "正确因果:" + str(counter10_01)
    print "错误因果:" + str(counter01_01)
    print "没有因果" + str(counter00_01)
    print "-----------------"
    print "01 data，CUTE causality test："
    print "correct cause and effect:" + str(counter_true)
    print "wrong cause and effect:" + str(counter_false)
    print "no cause and effect:" + str(counter_undecided)


test_data(6)
