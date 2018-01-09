import easygui as g
import bookodbc as b

import pygame,sys
def create():
    ms = b.ODBC_MS('{SQL SERVER}', r'AIR\SQLEXPRESS', 'Python', 'renyijing',  'Ren20151060016')    
    Uname = g.enterbox(msg='请输入用户名：',default='')
    while 1:
        global users
        if Uname in users:
            Uname = g.enterbox(msg='此用户名已存在，请重新输入：',default='')
        else:
            break
    Upassword= g.passwordbox(msg='请输入用户密码：',default='')
    users[Uname] = Upassword
    #print(name,key)
    #注意:在进行插入操作时,自增长度不能够写入
    sql ="insert into PythonUser(UserName,UserPassword) VALUES ('%s','%s')"%(Uname,Upassword) 
    ms.ExecNoQuery(sql)          
    g.msgbox('注册成功！')
    return

def log_in():    
    
    ms = b.ODBC_MS('{SQL SERVER}', r'AIR\SQLEXPRESS', 'Python', 'renyijing',  'Ren20151060016')
    "登陆账户，需要输入账户名及密码"
    
    i=0   
    Uname = g.enterbox(msg='请输入用户名：',default='')
    while 1:
        sql = "SELECT * FROM PythonUser WHERE UserName='%s'"%(Uname)
        ret=ms.ExecQuery(sql)
        if not ret:
            Uname=g.enterbox('您输入的用户名不存在，请重新输入:',default='')
        else:
            break
    Upassword = g.passwordbox(msg='请输入用户密码：',default='')
    
    while 1:
        #for row in rett:
            #print(row)
        if ret[1]==Upassword:
            g.msgbox('欢迎进入图书馆寻书系统，请点击OK键返回主菜单')
            i=1
            search()
            break    
        elif Upassword == '':
            break
        else:
            Upassword = g.enterbox(msg='您输入用户密码不正确，请重新输入:',default='')
    return
def search():
    
    ms = b.ODBC_MS('{SQL SERVER}', r'AIR\SQLEXPRESS', 'Python', 'renyijing',  'Ren20151060016')
    
    jiansuo=g.enterbox(msg='请输入书的检索号',default='')
    
    while 1:
        
        sql = "SELECT * FROM book WHERE number='%s'"%(jiansuo)
        ret=ms.ExecQuery(sql)
        ret[3].strip()
        if not ret:
            jiansuo=g.enterbox(msg='您输入的检索号不存在，请重新输入:',default='')
        else:
            print(ret[0],ret[1],ret[2],ret[3],ret[4])
            pygame.init()
            #prepare surface
            screen = pygame.display.set_mode([640,480])
            screen.fill([255, 255, 255])
            global pos
            if ret[2]==1:
                fmg = pygame.image.load("first floor.png")
                if ret[3]=='东一':
                    if ret[4]<20:
                        pos=(466+9*(19-ret[4]),386)
                    else:
                        pos=(412+9*(44-ret[4]),327)
                elif ret[3]=='西一':
                    if ret[4]<20:
                        pos=(166-9*(19-ret[4]),386)
                    else:
                        pos=(220-9*(44-ret[4]),327)
            elif ret[2]==2:
                fmg = pygame.image.load("second floor.png")
                if ret[3]=='东一':
                    if ret[4]<20:
                        pos=(432+9*(23-ret[4]),390)
                    else:
                        pos=(351+9*(55-ret[4]),330)
                elif ret[3]=='西一':
                    if ret[4]<20:
                        pos=(201-9*(23-ret[4]),390)
                    else:
                        pos=(282-9*(55-ret[4]),330)
            elif ret[2]==3:
                fmg = pygame.image.load("third floor.png")
                if ret[3]=='东一':
                    print(ret[0],ret[1],ret[2],ret[3],ret[4])
                    if ret[4]<20:
                        pos=(432+9*(23-ret[4]),390)
                    else:
                        pos=(351+9*(55-ret[4]),330)
                elif ret[3]=='西一':
                    if ret[4]<20:
                        pos=(201-9*(23-ret[4]),390)
                    else:
                        pos=(282-9*(55-ret[4]),330)
            else:
                fmg = pygame.image.load("fourth floor.png")

            screen.blit(fmg, [0,0])
            pygame.draw.rect(screen,(255,0,0),(pos, (6, 40)))

            #flip
            pygame.display.flip()
            running=True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running=False
            pygame.quit()
            sys.exit()
            break    
    return


users ={}
i=0;

pos=(0,0)
while 1:
    command = g.buttonbox(msg='请选择',title='',choices=('新建用户','登录账号','退出程序'))
    if command == '新建用户':
        create()
    elif command == '登录账号':        

        log_in()
        #if i==1:
        #     search()        
    
    elif command == '退出程序':
        break
