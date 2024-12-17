from Probabilities.ProbMap import ProbMap

# ProbMap for die with X sides (equal chance for all values between 1 and X)
def dX(X):
    result = ProbMap()
    for value in range( 1, X + 1 ):
        result[ value ] = 1 / X
    return result


coin = ProbMap({0:.5,1:.5})

# generate common dice
for die_value in [4,6,8,10,20,100]:
    globals()[f"d{die_value}"] = dX(die_value)


