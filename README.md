# ProbabilityTool
Helps calculate the probability of events

This tool was designed to calculate the chances of getting at least X 'value' from the sum of several events. (This can be used to quickly derive exactly X or less than X)

Example Usage:\
Import the libraries
```
from Probabilities.ProbMap import ProbMap
from Probabilities.ProbMap_Tools import coin, dX, d4, d6, d10, d100
```
Displaying the pre-made ProbMaps
```
coin.display() # this will display .5 for 0 and .5 for 1, thus a 50% chance for head or tails
d6.display() # .1666 (or 1/6) for all values between 1 and 6
```
ProbMap math
```
# adding the same ProbMap
two_coins = coin + coin # add two coints
two_coins.display() # 25% chance to get 0 or 2, 50% chance to get exactly 1 head

# adding many of the same ProbMap
four_coins = coin * 4 # sum of four coins
four_coins.display() # display chance to get any possible quantity of heads

# adding many of different ProbMaps
total = d4 * 4 + d6 * 2 # rolling four d4 and two d6
total.display()
```
A ProbMap Table will filter what information is displayed
```
# two d6
total = d6*2
total.display() # displays 11 different values (2-12)
2: 0.027777777777777776
3: 0.05555555555555555
4: 0.08333333333333333
5: 0.1111111111111111
6: 0.1388888888888889
7: 0.16666666666666669
8: 0.1388888888888889
9: 0.1111111111111111
10: 0.08333333333333333
11: 0.05555555555555555
12: 0.027777777777777776

total.display_cumulative_table(amount_filter=[5,10])
             units
instances         5        10
     1 :   83.333%   16.667%
# This shows with one set of 2d6, there is 83% chance to get to get at least a total of 5, and a 16% chance to get at least a total of 10.

d6.display_cumulative_table(instance_filter=[1,3,5,10], amount_filter=[1,5,10,15,20])
             units
instances         1         5        10        20
     1 :  100.000%   33.333%    0.000%    0.000%
     3 :  100.000%   98.148%   62.500%    0.000%
     5 :  100.000%  100.000%   98.380%   30.517%
    10 :  100.000%  100.000%  100.000%   99.852%
# this shows the chances of getting a total of at least 1, 5, 10, and 20 using 1, 3, 5, or 10 d6. \
The chance of getting at least 20 from 10d6 is 99.8, and the chance of getting at least 20 from 3d6 is 0.0%. 
```
Custom ProbMaps
```
# Example: 50% chance to get 0, 25% chance to get 1, and 25% chance to get 5
# Method 1: Initialize in the constructor
my_map = ProbMap( {1:.25,5:.25} ) # Note that 0 will be automatically set to make the total equal to 1. 
my_map.display()
# Method 2: Initialize empty, set values later
my_map = ProbMap()
my_map[1] = .25
my_map[2] = .25 # Again, 0 will be automatically set
my_map.display()
```
Nested ProbMaps
```
# Setting every chance individually may be time-consuming
# Nested ProbMaps is the ability to set a chance to have a value of another ProbMap
# Example: There is 50% chance to roll a d6, 25% chance to roll a d4, and a 25% chance that gaurantees 2
# (Method 1 dooes not support using objects as dictionary keys)
# Method 2
nested_map = ProbMap()
nested_map[d6] = .5
nested_map[d4] = .25
nested_map[2] = .25
nested_map.display()
```
RNG
```
# simulate a d100 100 times
print([d100.random() for _ in range(100)])
[30, 76, 90, 32, 89, 30, 63, 23, 80, 48, 80, 73, 66, 13, 100, 6, 18, 37, 81, 10, 75, 76, 23, 9, 98, 20, 99, 13, 36, 8, 12, 18, 46, 28, 62, 8, 53, 9, 81, 63, 67, 87, 23, 55, 100, 27, 67, 14, 3, 34, 52, 10, 67, 98, 47, 22, 18, 36, 84, 85, 17, 87, 20, 91, 77, 19, 70, 41, 66, 26, 45, 48, 66, 48, 59, 3, 23, 81, 2, 28, 11, 86, 14, 28, 1, 22, 5, 60, 37, 92, 82, 3, 51, 23, 34, 35, 63, 25, 21, 48]
```
