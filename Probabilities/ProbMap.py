from copy import copy
import random

MAX_CHANCE_ERROR = .00000000000001

# returns a list of all provided values between
#   range_min and range_max inclusive
# if values is None, returns a range that includes
#   all integers between range_min and range_max inclusive
# if range_min is None, there will be no minimum requirement
def filter_values( values = None, range_min = None, range_max = None ):
    # if values is a single value, convert to a list with that value
    if isinstance( values, int ):
        values = [values]

    # if values are not specified, return all values between min and max
    if values == None:
        return range( range_min, range_max + 1 )

    # return provided values that meet range requirements
    return [value for value in values
                if( ( range_min == None or value >= range_min )
                    and
                    ( range_max == None or value <= range_max ) )]




# map of <quantity> to <chance>
#   quantity is int
#   chance is float (0-1)
#   sum of chances is 1.0
#   any unused chance are applied to quantity=0
# NOTE: if the chance of 0 is less than MAX_CHANCE_ERROR,
#   the key of 0 will automatically be removed
class ProbMap(dict):
    # self: map of quanitiy -> chance
    # __set_percent: total percentage of the ProbMap used (excluding 0)

    # ProbMap() - 100% chance of 0
    #    - ProbMap()
    # ProbMap(dictionary) - set all key/values
    #    - ProbMap( {3:.01,5:.2} )
    # ProbMap(int) - 100% chance of value
    #    - ProbMap( 3 )
    def __init__( self, *args ):
        self.__set_percent = 0.0
        super().__setitem__( 0, 1 - self.__set_percent )

        # no more than one argument
        if len( args ) > 1:
            raise TypeError( "ProbMap expected at most 1 argument, got 2" )

        # zero arguments - default
        if len( args ) == 0:
            return



        # otherwise, exactly one argument
        arg = args[ 0 ]

        # store all keys if dictionary
        if isinstance( arg, dict ):
            for key,value in arg.items():
                self[ key ] = value
            return

        # not a dictionary - set 100% chance for argument
        self[ arg ] = 1.0




    # <int,float> -> set chance to get specified int
    # <ProbMap,float> -> set chance to get the ProbMap
        # NOTE: changing the value of the inserted ProbMap later
        #       will not effect this instance
    def __setitem__( self, quantity, chance ):
        # verify chance
            # verify type
        if not isinstance( chance, float ):
            raise TypeError( "ProbMap expected float as chance, " + 
                             f"but received {type(chance)}." )
            # verify value
        if isinstance( quantity, ProbMap ):
            chance_mod = chance
        else:
            chance_mod = chance - self[ quantity ]

        new_set_percent = self.__set_percent + chance_mod
        
        # fail if total percentage > 1
        if new_set_percent > 1.000001:
            raise ValueError( "Attempted to set chance from " + 
                              f"{self.__set_percent} to {new_set_percent}, " + 
                              "which is greater than 1.0\n" + 
                              "NOTE: Use values from 0-1 instead of percents" )

        if quantity == 0:
            self.__set_percent += chance
            return None
        
        ################### Process Data ###################
        # int: set chance of getting quantity
        if isinstance( quantity, int ):
            super().__setitem__( quantity, chance )

        # ProbMap: add chance of getting each value
        elif isinstance( quantity, ProbMap ):
            for subQuant, subChance in quantity.items():
                self[ subQuant ] += subChance * chance

        # ERROR: invalid quanitity type        
        else:
            raise TypeError( "ProbMap expected int or ProbMap as key, " + \
                             f"But received {type(quantity)}." )
        ############## Process Data End ####################

        # after processing successful, update set_percentage
        self.__set_percent = new_set_percent

        # temporarily remove the chance of 0
        if 0 in self.keys():
            self.pop( 0 )

        # set any significant remaining chance into 0
        rem_chance = 1 - sum( self.values() )
        if rem_chance > MAX_CHANCE_ERROR:
            lowest_value = 0
            super().__setitem__( 0, rem_chance )


    def __getitem__( self, index ):
        if index not in self.keys():
            return 0.0
        return super().__getitem__( index )



    # combines values from each ProbMap
    def __add__( self, probMap ):
        if not isinstance( probMap, ProbMap ):
            raise TypeError( "Can only add type ProbMap to ProbMap" )
        result = ProbMap()
        for q1,c1 in self.items():
            for q2,c2 in probMap.items():
                # exclude rounded zeros
                if ( c1 < .0000001 and q1 == 0 ) or \
                   ( c2 < .0000001 and q2 == 0 ):
                    continue
                
                # add chance to get both to result
                result[q1 + q2] += c1 * c2
        return result

    def display_map( self ):
        print( "ProbMap Display:" )
        for quantity, chance in self.items():
            print( f"chance of {quantity} = {chance}" )
        print()

    def __mul__( self, num_instances ):
        if not isinstance( num_instances, int ):
            raise TypeError( "Can only multiply type int to ProbMap" )
        # optimized multiplication algorithm by repeated addition
        baseProbMap = self
        multiplier = ProbMap()
        result = ProbMap()

        while num_instances:
            if num_instances & 1:
                result = result + baseProbMap

            num_instances >>= 1
            if num_instances:
                baseProbMap = baseProbMap + baseProbMap

        return result

    def generate_cumulative_table(self, max_instances, max_amount):
        # calcaulte height and width, including maximums
        height = max_instances+1
        width = max_amount+1

        # create width x height table
        result = [[0.0]*width for row_index in range(height)]

        # iterate over all values in table
        for instance_index in range( height ):
            for amount_index in range( width ):

                # total chance of success
                total_chance = 0.0
                
                # iterate over all values in self
                for prob_amount,prob_chance in self.items():

                    # calculate position of existing relevant data
                    prev_amount_index = amount_index - prob_amount
                    prev_instance_index = instance_index - 1

                    
                    # previous instance is negative -> no instances -> failure
                    if prev_instance_index < 0:
                        prev_chance = 0.0
                    # previous amount is non-positive -> sufficient units -> success
                    elif prev_amount_index <= 0:
                        prev_chance = 1.0
                    # otherwise, get chance directly from table
                    else:
                        prev_chance = result[prev_instance_index][prev_amount_index]


                    # calculate chance due to data at the position
                    total_chance += prev_chance * prob_chance

                # store the resulting data into the table
                result[instance_index][amount_index] = total_chance
        
        return result

    def display_cumulative_table( self, amount_filter,
                                        instance_filter=[1], 
                                        amount_label = "units", 
                                        instance_label = "instances" ):
        # generate data
        max_instances = max(instance_filter)
        max_amount = max(amount_filter)
        max_amount = int(max_amount)+1 # roundup
        table = self.generate_cumulative_table(max_instances, max_amount)

        # filter invalid indices
        instance_filter = filter_values( instance_filter, 0, len(table) )
        amount_filter = filter_values( amount_filter, 0, len(table[0]) )


        # store data into string
        result = str()
        # add title row
        result += "{:>18}\n".format(amount_label)
        result += "{:<8}".format(instance_label)
        for amount_ind in amount_filter:
            result += '{:10d}'.format( amount_ind )
        result += "\n"

        # add data from table
        for instance_ind in instance_filter:
            result += '{0: 6d} :'.format( instance_ind )
            for amount_ind in amount_filter:
                result += '{0: 9.3f}%'.format(table[instance_ind][amount_ind]*100)
            result += "\n"

        print(result)

    def display( self ):
        print("Probability map display")
        for key,value in self.items():
            print(f"{key}: {value}")

    # generate a random value using the chances
    def random( self ):
        rand_key = random.random()
        for amount,chance in self.items():
            rand_key -= chance
            if rand_key <= 0.0:
                return amount
        # no values identified - try again
        print( "WARNING: ProbMap.random() was unable to find an amount: retrying" )
        return self.random()



