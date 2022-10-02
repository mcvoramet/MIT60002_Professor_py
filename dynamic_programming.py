# Recursive Implementation of Fobonnaci

def fib(n):
    if n==0 or n==1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

# code is running slower and slower (exponential time complexity)
# solve by store an anwer and look it up when you need it because
# we doing the same thing that produce the same result repeatly. 
# (store that thing that occured repeatly)

# Use Cmd + / to comment/uncomment all at once.
# for i in range(121):                  #even at small number like 34 it start to get very slow
#     print("fib(" + str(i) + ") =", fib(i))



# Use Memoization to solve the slowness of recursion (trade off with space)
# Before computing, check if value have already benn computed
# if so we look it up and return it
# otherwise, compute it and store in table (memo)
def fastFib(n, memo = {}):
    """Assumes n is an int >= 0, memo used only by resursive calls
    Returns Fibonacci of n"""
    if n ==0 or n == 1:
        return 1
    try:                    # if try doesn't work, meaning no value in the table then go to except: (compute it and store it)
        return memo[n]
    except KeyError:
        result = fastFib(n-1, memo) + fastFib(n-1, memo) # Compute it 
        memo[n] = result # Store it in memo
        return result

# now it take less than a second to compute all 121
for i in range(121):
    print("fastFib(" + str(i) + ") =", fastFib(i))
