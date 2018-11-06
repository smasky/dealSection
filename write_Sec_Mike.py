'''
将断面写入成Mike的格式
method:write_mike write_mike_top write_middle
'''
import os
def write_mike(sec,filename):
    file=open("{}.txt".format(filename),'w')
    for key,values in sec.items():
        write_mike_top(key,key,file)
        file.write("PROFILE        {}\n".format(len(values)))
        write_middle(values,file)
        file.write("LEVEL PARAMS\n")
        file.write("   0  0    0.000  0    0.000  50\n")
        file.write("**************************\n")

def write_mike_top(Mileage,ID,file):
    file.write('2013\n')
    file.write('HUAIHEZHUGAN\n')
    file.write("{}\n".format(Mileage))
    file.write("COORDINATES\n")
    file.write("0\n")
    file.write("FLOW DIRECTION\n")
    file.write("0\n")
    file.write("PROTECT DATA\n")
    file.write("0\n")
    file.write("DATUM\n")
    file.write("0.00\n")
    file.write("RADIUS TYPE\n")
    file.write("0\n")
    file.write("DIVIDE X-Section\n")
    file.write("0\n")
    file.write("SECTION ID\n")
    file.write("{}\n".format(ID))
    file.write("INTERPOLATED\n")
    file.write("0\n")
    file.write("ANGLE\n")
    file.write("0.00    0\n")
    file.write("RESISTANCE NUMBERS\n")
    file.write("   1  0     1.000     1.000     1.000    1.000    1.000\n")

def write_middle(xy,file):
    x=[]
    y=[]
    for value in xy:
        x.append(value[0])
        y.append(value[1])
    min_y=y.index(min(y))
    yy=y[min_y:]
    left_max=y.index(max(y[:y.index(min(y))]))
    right_max=yy.index(max(y[y.index(min(y)):]))+min_y
    for i in range(len(x)):
        string="{}    {}    1.000    <#{}>    0    0.000    0\n"
        if(i==min_y):
            file.write(string.format(x[i],y[i],2))
        elif(i==left_max):
            file.write(string.format(x[i],y[i],1))
        elif(i==right_max):
            file.write(string.format(x[i],y[i],4))
        else:
            file.write(string.format(x[i],y[i],0))
