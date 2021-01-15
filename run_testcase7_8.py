import os
print('Input the test case you want to run!')
x = int(input())

os.system('./clean.sh')

if x == 7:
    com = 'rm my.out'
    os.system(com)
    for i in range(1, 4):
        print('Running test data', i)
        com = 'time ./code < BasicDataSet/testcase7/' + str(i) + '.txt >> my.out'
        os.system(com)
    print("Diffing Output")
    os.system('diff my.out BasicDataSet/testcase7/ans.txt')

if x == 8:
    com = 'rm my.out'
    os.system(com)
    for i in range(1, 101):
        print('Running test data', i)
        com = 'time ./code < BasicDataSet/testcase8/' + str(i) + '.txt >> my.out'
        os.system(com)
    print("Diffing Output")
    os.system('diff my.out BasicDataSet/testcase8/ans.txt')

os.system('./clean.sh')

