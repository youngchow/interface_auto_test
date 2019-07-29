import itertools
from itertools import *

team = ['a','b','c','d']
print('***'*4)
print('***'*4)
category = itertools.permutations(team)
print(category)
print(list(category))

cata = itertools.permutations(team,2)
print(list(cata))

# for i in count(1):
#     print(i)


# for i in zip([1,2,3,4], ['a', 'b', 'c']):
#     print(i)
# for i in zip(count(2), ['a', 'b', 'c']):
#     print(i)
#
# for i in repeat('hello python',10):
#     print(i)
#
#
# for i in chain([1,2,3],['a',5,6]):
#     print(i)
#
#
# a = ['aa', 'ab', 'abc', 'bcd', 'abcde']
# for i, k in groupby(a,len):
#     print(i,k)
#     print(i,list(k))
#
# print('stop at 5')
# for i in islice(count(),5):
#     print(i)
#
# print ('Start at 5, Stop at 10:')
#
# for i in islice(count(),5,10):
#     print(i)
# print('By tens to 100:')
# for i in islice(count(),0,101,10):
#     print(i)
# for i in islice(['a','b','c','d',1,2,3,4,],5):
#     print(i)

# print('Doubles:')
# for i in map(lambda x:2*x, range(5)):
#     print(i)
# print('Multiples:')
# for i in map(lambda x,y:(x, y, x*y), range(5), range(5,10)):
#     print(i)
# values = [(0, 5), (1, 6), (2, 7), (3, 8), (4, 9)]
# for i in starmap(lambda x,y:(x, y, x*y), values):
#     print(i)


a = (1, 2, 3)
b = ('A', 'B', 'C')
c = itertools.product(a,b)
for elem in c:
    print(elem)

list = [1,2,3,4,5,6,7,8,9,0,1,2,3,4,5]
for i in list[0:5]:
    print(i)
for i in islice(list,5):
    print(i)
