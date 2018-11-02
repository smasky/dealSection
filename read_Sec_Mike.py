'''
从Mike中读取断面信息
形成一个dict： key：断面里程 value:(x,y)元组的list
Author:smasky
'''
import os 
from global_variable import *
def read_section_mike(path='',name=''):
    """
        name: 河道名称
        path: 文件的地址
        从Mike读取断面信息
    """
    global Section
    isPoint=False
    isMileage=False
    Sec_name=''
    if(path==''):
        print('文件地址为空')
        return 0
    file=open(path,'r')
    for line in file:
        if("LEVEL PARAMS" in line):
            isPoint=False
        
        if(isMileage):
            Sec_name=str(line).strip('\n').replace(' ','')
            Section[Sec_name]=[]
            isMileage=False
        if(name in line):
            isMileage=True

        if(isPoint):
            string=str(line).strip('\n').lstrip().split('    ')
            xy=(string[0],string[1])
            Section[Sec_name].append(xy)
            #print(string)

        if("PROFILE" in line):
            isPoint=True
        
        
            
#测试
def main():
    read_section_mike("E://aaaa.txt","HUAIHEZHUGAN1")

if __name__ == '__main__':
    main()
