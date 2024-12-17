from Probabilities.ProbMap import ProbMap

# ProbMap for die with X sides (equal chance for all values between 1 and X)
def dX( X ):
    result = ProbMap()
    for value in range( 1, X + 1 ):
        result[ value ] = 1 / X
    return result

if __name__ == "__main__":
    TEST_MAP_SUBSET1 = False
    TEST_MAP_SUBSET2 = False
    TEST_ADD = False
    TEST_INIT_ARGS = False
    TEST_MULT = False
    TEST_GRID = False
    TEST_RANDOM = False
    
    if TEST_MAP_SUBSET1:
        my_map = ProbMap()
        my_map[ 1 ] = .5
        my_map[ 2 ] = .5

        my_map2 = ProbMap()
        my_map2[ 3 ] = .25
        my_map2[ 4 ] = .25
        my_map2[ my_map ] = .5
        my_map2.display()
        print( "Expected 1, 2, 3, 4 -> .25" )

        my_map2 = ProbMap()
        my_map2[ 1 ] = .25
        my_map2[ 3 ] = .25
        my_map2[ my_map ] = .5
        my_map2.display()
        print( "Expected 1->.5, 2->.25, 3->.25" )

    if TEST_MAP_SUBSET2:
        my_map = ProbMap()
        for i in range( 1,9 ):
            my_map[ i ] = .1

        my_map2 = ProbMap()
        for i in (3, 6, 9, 12, 15, 18):
            my_map2[ i ] = .05

        my_map.display()
        my_map2.display()

        my_map2[ my_map ] = .5
        my_map2.display()
        print( "Expecting:" )
        print( "1,2,4,5,7,8 -> .5*.1 = .05" )
        print( "3,6 -> .05+.5*.1 = .1" )
        print( "9,12,15,18 -> .05" )

    if TEST_ADD:
        my_map = ProbMap()
        my_map2 = ProbMap()
        for i in range( 6 ):
            my_map[ i + 1 ] = 1/6
            my_map2[ i + 1 ] = 1/6

        my_map3 = my_map + my_map2
        for quantity,chance in my_map3.items():
            print( f"{quantity}: {chance*36} / 36" )
        print( "Expected 2->1, 3->2, 4->3, ..., 7->6, 6->5, ..., 12->1" )

        # my_map1 (d6)
        my_map1 = ProbMap()
        my_map1_s0 = ProbMap()
        my_map1_s1 = ProbMap()

        my_map1_s0[ 1 ] = .5
        my_map1_s0[ 6 ] = .5
        my_map1_s1[ 2 ] = 1/3
        my_map1_s1[ 5 ] = 1/3
        my_map1_s1[ 4 ] = 1/3

        my_map1[ my_map1_s0 ] = 2/6
        my_map1[ my_map1_s1 ] = 3/6
        my_map1[ 3 ] = 1/6

        # my_map2 (coin)
        my_map2 = ProbMap()
        my_map2[ 1 ] = .5
        my_map2[ 0 ] = .5


        my_map1.display()
        my_map2.display()

        my_map3 = my_map1 + my_map2
        my_map3.display()
        print( "Expected 1,7->x ; 2,3,4,5,6->2x" )
        print( "x = 1 / ( 2 + 5 * 2 ) = .0833..." )
        print( "2x = 2 * x = .1666..." )

    if TEST_GRID:
        # PART 1
        myMap = ProbMap()
        myMap[1] = 1/2

        result_map = myMap.generate_cumulative_table(20,10)


        # PART 2
        myMap = ProbMap()
        myMap[1] = 1/2

        result_str = myMap.display_cumulative_table(instance_filter = [1,2,5,10,15,20],
                                   amount_filter = [1,3,5,10],
                                   instance_label = "instance2",
                                   amount_label = "amount2")

    if TEST_RANDOM:
        myMap = ProbMap()
        myMap[1] = .5
        results = [myMap.random() for i in range( 50 )]
        print( " ".join([str(i) for i in results]) )
        print()
        
        myMap = ProbMap({1:1/6,2:1/6,3:1/6,4:1/6,5:1/6,6:1/6})
        results = [myMap.random() for i in range( 50 )]
        print( " ".join([str(i) for i in results]) )
        print()

        myMap = ProbMap({1:1/6,2:1/6,3:1/6,4:1/6,5:1/6,6:1/6})
        results = [myMap.random() for i in range( 50 )]
        print( " ".join([str(i) for i in results]) )
        print()


        standard_orb = ProbMap()
        standard_orb[ 6 ] = .4698
        standard_orb[ 8 ] = .2685
        standard_orb[ 10 ] = .1342
        standard_orb[ 12 ] = .0671
        standard_orb[ 20 ] = .0336
        standard_orb[ 40 ] = .0134
        standard_orb[ 60 ] = .0067
        standard_orb[ 80 ] = .0054
        standard_orb[ 180 ] = .0013

        # Standard unlock orb
        standard_orb = ProbMap(
        {
          6: .4698, 
          8: .2685, 
         10: .1342, 
         12: .0671, 
         20: .0336, 
         40: .0134, 
         60: .0067, 
         80: .0054, 
        180: .0013
        } )


        myMap = standard_orb
        results = [myMap.random() for i in range( 1000 )]
        print( " ".join([str(i) for i in results]) )
        print()






