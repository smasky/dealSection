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
    return (x,y)

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

def cal_index_left_bottom(sec_x,sec_y,width,d_height):
    '''
    计算左部分断面底部的点(x,y)，index
    return [xy=(),extend_xy=(),index]
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
    extend_xy=(xy[0]-width,xy[1])
    return ([xy,extend_xy],index)

def cal_index_right_bottom(sec_x,sec_y,width,d_height,left_len):
    '''
    计算左部分断面底部的点(x,y)，index
    return [xy=(),extend_xy=(),index]
    '''
    index=-1
    for i in range(len(sec_y)-1):
        sign=(sec_y[i]-d_height)*(sec_y[i-1]-d_height)
        if(sign<=0):
            index=i
            break
    if(index==-1):
        return []
    xy=cal_intersection([sec_x[index],sec_y[index],sec_x[index+1],sec_y[index+1]],d_height)
    extend_xy=(xy[0]-width,xy[1])
    return ([xy,extend_xy],index+left_len)

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
        return []
    xy=cal_intersection_line([sec_x[index],sec_y[index],sec_x[index-1],sec_y[index-1]],(k,b))
    return (xy,index)
def cal_right_up(sec_x,sec_y,r_b_points,left_len):
    '''
    计算右侧部分上部交点
    return:(x,y) index
    '''
    index=-1
    k=-K
    b=r_b_points[1]-k*r_b_points[0]
    for i in range(len(sec_x)):
        sign1=sec_y[i]-k*sec_x[i]-b
        sign2=sec_y[i]-k*sec_x[i]-b
        if(sign1*sign2<=0):
            index=i
            break
    if(index==-1):
        return []
    xy=cal_intersection_line([sec_x[index],sec_y[index],sec_x[index+1],sec_y[index+1],(k,b)])
    return (xy,index)
def cal_intersect_points(Mileage,xy,d_height):
    '''
    计算断面左右挖槽的高程点
    '''
    global Width
    sec_x=[]
    sec_y=[]
    for value in xy:
        sec_x.append(value[0])
        sec_y.append(value[1])

    sec_min_x=find_min_index(sec_y)
    #TODO: 左部分和右部分宽度分配的问题
    (lb_xy,lb_index)=cal_index_left_bottom(sec_x[:sec_min_x],sec_y[:sec_min_x],Width/2,d_height)
    (rb_xy,rb_index)=cal_index_right_bottom(sec_x[sec_min_x:],sec_y[sec_min_x:],Width/2,d_height,sec_min_x)
    (lu_xy,lu_index)=cal_left_up(sec_x[:lb_index+1],sec_y[:lb_index+1],lb_xy)
    (ru_xy,ru_index)=cal_right_up(sec_x[rb_index:],sec_x[rb_index:],rb_xy)
    #TODO: 计算挖掉的面积
    





