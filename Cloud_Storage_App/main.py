from QT_Login import Ui_Dialog
from PyQt5.Qt import QMainWindow, QWidget, QLabel, Qt, QApplication, QFileDialog
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
import wget
import sys
import requests
import sqlite3
import webbrowser
from sys import argv, executable
import os

# server domen
DOMEN = "http://127.0.0.1:8000"
# create database
db = sqlite3.connect('base.db')
sql = db.cursor()
# create table in database
def create_table(Username, Password):
    db = sqlite3.connect('base.db')
    sql = db.cursor()
    # Creating a table
    sql.execute(""" CREATE TABLE IF NOT EXISTS data (username TEXT, password TEXT) """)
    # Adding data
    sql.execute("INSERT OR IGNORE INTO data VALUES (?, ?)", (Username, Password))
    # The confirmation
    db.commit() 
# delete table in database
def delete_table():
    db = sqlite3.connect('base.db')
    sql = db.cursor()
    # Удаляем 
    sql.execute('DELETE FROM data')
    db.commit()  
    sql.close() 
    db.close()
# get username and password from local database
def get_data():
    try:
        for i in sql.execute("SELECT * FROM data"):
            return i[0], i[1]
    except:
        return 'NONE', 'NONE'
# check username and pass
def valid(Username, Password):
    status = requests.post(DOMEN + "/api/user/login/", json={'username': Username, 'password': Password}).json()['status']
    return status
# login page
class LoginPage(QtWidgets.QMainWindow):
    def __init__(self):
        super(LoginPage, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle('Cloud - login page')
        self.setWindowIcon(QIcon('cloud.png'))
        # клик по кнопке Login
        self.ui.LoginButton.clicked.connect(self.Login)
        # клик по кнопке Registration
        self.ui.Registr.clicked.connect(self.Registration)
        
    # redirect on reg. page
    def Registration(self):
        webbrowser.open(DOMEN + '/registration/')

    # login func
    def Login(self):
        # get username and password
        Username = self.ui.Username.text()
        Password = self.ui.Password.text()
        # Проверяем логин и пароль на валидность
        status = valid(Username, Password)
        # if data is valid
        if status == "OK":
            self.ui.Message.setStyleSheet("background:#fff;color:#fff;")
            # create table 
            create_table(Username, Password)
            # close login page
            self.close()
            # open main page 
            os.execl(executable, os.path.abspath(__file__), *argv)
        # if not valid
        else:
            # send message
            self.ui.Message.setStyleSheet("background:#222;color:#fff;")
            self.ui.label.setText("Invalid Username or Password")
# main page
class MainPage(QtWidgets.QWidget):
    
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1280, 700)
        Dialog.setStyleSheet("border-radius: 10px; background-color: #fff; font-size: 16px;")
        self.UploadButton = QtWidgets.QPushButton(Dialog)
        self.UploadButton.setGeometry(QtCore.QRect(20, 20, 121, 41))
        self.UploadButton.setStyleSheet("border: 2px solid")
        self.UploadButton.setObjectName("UploadButton")
        self.UploadButton.clicked.connect(self.Upload)
   
        self.LogoutButton = QtWidgets.QPushButton(Dialog)
        self.LogoutButton.setGeometry(QtCore.QRect(160, 20, 81, 41))
        self.LogoutButton.setStyleSheet("border: 2px solid")
        self.LogoutButton.setObjectName("LogoutButton")
        self.LogoutButton.clicked.connect(self.Logout)
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle('Cloud - main page')
        Dialog.setWindowIcon(QIcon('cloud.png'))
        self.UploadButton.setText(_translate("Dialog", "upload file"))
        self.LogoutButton.setText(_translate("Dialog", "logout"))

        # get files
        Username, Password = get_data()
        data = requests.post(DOMEN + "/api/user/files/", json={'username': Username, 'password': Password}).json()
        if data['status'] == "OK":
            n = 20
            z = 80
            m = 0
            for i in data['data']:
                groupBox = "groupBox_"+str(i)
                DowloadBTN = "DowloadBTN_"+str(i)
                DeleteBTN = "DeleteBTN_"+str(i)
                label = "label_"+str(i)
                self.groupBox = QtWidgets.QGroupBox(Dialog)
                self.groupBox.setGeometry(QtCore.QRect(n, z, 191, 291))
                self.groupBox.setStyleSheet("font-size: 15px; border: 2px solid")
                self.groupBox.setObjectName(groupBox)
                self.label = QtWidgets.QLabel(self.groupBox)
                self.label.setGeometry(QtCore.QRect(10, 20, 171, 221))
                self.label.setStyleSheet("border:none;")
                self.label.setText("")
                self.label.setPixmap(QtGui.QPixmap("../Cloud_Storage_App/Files IMG/"+data['data'][i]['image']))
                self.label.setScaledContents(True)
                self.label.setObjectName(label)
                self.DowloadBTN = QtWidgets.QPushButton(self.groupBox)
                self.DowloadBTN.setGeometry(QtCore.QRect(10, 250, 111, 31))
                self.DowloadBTN.setObjectName(DowloadBTN)
                self.DowloadBTN.clicked.connect(lambda ch, id=data['data'][i]['id']: self.Download(id)) 
                self.DeleteBTN = QtWidgets.QPushButton(self.groupBox)
                self.DeleteBTN.setGeometry(QtCore.QRect(124, 250, 61, 31))
                self.DeleteBTN.setObjectName(DeleteBTN)

                self.DeleteBTN.clicked.connect(lambda ch, id=data['data'][i]['id']: self.Delete(id)) 
                
                _translate = QtCore.QCoreApplication.translate
                self.groupBox.setTitle(_translate("Dialog", i))
                self.DowloadBTN.setText(_translate("Dialog", "download"))
                self.DeleteBTN.setText(_translate("Dialog", "delete"))
                
                n += 210
                if n == 1280:
                    n = 20
                    z += 310
    
    # dowload file
    def Download(self, id):   
        try:                                 
            path = QFileDialog.getExistingDirectory(self,"Choose dir")
            path = str(path) + '/' + requests.post(DOMEN + '/api/file/' + str(id) + '/').json()['data']['file']
            url = DOMEN+"/api/file/download/"+str(id)+"/"
            
            print(path)
            filename = wget.download(url, path)
            print(filename)
        except:
            pass

    # delete file
    def Delete(self, id): 
        Username, Password = get_data()
        status = requests.post(DOMEN + "/api/file/delete/", json={'username': Username, 'password': Password, "id": id}).json()['status']
        if status == "OK":
            os.execl(executable, os.path.abspath(__file__), *argv)
        else:
            return "ERR"
    # upload file
    def Upload(self):
        try:
            file = QtWidgets.QFileDialog.getOpenFileName(self)
            Username, Password = get_data()
            files = {"file": open(file[0], "rb")}
            r = requests.post(DOMEN+"/api/file/upload/", files=files, data={"Content-Type": "application/json", 'username': Username, 'password': Password})
            # restart programm
            os.execl(executable, os.path.abspath(__file__), *argv)
        except:
            pass
    # user logout
    def Logout(self):
        try:
            delete_table()
        except:
            pass
        os.execl(executable, os.path.abspath(__file__), *argv)
# check on valid 
try:
    Username, Password = get_data()
except:
    Username, Password = "NONE", "NONE"

if valid(Username, Password) == "OK":
    # open page
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = MainPage()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
else:
    # if not valid - delete table in database
    try:
        delete_table()
    except:
        pass
    #open page
    app = QtWidgets.QApplication([])
    application = LoginPage()
    application.show()
    sys.exit(app.exec())
