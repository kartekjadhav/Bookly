arr = [1, 2, 3, 4, 5]

def func():
    yield from arr

for i in func():
    print(i)
