'''
UI
11-29
'''
import sys
import traceback
from PyQt5.QtWidgets import (QApplication,QMainWindow,QHBoxLayout,QVBoxLayout,
         QPushButton,QLabel,QLineEdit,QAction,QWidget,QFileDialog,QCheckBox,QMessageBox,QRadioButton)
from PyQt5.QtGui import QFont
from deal_Sec import *
class WCUI(QMainWindow):

    def __init__(self):
        super().__init__()
        
        self.initUI()

    def initUI(self):
        hbox=QVBoxLayout()
        centralW=QWidget()
        menubar=self.menuBar()
        fileMenu=menubar.addMenu("&File")

        self.initMenu(fileMenu)
        self.initLayout(hbox,centralW)
        self.setGeometry(300, 300, 500, 300)
        self.setWindowTitle('hydraulics cal')   
        self.show()

    def initLayout(self,allLayout,centeralW):
        first=QHBoxLayout()
        second=QHBoxLayout()
        third=QHBoxLayout()
        four=QHBoxLayout()
        tf=QHBoxLayout()
        tf2=QHBoxLayout()
        five=QHBoxLayout()
        #第一二行
        self.geo=QLabel('地形文件:',self)
        self.geoL=QLineEdit(self)
        self.geoL.setMinimumWidth(300)
        self.gs=QPushButton('选择',self)
        self.evt=QLabel('高程文件:',self)
        self.evtL=QLineEdit(self)
        self.evtL.setMinimumWidth(300)  
        self.es=QPushButton('选择',self)
        self.es.clicked.connect(self.openFile)
        self.gs.clicked.connect(self.openFile)
        self.gs.setObjectName('QPushButton1')
        self.es.setObjectName('QPushButton2')
        #复选框行
        self.re2=QLabel('计算模式:')
        self.re1=QLabel('结果输出形式:')
        self.ifmi=QCheckBox('*.txt mike')
        self.ifmi.setChecked(True)
        self.ifmi.setFont(QFont('SansSerif',10))
        self.ra1=QRadioButton('挖槽')
        self.ra1.setObjectName('wacao')
        self.ra2=QRadioButton('切边滩')
        self.ra2.setObjectName('qietan')
        #第三.5行
        self.r_name=QLabel('河道名称:')
        self.r_line=QLineEdit()
        self.r_line.setMaximumWidth(100)
        self.r_with=QLabel('疏浚宽度:')
        self.r_wline=QLineEdit()
        self.r_wline.setMaximumWidth(100)
        #输出行
        self.output=QPushButton('输出')
        self.output.clicked.connect(self.outPut)

        #copyright
        self.copy=QLabel('copyright@wmt 2018-2018 version 1.0')


        first.addStretch()
        first.addWidget(self.geo)
        first.addWidget(self.geoL)
        first.addWidget(self.gs)
        first.addStretch()
        second.addStretch()
        second.addWidget(self.evt)
        second.addWidget(self.evtL)
        second.addWidget(self.es)
        second.addStretch()
        third.addStretch(2)
        third.addWidget(self.re2)
        third.addWidget(self.ra1)
        third.addWidget(self.ra2)
        third.addStretch(10)
        third.addWidget(self.re1)
        third.addWidget(self.ifmi)
        four.addStretch(10)
        four.addWidget(self.output)
        four.addStretch(1)
        five.addStretch()
        five.addWidget(self.copy)
        five.addStretch()
        tf.addStretch(2)
        tf.addWidget(self.r_name)
        tf.addWidget(self.r_line)
        tf.addStretch(29)
        tf2.addStretch(2)
        tf2.addWidget(self.r_with)
        tf2.addWidget(self.r_wline)
        tf2.addStretch(29)

        

        allLayout.addStretch(5)
        allLayout.addLayout(first)
        allLayout.addStretch(2)
        allLayout.addLayout(second)
        allLayout.addStretch(2)
        allLayout.addLayout(tf)
        allLayout.addStretch(2)
        allLayout.addLayout(tf2)
        allLayout.addStretch(2)
        allLayout.addLayout(third)
        allLayout.addStretch(7)
        allLayout.addLayout(four)
        
        allLayout.addStretch(10)
        allLayout.addLayout(five)
        centeralW.setLayout(allLayout)
        self.setCentralWidget(centeralW)

    def outPut(self):
        '''
        连接输出
        '''
        wc=self.ra1.isChecked()
        qt=self.ra2.isChecked()
        if(wc):
            save_path=QFileDialog.getSaveFileName(self,"save file dialog","C:","Txt files(*.txt)")
            try:
                message=deal_wc_main(self.r_line.text(),self.geoL.text(),self.evtL.text(),save_path[0],self.r_wline.text())
                QMessageBox.information(self,'计算成功',message,QMessageBox.Ok)
            except BaseException as e:
                traceback.print_exc()
                print(e)
                QMessageBox.information(self,'错误','由于某些原因计算失败,请重新计算',QMessageBox.Ok)
        elif(qt):
            save_path=QFileDialog.getSaveFileName(self,"save file dialog","C:","Txt files(*.txt)")
            print(save_path[0])
            try:
                message=deal_cut_main(self.r_line.text(),self.geoL.text(),self.evtL.text(),save_path[0],self.r_wline.text())
                QMessageBox.information(self,'计算成功',message,QMessageBox.Ok)
            except BaseException as e:
                traceback.print_exc()
                print(e)
                QMessageBox.information(self,'错误','由于某些原因计算失败,请重新计算',QMessageBox.Ok)
        else:
            QMessageBox.information(self,'提示','请选择疏浚方式！',QMessageBox.Yes)

        


    def initMenu(self,submenu):
        '''
        初始化目录
        '''
        openAction=QAction('&Open',self)
        openAction.setShortcut('Ctrl+O')
        #TODO 打开文件

        exitAction=QAction('&Exit',self)
        exitAction.setShortcut('Ctrl+Q')
        #TODO 退出

        submenu.addAction(openAction)
        submenu.addAction(exitAction)

    def openFile(self):
        '''
        打开文件
        '''
        source=self.sender()
        path=QFileDialog.getOpenFileName(self,"open file dialog","C:","Txt files(*.txt)")
        if(source.objectName()=='QPushButton1'):
            self.geoL.setText(path[0])
        elif(source.objectName()=='QPushButton2'):
            self.evtL.setText(path[0])
        
        
        




if __name__=='__main__':

    app=QApplication(sys.argv)
    wc=WCUI()
    sys.exit(app.exec_())