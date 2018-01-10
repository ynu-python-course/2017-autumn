# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 14:47:59 2017

@author: angelshare
"""

from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication,QDesktopWidget,QLineEdit,
QMessageBox, QGridLayout, QLabel, QFrame,QMainWindow,QAction,qApp,QLineEdit,QInputDialog,QTextEdit)

from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QCoreApplication, Qt   
import sys
from numpy import *
import copy

def LUdecomp(a):
    n = len(a)
    for k in range(0,n-1):
        for i in range(k+1,n):
           if abs(a[i,k]) > 1.0e-9:
               lam = a [i,k]/a[k,k]
               a[i,k+1:n] = a[i,k+1:n] - lam*a[k,k+1:n]
               a[i,k] = lam
    return a
  
def LUsolve(a,b):
    n = len(a)
    for k in range(1,n):
        b[k] = b[k] - dot(a[k,0:k],b[0:k])
    b[n-1] = b[n-1]/a[n-1,n-1]    
    for k in range(n-2,-1,-1):
       b[k] = (b[k] - dot(a[k,k+1:n],b[k+1:n]))/a[k,k]
    return b
    
def Gausselimination(m):
    if type(m)!=list and type(m)!=tuple:
        return('valuerror')
    m=double(m)
    m=mat(m)     
    a=m.shape[0]
    b=m.shape[1]
    if linalg.det(m[:,0:a])==0:
        return('系数矩阵奇异') 
    for j in range(a-1):
        maxx=m[j,j]
        k=j
        for i in range(j,a):
            if m[i,j]>maxx:
                maxx=m[i,j]
                k=i
        p=copy.copy(m[j])
        m[j]=m[k]
        m[k]=p
        for i in range(j+1,a):
            m[i]=m[i]-m[j]*(m[i,j]/maxx)
    x=['']*a
    for i in range(a-1,-1,-1):
        if i==a-1:
            x[i]=m[a-1,a]/m[a-1,a-1]
        else:
#            x[i]=(m[i-1,a]-(lambda i:sum(x[j]*m[i,j] for j in range(i+1,a))))/m[i,i]
            x[i]=(m[i-1,a]-sum(x[j]*m[i,j] for j in range(i+1,a)))/m[i,i]
    #for i in range(a):
        print("x(%i)=%d"%(i,x[i]))                                      
    return(x)

def inverse(m):
    if type(m)!=list and type(m)!=tuple:
        return('valuerror')
    m=array(m)     
    a=m.shape[0]
    b=m.shape[1]
    if a!=b:
        return('矩阵必须为方阵')
    if linalg.det(m[:,0:a])==0:
        return('矩阵奇异')
    m=column_stack([m,eye(a)])
    for x in range(a):
        g=m[x][x]
        k=[x,x]
        for i in range(x,a):
            for j in range(x,a):
                if m[i][j]>g:
                    g=m[i,j]
                    k=[i,j]
        p=copy.copy(m[x])
        m[x]=m[k[0]]
        m[k[0]]=p
        m[:, [x, k[1]]] = m[:, [k[1], x]]#交换列
        m[x]=m[x]/g
        for y in range(a):
            if y!=x:
                m[y]=m[y]-m[x]*m[y,x]
    return(m[:,a:2*a])

def transposition(m):
    if type(m)!=list and type(m)!=tuple:
        return('valuerror')
    return(list(map(list,zip(*m))))


class wid(QMainWindow):
    
    def __init__(self):
        super(QMainWindow, self).__init__()
         
        self.initUI()
    
         
    def initUI(self):
         
        self.resize(800, 600)
        self.center()
        self.setWindowTitle('线性方程组计算器')
        self.setWindowIcon(QIcon('icon.jpg'))
        
        lbl1=QLabel('欢迎使用',self)
        lbl1.move(360,150)
        
        lbl2=QLabel('请选择方法',self)
        lbl2.move(360,200)
        
        but1 = QPushButton('高斯消元法', self)
        but1.resize(but1.sizeHint())
        but1.move(100, 360)
        but1.setObjectName("but1")
        but1.clicked.connect(self.skip2)
        
        but2 = QPushButton('三角分解法',self)
        but2.resize(but2.sizeHint())
        but2.move(360, 360)
        but2.setObjectName("but2")
        but2.clicked.connect(self.skip2)
        
        but3 = QPushButton('追赶法',self)
        but3.resize(but3.sizeHint())
        but3.move(620, 360)
        but3.setObjectName("but3")
        but3.clicked.connect(self.skip2)
        
        exit_menu = QAction(QIcon(r"1.ico"), "退出", self)
        exit_menu.setShortcut("Ctrl+Q")
        exit_menu.setStatusTip("退出程序")
        exit_menu.triggered.connect(qApp.quit)
        
        menubar = self.menuBar()
        file = menubar.addMenu("文件")
        file.addAction(exit_menu)
      

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def closeEvent(self, event):
        reply = QMessageBox.question(self,'确认退出','你确定要退出么？',
                                     QMessageBox.Yes,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
            
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
              reply = QMessageBox.question(self,'确认退出','你确定要退出么？',
                                     QMessageBox.Yes,
                                     QMessageBox.No)
              if reply == QMessageBox.Yes:
                  self.close()
              else:
                  event.ignore()
                
    def skip2(self):
        self.haoN=InputDialog()
        self.haoN.show()
    
class InputDialog(QWidget):
    def __init__(self):
        super(InputDialog, self).__init__()
        
        self.setWindowIcon(QIcon('icon.jpg'))
        self.setWindowTitle("请输入增广矩阵")
        self.resize(600, 400)
        self.center()
        self.button = QPushButton("点击此处输入", self)
        self.button.setFocusPolicy(Qt.NoFocus)
        self.button.move(20, 20)
        self.button.clicked.connect(self.show_dialog)
        self.setFocus()

        self.label = QTextEdit(self)
        self.label.move(135, 22)
    
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def show_dialog(self):
        text, ok = QInputDialog.getText(self, "输入框", "请以列表形式输入：")
        if ok:
            text=Gausselimination(eval(text))
            self.label.setText(str(text))
                 
class wid2(QMainWindow):
    
    def __init__(self):
        super(QMainWindow, self).__init__()
         
        self.initUI()
    
         
    def initUI(self):
         
        self.resize(800, 600)
        self.center()
        self.setWindowTitle('线性方程组计算器')
        self.setWindowIcon(QIcon('icon.jpg'))
        
        
        exit_menu = QAction(QIcon(r"1.ico"), "退出", self)
        exit_menu.setShortcut("Ctrl+Q")
        exit_menu.setStatusTip("退出程序")
        exit_menu.triggered.connect(qApp.quit)
        
        menubar = self.menuBar()
        file = menubar.addMenu("文件")
        file.addAction(exit_menu)
        

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def closeEvent(self, event):
        reply = QMessageBox.question(self,'确认退出','你确定要退出么？',
                                     QMessageBox.Yes,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
            
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
              reply = QMessageBox.question(self,'确认退出','你确定要退出么？',
                                     QMessageBox.Yes,
                                     QMessageBox.No)
              if reply == QMessageBox.Yes:
                  self.close()
              else:
                  event.ignore()
                  
class wid3(QMainWindow):
    
    def __init__(self):
        super(QMainWindow, self).__init__()
         
        self.initUI()
    
         
    def initUI(self):
         
        self.resize(800, 600)
        self.center()
        self.setWindowTitle('结果')
        self.setWindowIcon(QIcon('icon.jpg'))
        

        
        exit_menu = QAction(QIcon(r"1.ico"), "退出", self)
        exit_menu.setShortcut("Ctrl+Q")
        exit_menu.setStatusTip("退出程序")
        exit_menu.triggered.connect(qApp.quit)
        
        menubar = self.menuBar()
        file = menubar.addMenu("文件")
        file.addAction(exit_menu)
        

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def closeEvent(self, event):
        reply = QMessageBox.question(self,'确认退出','你确定要退出么？',
                                     QMessageBox.Yes,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
            
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
              reply = QMessageBox.question(self,'确认退出','你确定要退出么？',
                                     QMessageBox.Yes,
                                     QMessageBox.No)
              if reply == QMessageBox.Yes:
                  self.close()
              else:
                  event.ignore()
if __name__ == '__main__':
     
    app = QApplication(sys.argv)
    ex = wid()
    QToolTip.setFont(QFont('SansSerif', 10))
    ex.show()
    
    sys.exit(app.exec_())
    
    