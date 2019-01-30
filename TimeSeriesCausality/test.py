# encoding:utf-8
import random
import math
from simulate import generate_continue_data_with_change_lag
from Util import generate_continue_data, get_type_array,normalize,zero_change
from Util2 import calculate_difference,calculate_difference3,calculate_difference4
from statsmodels.tsa.stattools import grangercausalitytests
from Util2 import bh_procedure,change_to_zero_one
from granger_test import granger
from snml import bernoulli2,cbernoulli2,bernoulli,cbernoulli
import matplotlib.pyplot as plt
from GMM import GMM
import numpy as np
# test causal continue data

def normalize_data(data):
    mean = np.mean(data)
    std = np.std(data)
    for i in range(0,len(data)):
        data[i] = (data[i]-mean)/std
    return data

def negative(data):
    result = []
    for element in data:
        if element==2:
            result.append(0)
        elif element==0:
            result.append(2)
        else:
            result.append(1)
    return result


def test_data(length,array_length):
    #txtName = "causal_continue_noise_0.4_normal_sample_1000_length_200.txt"
    #f = file(txtName, "a+")
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
    counter_undecided2 = 0
    counter_true2 = 0
    counter_false2 = 0
    counter_error_1=0
    counter_error_2=0
    p_array_granger1 = []
    p_array_granger2 = []
    p_array_CUTE1 = []
    p_array_CUTE2 = []
    p_array_improve_CUTE1 = []
    p_array_improve_CUTE2 = []
    p_array1 = []
    p_array2 = []
    p_array_granger = []
    for i in range(0, 1000):
        write_str = ""
        p = random.randint(1, 3)
        #effect, test1 = generate_continue_data(200, p)

        #cause, effect = generate_continue_data(150, p)
        #cause_tmp = list(cause)
        #effect_tmp = list(effect)
        #cause = zero_change(cause)
        #effect = zero_change(effect)

        #cause,effect = generate_continue_data_with_change_lag(350,10)
        cause = GMM(3,array_length)
        effect = GMM(5,array_length)

        cause_tmp = list(cause)
        effect_tmp = list(effect)

        #effect = forward_shift_continue_data(cause,p)
        #noise = np.random.normal(0, 0.1, 200)
        #for j in range(0, 200):
        #    effect[j] = effect[j] + noise[j]

        #for i in range(0,len(cause)):
            #cause[i]=math.tanh(cause[i])
            #cause[i] = math.pow(math.e,cause[i])
            #effect[i] = math.pow(math.e,effect[i])
            #cause[i] = math.pow(cause[i],3)/10
            #effect[i] = math.pow(effect[i],3)/10
            #effect[i]=math.tanh(effect[i])
            #effect[i] = math.pow(effect[i],3)
        #effect = GMM(8,200)


        #plt.plot(cause)
        #plt.plot(effect)
        #plt.show()
        #cause = normalize(cause)
        #effect = normalize(effect)


        #cause = normalize_data(cause)
        #effect = normalize_data(effect)

        #cause = zero_change(cause)
        #effect = zero_change(effect)
        from scipy.special import expit
        #for i in range(0,len(effect)):
            #effect[i]=expit(effect[i])
            #effect[i] = 1.0/effect[i]

        for ii in range(0, len(cause)):
            write_str = write_str + " " + str(cause[ii])
        for jj in range(0, len(effect)):
            write_str = write_str + " " + str(effect[jj])
        #print "cause:" + str(cause)
        #print "effect:" + str(effect)
        # effect, test2 = ge_normal_data(p,200)

        print "Continuous data, Granger causality test"
        print "cause->effect"
        p_value_cause_to_effect1 = []
        flag1 = False
        #ce1 = grangercausalitytests([[effect[i], cause[i]] for i in range(0, len(cause))], p)
        ce_p = granger(cause,effect,-1)
        #for key in ce1:
        #    p_value_cause_to_effect1.append(ce1[key][0]["params_ftest"][1])
         #   if ce1[key][0]["params_ftest"][1] < 0.05:
        #        flag1 = True
        if ce_p < 0.05:
            flag1 = True
        print "effect->cause"
        p_value_effect_to_cause2 = []
        flag2 = False
        #ce2 = grangercausalitytests([[cause[i], effect[i]] for i in range(0, len(cause))], p)
        ce2_p = granger(effect,cause,-1)
        #for key in ce2:
        #    p_value_effect_to_cause2.append(ce2[key][0]["params_ftest"][1])
        #    if ce2[key][0]["params_ftest"][1] < 0.05:
        #        flag2 = True
        if ce2_p < 0.05:
            flag2 = True
        if ce_p<0.05:
            p_array_granger1.append(ce_p)
        elif ce2_p<0.05:
            p_array_granger2.append(ce2_p)
        if flag1 and flag2:
            print "Continuous data，Granger two-way cause and effect"
            write_str = write_str + " " + "连续数据，格兰杰双向因果"
            counter11 += 1
        elif flag1 and not flag2:
            print "Continuous data，Granger correct cause and effect"
            write_str = write_str + " " + "连续数据，格兰杰正确因果"
            counter10 += 1
            p_array_granger.append(ce_p)
        elif not flag1 and flag2:
            print "Continuous data，Granger wrong cause and effect"
            write_str = write_str + " " + "连续数据，格兰杰错误因果"
            counter01 += 1
        elif not flag1 and not flag2:
            print "Continuous data，Granger no cause and effect"
            write_str = write_str + " " + "连续数据，格兰杰没有因果"
            #break
            counter00 += 1
        #write_str = write_str + " " + str(min(p_value_cause_to_effect1)) + " " + str(min(p_value_effect_to_cause2))
        cause2 = get_type_array(cause,length)
        effect2 = get_type_array(effect,length)
        print "01 data, Granger causality test"
        print "cause->effect"
        p_value_cause_to_effect3 = []
        flag3 = False
        #ce3 = grangercausalitytests([[effect2[i], cause2[i]] for i in range(0, len(cause2))], p)
        ce3_p = granger(cause2,effect2,-1)
        #for key in ce3:
        #    p_value_cause_to_effect3.append(ce3[key][0]["params_ftest"][1])
        #    if ce3[key][0]["params_ftest"][1] < 0.05:
        #        flag3 = True
        if ce3_p < 0.05:
            flag3 = True
        print "effect->cause"
        p_value_effect_to_cause4 = []
        flag4 = False
        #ce4 = grangercausalitytests([[cause2[i], effect2[i]] for i in range(0, len(cause2))], p)
        ce4_p = granger(effect2,cause2,-1)
        #for key in ce4:
        #    p_value_effect_to_cause4.append(ce4[key][0]["params_ftest"][1])
        #    if ce4[key][0]["params_ftest"][1] < 0.05:
        #        flag4 = True
        if ce4_p < 0.05:
            flag4 = True
        if flag3 and flag4:
            print "01 data，Granger two-way cause and effect"
            write_str = write_str + " " + "离散数据，格兰杰双向因果"
            counter11_01 += 1
        elif flag3 and not flag4:
            print "01 data，Granger correct cause and effect"
            write_str = write_str + " " + "离散数据，格兰杰正确因果"
            counter10_01 += 1
        elif not flag3 and flag4:
            print "01 data，Granger wrong cause and effect"
            write_str = write_str + " " + "离散数据，格兰杰错误因果"
            counter01_01 += 1
        elif not flag3 and not flag4:
            print "01 data，Granger no cause and effect"
            write_str = write_str + " " + "离散数据，格兰杰没有因果"
            counter00_01 += 1
        #write_str = write_str + " " + str(min(p_value_cause_to_effect3)) + " " + str(min(p_value_effect_to_cause4))
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
        p = math.pow(2, -(delta_ce - delta_ec))
        if p<1:
            p_array1.append(p)
        else:
            p_array2.append(math.pow(2, -(delta_ec - delta_ce)))
        #f.write(write_str)
        #f.write("\n")
        cause = change_to_zero_one(cause_tmp)
        effect = change_to_zero_one(effect_tmp)
        cause2effect = bernoulli2(effect, length) - cbernoulli2(effect, cause, length)
        effect2cause = bernoulli2(cause, length) - cbernoulli2(cause, effect, length)
        # print 'cause' + ' -> ' + 'effect' + ':' + str(cause2effect)
        # print 'effect' + ' -> ' + 'cause' + ':' + str(effect2cause)
        p = math.pow(2, -(cause2effect - effect2cause))
        if p<1:
            p_array_improve_CUTE1.append(p)
        else:
            p_array_improve_CUTE2.append(math.pow(2, -(effect2cause - cause2effect)))

        cause2effect = bernoulli(effect) - cbernoulli(effect, cause)
        effect2cause = bernoulli(cause) - cbernoulli(cause, effect)
        if p<1:
            p_array_CUTE1.append(p)
        else:
            p_array_CUTE2.append(math.pow(2, -(effect2cause - cause2effect)))

        print
        print "*****************************cut line*****************************"
        print
    #f.close()
    print "连续数据，格兰杰因果关系检验："
    print "双向因果:" + str(counter11)
    print "正确因果:" + str(counter10)
    print "错误因果:" + str(counter01)
    print "没有因果" + str(counter00)
    print "-----------------"
    print "离散数据，格兰杰因果关系检验："
    print "双向因果:" + str(counter11_01)
    print "正确因果:" + str(counter10_01)
    print "错误因果:" + str(counter01_01)
    print "没有因果" + str(counter00_01)
    print "-----------------"
    print "discret  data，snml causality test："
    print "correct cause and effect:" + str(counter_true)
    print "wrong cause and effect:" + str(counter_false)
    print "no cause and effect:" + str(counter_undecided)
    print "-----------------"
    print "01 data，CUTE causality test："
    granger_test = (bh_procedure(p_array_granger1,0.05)+bh_procedure(p_array_granger2,0.05))/1000.0
    ourmodel = (bh_procedure(p_array1,0.05)+bh_procedure(p_array2,0.05))/1000.0
    cute = (bh_procedure(p_array_CUTE1,0.05)+bh_procedure(p_array_CUTE2,0.05))/1000.0
    improve_cute = (bh_procedure(p_array_improve_CUTE1,0.05)+bh_procedure(p_array_improve_CUTE2,0.05))/1000.0
    print granger_test
    print improve_cute
    print ourmodel
    return granger_test,ourmodel,cute,improve_cute


def test_significance(length):
    delta_array = []
    for i in range(0,1000):
        cause, effect = generate_continue_data(200, random.randint(1,3))  # random.randint(1,5)
        cause = normalize(cause)
        cause = zero_change(cause)
        effect = normalize(effect)
        effect = zero_change(effect)
        cause2effect = calculate_difference3(cause, effect, length)
        effect2cause = calculate_difference3(effect, cause, length)
        print 'cause' + ' -> ' + 'effect' + ':' + str(cause2effect)
        print 'effect' + ' -> ' + 'cause' + ':' + str(effect2cause)
        p = math.pow(2, -(cause2effect - effect2cause))
        #p_array.append(p)
        delta_array.append(cause2effect - effect2cause)
    fig = plt.figure()
    axes = fig.add_subplot(111)
    delta_array.sort(reverse=True)
    for i in range(len(delta_array)):
        if delta_array[i] <-math.log(0.05,2):
            #  第i行数据，及returnMat[i:,0]及矩阵的切片意思是:i：i+1代表第i行数据,0代表第1列数据
            axes.scatter(i, delta_array[i], color='grey')
        else:
            axes.scatter(i, delta_array[i], color='green')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()


def up(low,high,num):
    result = []
    for i in range(0,num):
        element = low+i*(high-low)/num
        result.append(element)
    return result


def down(low,high,num):
    result = []
    for i in range(0,num):
        element = high-i*(high-low)/num
        result.append(element)
    return result


def const(c,num):
    result = []
    for i in range(0,num):
        result.append(c)
    return result

from simulate import forward_shift_continue_data

def motivation_test():
    cause = []
    for i in range(0,5):
        cause.extend(up(0.0,1.0,10))
        cause.extend(const(1.0,20))
        cause.extend(down(0.0,1.0,10))
        cause.extend(const(0.0,20))
    noise1=np.random.normal(0, 0.1, len(cause))
    noise2=np.random.normal(0,0.1,len(cause))
    effect =forward_shift_continue_data(cause,8)
    for i in range(0,len(cause)):
        cause[i]+=noise1[i]
        effect[i]+=noise2[i]
    plt.plot(cause)
    plt.plot(effect)
    plt.show()
    print cause
    print effect
    #cause2effect = calculate_difference3(cause, effect, 6)
    #effect2cause = calculate_difference3(effect, cause, 6)
    cause = change_to_zero_one(cause)
    effect = change_to_zero_one(effect)
    cause2effect = bernoulli(effect) - cbernoulli(effect, cause)
    effect2cause = bernoulli(cause) - cbernoulli(cause, effect)
    print 'cause' + ' -> ' + 'effect' + ':' + str(cause2effect)
    print 'effect' + ' -> ' + 'cause' + ':' + str(effect2cause)
    p = math.pow(2, -(cause2effect - effect2cause))
    print p

#motivation_test()


def imbalance_test():
    cause = []
    for i in range(0,500):
        p = random.random()
        if p<0.1:
            cause.append(1)
        else:
            cause.append(0)
    effect = []
    for i in range(0,500):
        p = random.random()
        if p<0.5:
            effect.append(1)
        else:
            effect.append(0)
    cause2effect = bernoulli(effect) - cbernoulli(effect, cause)
    effect2cause = bernoulli(cause) - cbernoulli(cause, effect)
    print 'cause' + ' -> ' + 'effect' + ':' + str(cause2effect)
    print 'effect' + ' -> ' + 'cause' + ':' + str(effect2cause)

#imbalance_test()

def test_sin():
    x = np.arange(0, 5*2 * np.pi, 0.1)
    cause = np.sin(x)
    effect = forward_shift_continue_data(cause,10)
    p1 = granger(cause,effect,10)
    p2 = granger(cause, effect, 10)
    print list(cause)
    print effect
    plt.plot(cause)
    plt.plot(effect)
    plt.show()
    print p1, p2
#cause, effect = generate_continue_data(51, 5)
#print list(cause)
#print list(effect)

def granger_disadvantage_test():
    main = np.random.normal(0, 1, 100)
    noise = np.random.normal(0, 0.1, 100)
    main_max = max(main)
    main_max_index = 0
    main_min = min(main)
    main_min_index = 0
    for i in range(0,100):
        if main[i]==main_max:
            main_max_index = i
        if main[i]==main_min:
            main_min_index = i
    noise[main_max_index+3]=main_max
    noise[main_min_index + 3] = main_min
    print list(main)
    print list(noise)
    p1 = granger(main,noise,3)
    p2 = granger(main,noise,3)
    print p1
    print p2

#granger_disadvantage_test()

#cause = [-0.025278944947613798, 0.0081629713161245256, 0.12716389293513394, 0.0098970273211880719, 0.082150391670884296, -0.0040592865600230961, 0.088852175993307733, 0.046575801767235261, -0.17147342849163844, -0.010761642697761314, -0.28436567407903146, -0.0041658986270868238, 0.060594487638966826, 0.077342265560369508, -0.13317784797332841, -0.0035437682530420353, 0.10229012963748135, -0.072029095680128885, -0.037735147349116052, -0.036099074097138861, -0.018470478304071471, -0.10243690013623485, -0.058876071205011975, 0.021523551772067034, 0.17746508162218075, -0.086974110698661095, -2.349707896846061, 0.014903595659312008, 0.10611708742636382, -0.0056675985101653061, 0.071402520862019467, -0.10200899859259277, -0.024284564494181884, 0.15014010954402124, 0.026599137599380002, -0.21502097163626771, 0.012330793312902502, 0.091265542727170898, -0.2103528142122329, 0.034767631924471319, 2.8258265941215996, -0.038912735570578873, -0.0018814896129807136, -0.087988640800740342, 0.15374071376543341, -0.088020445383417759, 0.040544080737064656, -0.034084071130929226, 0.082625153269708124, -0.042582878948228362, 0.15790222329866088, 0.16787442747511111, -0.027105909488974757, 0.13891347986698754, -0.061053955035784639, 0.082459227424137485, 0.001558593657823084, 0.05847715561524755, -0.043166834838574364, 0.16931845934897474, 0.024200267301552308, -0.0099177394389470715, -0.15837695292589191, 0.07886974789040109, 0.24588164365439719, 0.16803892515709437, -0.0072879786863644484, 0.0066378317964272057, -0.040298880220027228, -0.023071688214004044, 0.095249200734175879, 0.19392571759799951, -0.039053596059179407, 0.098807163250681895, 0.17993139020097051, 0.016222998801966294, -0.21717955130110986, -0.023808759389823183, -0.010632718827491141, -0.17163509383528697, -0.025839447070262301, 0.2224980916039061, 0.17849071878185296, 0.009148206807997647, -0.06979467775145784, -0.089552270318243365, 0.10015845716867217, -0.12591711941896966, -0.15905611075296747, -0.031729467195162397, 0.19069516933020933, -0.053584939128862807, 0.091785831982237262, 0.14613283065564928, 0.057744338799696121, 0.017130752335373051, -0.045989834466322745, -0.074329863108335226, -0.10118129505953488, 0.1015086381082469]
#for i in range(0,len(cause)):
#    cause[i]-=2
#print cause
#test_data(6)
#test_sin()
def night_test():
    final_granger = []
    final_ourmodels = []
    final_cutes = []
    final_improve_cutes=[]
    lengths = [150,250,350,450]
    for length in lengths:
        granger_tests = []
        ourmodels = []
        cutes = []
        improve_cutes = []
        for i in range(0,100):
            granger_test, ourmodel, cute, improve_cute = test_data(6,length)
            granger_tests.append(granger_test)
            ourmodels.append(ourmodel)
            cutes.append(cute)
            improve_cutes.append(improve_cute)
        print granger_tests
        print ourmodels
        print cutes
        print improve_cutes
        print np.mean(granger_tests)
        print np.mean(ourmodels)
        print np.mean(cutes)
        print np.mean(improve_cutes)
        print np.std(granger_tests)
        print np.std(ourmodels)
        print np.std(cutes)
        print np.std(improve_cutes)
        final_granger.append(granger_test)
        final_cutes.append(cutes)
        final_improve_cutes.append(improve_cutes)
        final_ourmodels.append(ourmodels)
    for element in final_granger:
        print element
        print np.mean(element)
        print np.std(element)
    print '****************************************'
    for element in final_cutes:
        print element
        print np.mean(element)
        print np.std(element)
    print '****************************************'
    for element in final_improve_cutes:
        print element
        print np.mean(element)
        print np.std(element)
    print '****************************************'
    for element in final_ourmodels:
        print element
        print np.mean(element)
        print np.std(element)
    print '****************************************'
night_test()
#test_data(6)
#test_significance(6)

