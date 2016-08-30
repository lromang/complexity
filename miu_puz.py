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
## of .5 to one instance of III.
## -----------------------------------
def ufornot(string, begIndex):
    if random.randint(0,1) == 1:
        return string[:begIndex] + string[(begIndex + 2):]
    return string

## -----------------------------------
## Niforu:
## This function performs rule
## 4. MxUUx -> Mxx. With a probability
## of .5 to any instances of III.
## -----------------------------------
def nufornot(string):
    ## All instances of III
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
    rule = random.randint(1, 3)
    if rule == 1:
        return addu(string)
    if rule == 2:
        return duplicate(string)
    if rule == 3:
        return niforu(string)
    return nufornot(string)

## -----------------------------------
## Iterate:
## This function applies all the rules
## in different order and stops when
## getting "MU" (never) or after M
## iterations
## -----------------------------------
def iterate(string, M = 100):
    count   = 0
    lengths = []
    while string != "MU" and string != "M" and count < 100:
        string = apply_rule(string)
        count  = count + 1
        lengths.append(len(string))
        # print(string)
    return lengths

## -----------------------------------
## Mean dist:
## Obtains the average distribution of
## N iterations of iterate
## -----------------------------------
def mean_dist(string, N = 1000, M = 100):
    means = []
    for i in range(N):
        lengths = iterate(string, M)
        means.append(np.mean(lengths))
    return means

## -----------------------------------
## Test
## -----------------------------------
means = mean_dist("MI")

## Histogram
plt.hist(means)
plt.show()
