



def pageshow(count,p):
    '''
        count 总页数,p  当前页
        begin 开始页 
        end 结束页
    '''
    # 开始页
    begin = p-4
    # 结束页
    end = p+5
   
    # 判断如果当前页 小于5
    if p < 5:
        # 则开始页为1
        begin = 1
        # 结束页为10
        end = 10


    # 判断如果当前页 大于 总页数-5
    if p > count-5:
        # 则开始页为总页数-9
        begin = count - 9
        # 结束页为总页数
        end = count


    # 判断如果开始页 小于等于 0,则开始页为1
    if begin <= 0:
        begin = 1

    for x in range(begin,end+1):
        print(x)



pageshow(6,5)