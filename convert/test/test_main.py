#   调用read()方法可以一次读取文件的全部内容，Python把内容读到内存，用一个str对象表示
#       所以，要保险起见，可以反复调用read(size)方法，每次最多读取size个字节的内容
#   调用readline()可以每次读取一行内容
#   调用readlines()一次读取所有内容并按行返回list


"""
# [::]

a='sad asd asd asd sad asd dds dsf '
print(a[::2])
print(a[-1:-1])
print(a[::])
print(a.find('asd'))
"""

a = ['xiao', 'wang', 'xiao', 'zhang', 'xiao', 'hua']

'''
#   try: join title rjust input

A = ' '.join(a).title().split(' ')
print(A)
print('add'.center(30))
print(A)
temp = input('please input name:'.ljust(20))
A.append(temp)
print('after add:'.ljust(20), end='')
print(A)
'''

b = ['sada']
print(a)
print(b)
b.extend(a[-1::-1])
print(b)
b.insert(2, a[2:5])
print(b)
print(b.count('xiao'))
# b.pop()
# print(b)
# del b[2]
# print(b)
b.remove('xiao')

c = {'name': 'sadas', 'sex': 'nan'}
print(c)
del c['sex']
print(c)
c.clear()
print(c)

print('xiao' in a)
while 'xiao' not in a:
    a.remove('xiao')
print(a)

help(print)

with open('/home/l/PycharmProjects/daily-strutil/docs/test.txt', 'r') as f:
    print('read data : ' + f.read(3))
    position = f.tell()
    print("position:  %s" % position)
    # why is error?
    # f.seek(3, 2)
    print("position:  %s" % position)


import os


os.mkdir('test_os')
print(os.listdir("./"))
root = os.getcwd()
print(root)
os.rename(os.path.join(root, 'test_os'), os.path.join(root, 'new_test_os'))
print(os.listdir("./"))
os.rmdir(os.path.join(root, 'new_test_os'))
print(os.listdir('./'))
