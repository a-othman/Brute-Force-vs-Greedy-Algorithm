import time

#From codereview.stackexchange.com                    
def partitions(set_):
    if not set_:
        yield []
        return
    for i in range(2**len(set_)//2):
        parts = [set(), set()]
        for item in set_:
            parts[i&1].add(item)
            i >>= 1
        for b in partitions(parts[1]):
            yield [parts[0]]+b


# This is a helper function that will fetch all of the available 
# partitions for you to use for your brute force algorithm.
def get_partitions(set_):
    counter = 0
    for partition in partitions(set_):
        counter +=1
        yield [list(elt) for elt in partition]


def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    cow_dict = dict()

    f = open(filename, 'r')
    
    for line in f:
        line_data = line.split(',')
        cow_dict[line_data[0]] = int(line_data[1])
    return cow_dict



### Enter your code for the Greedy Cow Transport here 
#Helper functions
def cows_Info(cows):
    ''' Takes in a dictionariy including names and weights
        returns a tulpes insde a list. Each tuple has the cow name and weight
    '''
    cows_Names = list(cows.keys())
    cows_Weights = list(cows.values())
    Call = list(zip(cows_Weights, cows_Names)) 
    Call.sort(reverse= True)  
    return Call


def listtodic(lst):
    """
    Takes in a list
    Returns a dictionary
    """
    dct= {}
    for i in range(len(lst)):
           dct[lst[i][1]]=lst[i][0]
    return dct
#Main code for the greedy algorithm         
def greedy_cow_transport(cows,limit, All_Trips=None):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    if not All_Trips:
        All_Trips = []

    cows = cows_Info(cows)
    cows_copy = cows[:]
    trip_List = []
    temp_limit = limit
    if len(cows_copy)==0:
       # print(All_Trips)
        return All_Trips
    for i in range(len(cows)):
        if temp_limit >0:
            if cows[i][0] <= temp_limit:
                trip_List.append(cows[i][1])
                temp_limit -= cows[i][0]
                cows_copy.remove(cows[i])
    updated_cows = listtodic(cows_copy)
    All_Trips.append(trip_List)
    return greedy_cow_transport(updated_cows,limit, All_Trips=All_Trips)


# Enter your code for the Brute Force Cow Transport here 
def brute_force_cow_transport(cows,limit):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    cowslst = list(cows.keys())
    lst = []
    for item in get_partitions(cowslst):
        lst.append(item)
    lst_f= lst.copy()
    for i in lst:
        for j in i:
            sum_ = 0
            for k in j:
                sum_ += cows[k]
                if sum_ > limit:
                    try:
                        lst_f.remove(i)
                        break
                    except ValueError:
#                        pass
                        break
    trips_map= lst_f[0]
    for i in range(1,len(lst_f)): 
        if len(trips_map) > len(lst_f[i]):
            trips_map= lst_f[i]
            if lst_f[i] == lst_f[-1]:
                return trips_map
    return trips_map


#Testing an Example:
cows = load_cows("ps1_cow_data.txt")
limit=10
#print(cows)


def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    #time it takes greedy algorith to finish
    tic1= time.time()
    greedy_cow_transport(cows,limit, All_Trips=None)
    toc1= time.time()
    time1= toc1-tic1
    
    #time it takes brute force algorith to finish
    tic2= time.time()
    brute_force_cow_transport(cows,limit)
    toc2= time.time()
    time2= toc2-tic2
    return ("Time it took greedy algorith is", time1,
            "Time it took brute force algorithm", time2)
    
