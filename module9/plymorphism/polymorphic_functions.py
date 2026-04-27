def add(x, y):
    return x + y

def concatenate(x, y):
    return str(x) + str(y)

def operate(operation, x, y):
    return operation(x, y)

result_sum = operate(add,3,5)
print("Result of sum:", result_sum)

result_concatenate = operate(concatenate,"Hello","World")
print("Result of concatenate:", result_concatenate)