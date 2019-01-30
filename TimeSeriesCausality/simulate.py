import numpy as np

import math
# generate continue cause and effect
def generate_continue_data(length, shift):
    cause = []
    main = np.random.normal(0, 1, length)
    noise = np.random.normal(0, 0.1, length)
    for i in range(0, length):
        if i == 0:
            cause.append(main[i])
        else:
            cause.append(cause[i - 1] + main[i])
    effect = forward_shift_continue_data(cause, shift)
    for j in range(0, length):
        effect[j] = effect[j] + noise[j]
    #for x in range(0, len(effect)):
        #effect[x] = effect[x] + abs(min(effect)) + 0.1
        #effect[x] = 1.0/effect[x]#math.pow(effect[x], 3)
        #if effect[x]<0:
            #effect[x] = effect[x]/2
        #effect[x] = math.tanh(effect[x])
    return cause, effect

import random
# generate continue cause and effect
def generate_continue_data_with_change_lag(length, segment_length):
    cause = []
    main = np.random.normal(0, 1, length)
    noise = np.random.normal(0, 0.3, length)
    for i in range(0, length):
        if i == 0:
            cause.append(main[i])
        else:
            cause.append(cause[i - 1] + main[i])
    effect = list(cause)
    head = 0
    counter = 0
    while head<length:
        start = counter*segment_length
        if (counter+1)*segment_length<length:
            end = (counter+1)*segment_length
        else:
            end = length
        lag = random.randint(1,6)
        for i in range(start+lag,min([end+lag,length])):
            effect[i] = cause[i-lag]
        head+=segment_length
        counter+=1
    for j in range(0, length):
        effect[j] = effect[j] + noise[j]
    return cause, effect


# generate continue cause and effect
def generate_continue_data2(length, shift):
    cause = []
    main = np.random.normal(0, 1, 10)
    noise = np.random.normal(0, 0.1, length)
    for i in range(0, len(main)):
        if i == 0:
            cause.append(main[i])
        else:
            cause.append(cause[i - 1] + main[i])
    for i in range(0,length-len(main)):
        next_value = np.random.normal(0, np.std(cause), 1)[0]
        cause.append(next_value)
    effect = forward_shift_continue_data(cause, shift)
    for j in range(0, length):
        effect[j] = effect[j] + noise[j]
    return cause, effect


# move the coninue sequence forward by shift bits
def forward_shift_continue_data(seq, shift):
    lseq = len(seq)
    sseq = [None] * lseq
    for i in xrange(lseq):
        if i >= shift:
            sseq[i] = seq[i - shift]
        else:
            sseq[i] = np.random.normal(0, 1, 1)[0]
    return sseq