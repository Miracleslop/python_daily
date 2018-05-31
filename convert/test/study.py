L = ['Michael', 'Sarah', 'Tracy', 'Bob', 'Jack']
print(L[0], L[1], L[2])
print(L[-2:])

L = list(range(100))
print(L[-10::2])

for i, v in enumerate(L):
    print(i, v, end=' ')

L = [x * x for x in range(0, 5)]
print(L)

g = (x * x for x in range(0, 5))
print(next(g))


def fib(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b
        a, b = b, a + b
        n = n + 1
    return 'done'


f = fib(10)

for i in range(0, 10):
    print(next(f), end=' ')

print()

for n in fib(6):
    print(n, end=' ')

print()

g = fib(6)
while True:
    try:
        x = next(g)
        print('g:', x)
    except StopIteration as e:
        print('Generator return value', e.value)
        break

for x in {1, 2, 3, 4, 5}:
    pass

it = iter([1, 2, 3, 4, 5])
while True:
    try:
        x = next(it)
        print(x, end=', ')
    except StopIteration:
        break

print()
from functools import reduce

DIGITS = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}

#l = lambda s: reduce(lambda x, y: x * 10 + y, map(lambda x: DIGITS[x], map(lambda x: x, s)))

#print(l(filter(lambda x: isinstance(x, str), ('6156', '1651'))))
