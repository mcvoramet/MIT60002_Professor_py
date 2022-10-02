from greedy_algorithm import Food, testGreedys, buildMenu
import random

# `toConsider` Those items that nodes higher up in the tree
# (corresoponding to earlier calls in the recursive call stack) have not yet considered
# `avail` The amount of space still available
# We're not actually build a tree but use tracking result trick.
def maxVal(toConsider, avail):
    """Assumes toCosider a list of items, avail a eight
    Returns a tuple of the total value of a solution to 0/1 knapsack problem 
    and the items of that solution"""
    
    if toConsider == [] or avail == 0: #There's nothing left to consider or there's no available weight
        result = (0, ())               #We couldn't take anything, this is the best of our recursion 
                                       #result = (0, ()) is record the best solution found so far
    elif toConsider[0].getCost() > avail:
        #Explore right branch only
        result = maxVal(toConsider[1:], avail)  #Max value of the remaning elements (If it it max, we don't need to explore the left branch
                                                #we can't affort to put that in the bagpack)

    else:                               #We now have to consider both brancehs (Right and Left)
        nextItem = toConsider[0]
        #Explore Left branch
        withVal, withToTake = maxVal(toConsider[1:],avail - nextItem.getCost())
        withVal += nextItem.getValue()

        #Explore Right branch
        withoutVal, withoutToTake = maxVal(toConsider[1:], avail)

        #Choose better branch
        if withVal > withoutVal:
            result = (withVal, withToTake + (nextItem,))
        else:
            result = (withoutVal, withoutToTake)
        
    return result
        
def testMaxVal(foods, maxUnits, printItems=True):
    print('Use search tree to allocate', maxUnits, "calories")
    val, taken = maxVal(foods, maxUnits)
    print("Total value of items taken =", val)
    if printItems:
        for item in taken:
            print("   ", item)

# Test the result (to select all and comment/uncomment press Cmd+/)
# names = ["wine", "beer", "pizza", "burger", "fries", "cola", "apple",
#         "donut", "cake"]
# values = [89, 90, 95, 100, 90, 79, 50, 10]
# calories = [123, 154, 258, 354, 365, 150, 95, 195]
# foods = buildMenu(names, values, calories)

# testGreedys(foods, 750)
# print('')
# testMaxVal(foods, 750)
# print("\nNote: Search tree give more optimal solution than greedy alogrithm.")

# Let's try search tree on large example

def buildLargeMenu(numItems, maxVal, maxCost):
    items = []
    for i in range(numItems):
        items.append(Food(str(i),
        random.randint(1, maxVal),
        random.randint(1, maxCost)))
    
    return items

# on large example it work but it run very slow as the numItems grow
# for numItems in (5, 10, 15, 20, 30, 35, 40, 45):
#     print('Try a menu with', numItems, 'items')
#     items = buildLargeMenu(numItems, 90, 250)
#     testMaxVal(items, 750, False)



# Let's try modify maxVal function by adding memo (Memoization)
def fastMaxVal(toConsider, avail, memo = {}):
    """Assumes toConsider a list of subjects, avail a weight
         memo supplied by recursive calls
       Returns a tuple of the total value of a solution to the
         0/1 knapsack problem and the subjects of that solution"""
    if (len(toConsider), avail) in memo:
        result = memo[(len(toConsider), avail)]
    elif toConsider == [] or avail == 0:
        result = (0, ())
    elif toConsider[0].getCost() > avail:
        #Explore right branch only
        result = fastMaxVal(toConsider[1:], avail, memo)
    else:
        nextItem = toConsider[0]
        #Explore left branch
        withVal, withToTake =\
                 fastMaxVal(toConsider[1:],
                            avail - nextItem.getCost(), memo)
        withVal += nextItem.getValue()
        #Explore right branch
        withoutVal, withoutToTake = fastMaxVal(toConsider[1:],
                                                avail, memo)
        #Choose better branch
        if withVal > withoutVal:
            result = (withVal, withToTake + (nextItem,))
        else:
            result = (withoutVal, withoutToTake)
    memo[(len(toConsider), avail)] = result
    return result

def testfastMaxVal(foods, maxUnits, printItems=True):
    print('Use search tree to allocate', maxUnits, "calories")
    val, taken = fastMaxVal(foods, maxUnits)
    print("Total value of items taken =", val)
    if printItems:
        for item in taken:
            print("   ", item)

# with memo it make the algorithm run so much faster (less than a second!)
for numItems in (5, 10, 15, 20, 30, 35, 40, 45):
    print('Try a menu with', numItems, 'items')
    items = buildLargeMenu(numItems, 90, 250)
    testfastMaxVal(items, 750, False)