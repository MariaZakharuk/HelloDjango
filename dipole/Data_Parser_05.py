import os, sys, json
import pandas as pd
import linecache
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
       
        self.setGeometry(300, 300, 246, 72)
        self.setWindowTitle('Data Parser mk_II')
        
        self.extFrame = QFrame(self)
        self.extFrame.setGeometry(1,1,110,70)
        self.extFrame.setFrameShape(QFrame.StyledPanel)

        self.prsFrame = QFrame(self)
        self.prsFrame.setGeometry(115,1,130,70)
        self.prsFrame.setFrameShape(QFrame.StyledPanel)
        
        self.fromLbl = QLabel('From', self.extFrame)
        self.fromLbl.move(7,4)

        self.toLbl = QLabel('To', self.extFrame)
        self.toLbl.move(57,4)
        
        self.combo1 = QComboBox(self.extFrame)
        self.combo1.addItems([".min", ".json", ".txt"])
        self.combo1.move(5, 22)

        self.combo2 = QComboBox(self.extFrame)
        self.combo2.addItems([".min", ".json", ".txt"])
        self.combo2.move(55, 22)

        self.extBtn = QPushButton('Change extension', self.extFrame)
        self.extBtn.setToolTip('Change extension of files in selected folder')
        self.extBtn.move(7,43)
        
        self.parseToJsonBtn = QPushButton('Parse to JSON format', self.prsFrame)
        self.parseToJsonBtn.setToolTip('Parse Raw Data files to JSON format')
        self.parseToJsonBtn.move(7,25)
        
        self.extBtn.clicked.connect(self.Rename)
        self.parseToJsonBtn.clicked.connect(self.parseToJson)

        self.show()


    def Rename(self):

        folder = QFileDialog.getExistingDirectory(self, 'Select folder')
        
        for filename in os.listdir(folder):
            infilename = os.path.join(folder,filename)
            if not os.path.isfile(infilename): continue
            oldbase = os.path.splitext(filename)
            newname = infilename.replace(self.combo1.currentText(),self.combo2.currentText())
            output = os.rename(infilename, newname)
        QMessageBox.question(self, 'Done', "Data extension successfully changed", QMessageBox.Ok)


    def parseToJson (self):
        
        folder = QFileDialog.getExistingDirectory(self, 'Select folder')

        #bigDF = pd.DataFrame(columns = ['0', '1', '2', '3', '4', '5', '6'])
        bigDF = pd.DataFrame()
        recordsCount = 0
        #print(bigDF)
        
        for filename in os.listdir(folder):
            infilename = os.path.join(folder,filename)
            if not os.path.isfile(infilename): continue

            
        
            s = ''  #Создаем пустую строку, чтобы потом записать в нее текст из файла
            #print(infilename)
            #print(folder)
            f = open(infilename)
            flines = f.readlines()
            f.close()

            x = 0
            

           # print(len(flines))
            
            while (x != len(flines)):
                if ('c/s' in flines[x]):
                    #print(flines[x])
                    break
                x += 1
            #print(x)
            #print(flines[x])
                
            #for x in range(0, len(flines)):  #Считываем строки с 26 по 1466...
            #    if (flines[x] == 'DATE       TIME         DOY     EYRX      EYRY      EYRZ      EYRG   |'):
                    
            #        break
            #print('x =',x)
            for j in range (x+1, len(flines)):
                s = s + flines[j] #...и собираем их в одну строку 

            space = ' '  #Строка, состоящая из одного пробела. Она пригодится нам дальше
        
            s = s.replace('|', ' ')  #Чистим строку от всего лишнего
            s = s.replace('\n', ' ') #Чистим строку от всего лишнего
            #s = s.replace('99999.00', 'NaN') 

            for x in range (6, 1, -1):
                s = s.replace(space*x, space)  #Чистим строку от всего лишнего

            data = s.split(sep=' ') #Создаем из строки массив, разделив ее по пробелам
            data.remove('')
            
            JSData = {}  #Создаем пустой словарь...
            i = 0  #...и счетчик

           # print(recordsCount)
            
            for x in range(0, 100, 25):  #Проходим по всем элементам массива с шагом в 7...
                JSData.update({i + recordsCount:data[x:x+25]}) #...и формируем из них словарь...
                i += 1  #...не забывая увеличивать счетчик
           
            df = pd.DataFrame(JSData) #Конвертируем словарь в DataFrame...
            df = df.transpose()
            #infilename.replace('\\', '/')            
            #print(df)

            bigDF = bigDF.append(df)
            #print(bigDF)

            recordsCount += 3
            
            #df.to_json(infilename)

        # bigDF = bigDF.transpose()
        filename = os.path.split(folder)[1]
        bigDF.to_json(filename+'.json')            

        QMessageBox.question(self, 'Done', "Data format successfully changed", QMessageBox.Ok)
        print ("Успех!")

            
if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
