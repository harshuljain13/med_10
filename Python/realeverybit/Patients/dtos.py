def main():
    f = open('1.txt','r')
    f2 = open('result.txt','w+')
    l2 = list()
    for line in f:
        red_ir = line.split(' ')
        l2.append(red_ir[0])
    result_string = ' '.join(l2)
    f2.write(result_string)
    print result_string


if __name__ =='__main__':
    main()
