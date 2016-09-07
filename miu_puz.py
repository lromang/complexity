## -------------------------------------------------------------
## Luis Manuel Román García
## -------------------------------------------------------------

################################################################
## -------------------------------------------------------------
##                        MIU - PUZZLE
## -------------------------------------------------------------
##
## This script contains several routines to create a statistical
## argument against the possibility of forming the string 'MU'
## From the string 'MI' using the following rules:
## 1.- MxI    -> MxIU
## 2.- Mx     -> Mxx
## 3.- MxIIIx -> MxUx
## 4.- MxUUx  -> Mxx
################################################################

################################
## Libraries
################################
import numpy as np
import matplotlib.pyplot as plt
import random
import re

################################
## Functions
################################
test = "MI"

## -----------------------------------
## Addu:
## This function performs rule
## 1. MxI -> MxU. With a probability
## of .5
def addu(string):
    if random.randint(0,1) == 1 and string[-1] == 'I':
        return string + 'U'
    return string

## -----------------------------------
## Duplicate:
## This function performs rule
## 2. Mx -> Mxx. With a probability
## of .5
## -----------------------------------
def duplicate(string):
    if random.randint(0,1) == 1:
        return string + string[1:]
    return string

## -----------------------------------
## Iforu:
## This function performs rule
## 3. MxIIIx -> MxUx. With a probability
## of .5 to one instance of III.
## -----------------------------------
def iforu(string, begIndex):
    if random.randint(0,1) == 1:
        return string[:begIndex] + 'U' + string[(begIndex + 3):]
    return string

## -----------------------------------
## Niforu:
## This function performs rule
## 3. MxIIIx -> MxUx. With a probability
## of .5 to any instances of III.
## -----------------------------------
def niforu(string):
    ## All instances of III
    indexes = [m.start() for m in re.finditer('(?=III)', string)]
    ## Select one for change
    if len(indexes) > 0:
        index = random.sample(indexes, 1)[0]
    else:
        index = len(string)
    return iforu(string, index)

## -----------------------------------
## Ufornot:
## This function performs rule
## 4. MxUUx -> Mxx. With a probability
## of .5 to one instance of UU.
## -----------------------------------
def ufornot(string, begIndex):
    if random.randint(0,1) == 1:
        return string[:begIndex] + string[(begIndex + 2):]
    return string

## -----------------------------------
## Niforu:
## This function performs rule
## 4. MxUUx -> Mxx. With a probability
## of .5 to any instances of UU.
## -----------------------------------
def nufornot(string):
    ## All instances of  UU
    indexes = [m.start() for m in re.finditer('(?=UU)', string)]
    ## Select one for change
    if len(indexes) > 0:
        index = random.sample(indexes, 1)[0]
    else:
        index = len(string)
    return ufornot(string, index)

## -----------------------------------
## Apply rule:
## Randomly applies any of the rules
## of the system
## -----------------------------------
def apply_rule(string):
    new_string = string # Auxiliar string
    while new_string == string: # Avoid returning string without change
        rule = random.randint(1, 4)
        if rule == 1:
            new_string =  addu(string)
        if rule == 2:
            new_string =  duplicate(string)
        if rule == 3:
            new_string =  niforu(string)
        if rule == 4:
            new_string = nufornot(string)
    return new_string

## -----------------------------------
## Iterate:
## This function applies all the rules
## in different order and stops when
## getting "MU" (never) or after M
## applications
## -----------------------------------
def iterate(string, M = 10):
    count   = 0
    while string != "MU" and string != "M" and count < M:
        string = apply_rule(string)
        count  = count + 1
    return string

## -----------------------------------
## Mean and Sd:
## Obtains the average and standard
## deviation of N iterations of M
## rules applied.
## -----------------------------------
def mean_str(string, N = 1000, M = 10):
    lengths = []
    for i in range(N):
        new_string = iterate(string, M)
        lengths.append(len(new_string))
    return np.mean(lengths)

## -----------------------------------
## Mean, Sd dist:
## Obtains the average and standard
## deviation of N iterations of M
## rules applied.
## -----------------------------------
def mean_dist(string, boots = 1000, N = 1000, M = 10):
    mean_d = []
    for i in range(boots):
        mean = mean_str(string, N, M)
        mean_d.append(mean)
    return mean_d

## -----------------------------------
## Means distribution
## -----------------------------------
means = mean_dist("MI", 100, 1000, 10)

## Histogram
plt.hist(means)
plt.show()

## -----------------------------------
## Test of hypothesis
## -----------------------------------
