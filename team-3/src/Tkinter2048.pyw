# -*- coding: utf8 -*-
# 经典游戏2048来自第三组的小伙伴

# 调用本程序所需要的模块、包
from tkinter import *
import random
import tkinter.messagebox   # 用于显示应用程序的消息框

# 基本窗口建立
root = Tk(className = "2048")   # 创建一个根窗口，其余的控件都要在这个窗口上面
root.geometry("320x360")    # 改变root大小为320x360

# 相关初始化
str_data=[]
B_list = []
frame2 = Frame(root,borderwidth = 10)   # 确定框架位置，使不偏离
dic_color = {0:'GhostWhite', 2:'AliceBlue', 4:'LightCyan', 8:'Khaki',16:'SandyBrown', 32:'Goldenrod',64:'Orange',128:'Maroon',256:'Tomato',512:'OrangeRed',1024:'FireBrick',2048:'Red'} # 为各个值设置不同的颜色
list_data=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] # 定义数据列表
left=0
up=1
right=2
down=3
derection_index=[   [[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]], 
                    [[0,4,8,12],[1,5,9,13],[2,6,10,14],[3,7,11,15]],
                    [[3,2,1,0],[7,6,5,4],[11,10,9,8],[15,14,13,12]],
                    [[12,8,4,0],[13,9,5,1],[14,10,6,2],[15,11,7,3]]   ] # 方向索引，按照1--16的顺序写成矩阵来分析会很简单

# 4x4网格建立
for i in range(16):
    str_data.append(StringVar())    # StringVar()跟踪变量的值的变化，以保证值的变更随时可以显示在界面上。
    B_list.append(Button(frame2, width=4, height=2, textvariable = str_data[i]  ,font = ("Courier 20 bold roman"),bg=dic_color[0])) # Button()按钮控件,在程序中显示按钮
    B_list[i].grid(row=i//4,column=i%4)  # 行、列网格

# 判定可移动条件函数
def CanMove(derection, index):
    for i in range(1, 4):
        if list_data[derection_index[derection][index][i]] == list_data[derection_index[derection][index][i-1]]:    # 相同数字可移动
            return True
        if list_data[derection_index[derection][index][i]] != 0 and list_data[derection_index[derection][index][i-1]] == 0: # 有空位可移动
            return True
    return False

# 分配空的区域
def DealSpace(derection, index):
    for i in [3,2,1]:
        if list_data[derection_index[derection][index][i]] == 0:    # 若该位置数字为0，跳出循环
            continue
        if list_data[derection_index[derection][index][i-1]] == 0:  # 若相邻位置数字为0，移动并置原来位置为0
            j = i
            while (j < 4):
                list_data[derection_index[derection][index][j-1]] = list_data[derection_index[derection][index][j]]
                list_data[derection_index[derection][index][j]] = 0
                j=j+1

# 消除、合并数字函数
def DealEqualNum(derection, index):
    for i in [0,1,2]:
        if list_data[derection_index[derection][index][i]] == list_data[derection_index[derection][index][i+1]]:    # 一行或一列有两数字相同，则相加并合并
            list_data[derection_index[derection][index][i]] = list_data[derection_index[derection][index][i]] * 2
            list_data[derection_index[derection][index][i+1]] = 0

# 移动函数，通过调用上述两个函数实现
def Move(derection, index): 
    DealSpace(derection, index) 
    DealEqualNum(derection, index)  
    DealSpace(derection, index) 

# 刷新新界面函数
def Refresh():
    for i in range(16):
        B_list[i].configure(bg=dic_color[list_data[i]]) # 重新分配
        if list_data[i] == 0:
            str_data[i].set("")
            continue
        str_data[i].set(str(list_data[i]))

# 按键事件函数         
def key_event(event):
    canmovelist = []
    derection_code = 9
    global list_data

    if event.keycode == 37: # 键盘按键的Unicode值
        derection_code = left
    if event.keycode == 39:
        derection_code = right
    if event.keycode == 38:
        derection_code = up
    if event.keycode == 40:
        derection_code = down

    for i in range(4):
        if CanMove(derection_code, i):
            Move(derection_code, i)
            canmovelist.append(i)

    if len(canmovelist) == 0:
        return
    list_data[derection_index[derection_code][canmovelist[random.randint(0,len(canmovelist)-1)]][3]] = 2  # 得分
    Refresh()
    for i_derection in range(4):    # 判断上下左右
        for i_index in range(4):
            if CanMove(i_derection, i_index):   # 判断是否可继续移动
                return
    tkMessageBox.showinfo('Game Over','Your score is %u.\n' % sum(list_data))   # 输出游戏结束
    list_data=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] # 清除所有数字
    Refresh()   # 刷新新界面

frame2.bind('<KeyRelease>', key_event)  # 事件绑定，捕获键盘事件
frame2.pack()   # 布局管理
frame2.focus_set()  # 获取焦点，即直接对框架进行操作而不是根窗口
root.mainloop()  #让根窗口进入事件循环
