# def myyield():
#     for i in range(3):
#         yield i
#     for j in range(2):
#         yield j
#
# for j in myyield():
#     print(j)




def yield2():
    yield 1;
    yield 3;

y = yield2()
print(y.__next__())
print(y.__next__())