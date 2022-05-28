b = input('输入两个数字').split(',')
lis = []
lis1 = []
for i in b:
    lis.append(int(i))

for i in range(lis[0], lis[1]):
    for a in range(2, i):
        if i % a == 0:
            break
    else:
        lis1.append(i)
print(lis)
print(lis1)
print('5555555555555')
