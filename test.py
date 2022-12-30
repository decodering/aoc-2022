def divby2(n):
    num = 0
    while num < n:
        yield num / 2
        num += 1


print([i for i in divby2(100)])
