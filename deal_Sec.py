'''
给定底高程和底宽的挖槽程序
input: wacao.txt   13670 5
                   14680 5.1
output：可选Mike格式Section
1.找最小值
2.沿最小值两边找疏浚高程
3.边坡1:4 求交点
a.插值函数
Author:smasky
'''
from read_Sec_Mike import read_section_mike
from global_variable import *
from write_Sec_Mike import write_mike
def read_height():
    '''
    本地文件夹：height.txt 格式： 里程 高程
    '''
    file=open("height.txt",'r')
    for line in file:
        string=line.strip('\n').split(' ')
        Height[("%.3f"%float(string[0]))]=float(string[1])
    file.close()
def find_min_index(x):
    '''
    计算最小值的Index
    return: index
    '''
    return x.index(min(x))

def cal_intersection_line(point_xy,kb):
    '''
    计算两个点加已知直线 求交点
    return:(x,y)
    '''
    if(point_xy[1]==point_xy[3]):
        x=(point_xy[3]-kb[1])/kb[0]
        return (x,point_xy[1])
    k1=(point_xy[1]-point_xy[3])/(point_xy[0]-point_xy[2])
    b1=point_xy[3]-point_xy[2]*k1
    x=(kb[1]-b1)/(k1-kb[0])
    y=k1*x+b1
    return (round(x,1),round(y,1))

def cal_intersection(point_xy,d_height):
    '''
    往两个点之间 插值一个高d_height的点
    '''
    if(point_xy[0]==point_xy[2]):
        return (point_xy[0],d_height)
    k=(point_xy[1]-point_xy[3])/(point_xy[0]-point_xy[2])
    b=point_xy[3]-k*point_xy[2]
    x=(d_height-b)/k
    return (x,d_height)

def cal_index_left_bottom(sec_x,sec_y,d_height):
    '''
    计算左部分断面底部的点(x,y)，index
    return [xy=(),index]
    '''
    index=-1
    for i in range(len(sec_y)-1,0,-1):
        sign=(sec_y[i]-d_height)*(sec_y[i-1]-d_height)
        if(sign<=0):
            index=i
            break
    if(index==-1):
        return [ ]
    xy=cal_intersection([sec_x[index],sec_y[index],sec_x[index-1],sec_y[index-1]],d_height)
    return (xy,index)

def cal_index_right_bottom(sec_x,sec_y,d_height,left_len):
    '''
    计算左部分断面底部的点(x,y)，index
    return [xy=(),index]
    '''
    index=-1
    for i in range(len(sec_y)-1):
        sign=(sec_y[i]-d_height)*(sec_y[i+1]-d_height)
        if(sign<=0):
            index=i
            break
    if(index==-1):
        return []
    #print('111')
    xy=cal_intersection([sec_x[index],sec_y[index],sec_x[index+1],sec_y[index+1]],d_height)
    index=index+left_len
    return (xy,index)

def cal_left_up(sec_x,sec_y,l_b_points):
    '''
    计算左侧部分上部交点
    return:(x,y) index
    '''
    index=-1
    k=-K
    b=l_b_points[1]-l_b_points[0]*k
    for i in range(len(sec_y)-1,0,-1):
        sign1=sec_y[i]-k*sec_x[i]-b
        sign2=sec_y[i-1]-k*sec_x[i-1]-b
        if(sign1*sign2<=0):
            index=i
            break
    if(index==-1):
        x=(sec_y[-1]-b)/k
        return ((x,sec_y[-1]),len(sec_x))
    xy=cal_intersection_line([sec_x[index],sec_y[index],sec_x[index-1],sec_y[index-1]],(k,b))
    return (xy,index)
def cal_right_up(sec_x,sec_y,r_b_points,left_len):
    '''
    计算右侧部分上部交点
    return:(x,y) index
    '''
    index=-1
    k=K
    b=r_b_points[1]-k*r_b_points[0]
    for i in range(len(sec_x)-1):
        sign1=sec_y[i]-k*sec_x[i]-b
        sign2=sec_y[i+1]-k*sec_x[i+1]-b
        if(sign1*sign2<=0):
            index=i
            break
    if(index==-1):
        x=(sec_y[-1]-b)/k
        return ((x,sec_y[-1]),len(sec_x)+left_len)
    xy=cal_intersection_line([sec_x[index],sec_y[index],sec_x[index+1],sec_y[index+1]],(k,b))
    return (xy,index+left_len)
def lr_width_distr(l_xy,r_xy,sec_x,width):
    '''
    return: (左边宽度,右边宽度)
    '''
    left=l_xy[0]-sec_x[0]
    right=sec_x[-1]-r_xy[0]
    c_width=width-(r_xy[0]-l_xy[0])
    if(c_width<=0):
        return []
    w_left=c_width*left/(left+right)
    w_right=c_width*right/(left+right)

    return (w_left,w_right)
def cal_right_area(r_xy,rb_xy,ru_xy,sec_x,sec_y):
    '''
    计算需要开挖的面积
    return: area
    '''
    num=len(sec_x)+1
    area=0
    k=K
    b=rb_xy[1]-k*rb_xy[0]
    sec_x.append(ru_xy[0])
    sec_y.append(ru_xy[1])
    for i in range(num-1):
        if(sec_x[i+1]<=rb_xy[0]):
            area+=(sec_x[i+1]-sec_x[i])*(sec_y[i]-rb_xy[1]+sec_y[i+1]-rb_xy[1])/2
        else:
            area+=(sec_x[i+1]-sec_x[i])*(sec_y[i+1]-k*sec_x[i+1]-b+sec_y[i]-k*sec_x[i]-b)/2
    return area
def cal_left_area(l_xy,lb_xy,lu_xy,sec_x,sec_y):
    num=len(sec_x)+1
    area=0
    k=-K
    b=lb_xy[1]-k*lb_xy[0]
    sec_x.append(lu_xy[0])
    sec_y.append(lu_xy[1])
    for i in range(num-1):
        if(sec_x[i+1]>=lb_xy[0]):
            area+=(sec_x[i+1]-sec_x[i])*(sec_y[i+1]-k*sec_x[i+1]-b+sec_y[i]-k*sec_x[i]-b)/2
        else:
            area+=(sec_x[i+1]-sec_x[i])*(sec_y[i]+sec_y[i+1]-2*lb_xy[1])/2
    return area
def cal_intersect_points(Mileage,xy,d_height,width):
    '''
    计算断面左右挖槽的高程点
    '''
    global G_num
    sec_x=[]
    sec_y=[]
    for value in xy:
        sec_x.append(value[0])
        sec_y.append(value[1])
    sec_min_x=find_min_index(sec_y)
    if(sec_y[sec_min_x]>d_height):
        G_num+=1
        print('高程不符合')
        return []
    (l_xy,lb_index)=cal_index_left_bottom(sec_x[:sec_min_x+1],sec_y[:sec_min_x+1],d_height)
    (r_xy,rb_index)=cal_index_right_bottom(sec_x[sec_min_x-1:],sec_y[sec_min_x-1:],d_height,sec_min_x)
    c_width=lr_width_distr(l_xy,r_xy,sec_x,width) #合理分配 左右宽度
    if(len(c_width)==0):
        return []
    lb_xy=(l_xy[0]-c_width[0],l_xy[1])
    rb_xy=(r_xy[0]+c_width[1],r_xy[1])
    (lu_xy,lu_index)=cal_left_up(sec_x[:lb_index+1],sec_y[:lb_index+1],lb_xy)
    (ru_xy,ru_index)=cal_right_up(sec_x[rb_index-1:],sec_y[rb_index-1:],rb_xy,rb_index)
    #TODO: 计算挖掉的面积
    area=cal_left_area(l_xy,lb_xy,lu_xy,sec_x[lu_index:lb_index],sec_y[lu_index:lb_index])
    area+=cal_right_area(r_xy,rb_xy,ru_xy,sec_x[rb_index:ru_index],sec_y[rb_index:ru_index])
    print(area)
    sec_x[rb_index-1:ru_index+1]=[r_xy[0],rb_xy[0],ru_xy[0]]
    sec_x[lu_index:lb_index]=[lu_xy[0],lb_xy[0],l_xy[0]]
    sec_y[rb_index-1:ru_index+1]=[r_xy[1],rb_xy[1],ru_xy[1]]
    sec_y[lu_index:lb_index]=[lu_xy[1],lb_xy[1],l_xy[1]]
    xy=[]
    for x,y in zip(sec_x,sec_y):
        xy.append((round(x,1),round(y,1)))
    return xy

def cut_beach(Mileage,xy,d_height,width):
    '''
    切边滩
    计算断面左右挖槽的高程点
    '''
    global G_num
    sec_x=[]
    sec_y=[]
    for value in xy:
        sec_x.append(value[0])
        sec_y.append(value[1])
    sec_min_x=find_min_index(sec_y)
    #TODO: 左部分和右部分宽度分配的问题
    if(sec_y[sec_min_x]>d_height):
        G_num+=1
        print('高程不符合')
        return []
    (l_xy,lb_index)=cal_index_left_bottom(sec_x[:sec_min_x+1],sec_y[:sec_min_x+1],d_height)
    (r_xy,rb_index)=cal_index_right_bottom(sec_x[sec_min_x-1:],sec_y[sec_min_x-1:],d_height,sec_min_x)
    lb_xy=(l_xy[0]-width/2,l_xy[1])
    rb_xy=(r_xy[0]+width/2,r_xy[1])
    (lu_xy,lu_index)=cal_left_up(sec_x[:lb_index+1],sec_y[:lb_index+1],lb_xy)
    (ru_xy,ru_index)=cal_right_up(sec_x[rb_index-1:],sec_y[rb_index-1:],rb_xy,rb_index)
    #TODO: 计算挖掉的面积
    sec_x[rb_index:ru_index+1]=[r_xy[0],rb_xy[0],ru_xy[0]]
    sec_x[lu_index:lb_index]=[lu_xy[0],lb_xy[0],l_xy[0]]
    sec_y[rb_index:ru_index+1]=[r_xy[1],rb_xy[1],ru_xy[1]]
    sec_y[lu_index:lb_index]=[lu_xy[1],lb_xy[1],l_xy[1]]
    xy=[]
    for x,y in zip(sec_x,sec_y):
        xy.append((round(x,1),round(y,1)))
    return xy
def cal_all():
    global Num
    for key,xy in Section.items():
        n_xy=cal_intersect_points(key,xy,Height[key],Width)
        if(len(n_xy)==0):
            New_Section[key]=Section[key]
        else:
            New_Section[key]=n_xy
            Num+=1
            print(key)
    print('一共{}个断面,挖了{}个断面,高程不够{}个断面'.format(len(Section),Num,G_num))
def main():
    read_section_mike("hh.txt","HUAIHEZHUGAN1")
    read_height()
    cal_all()
    write_mike(New_Section,"nhh")

if __name__=="__main__":
    main()
