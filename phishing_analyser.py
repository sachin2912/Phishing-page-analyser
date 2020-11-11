from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sys, time , project

ui,_=loadUiType('gui.ui')

class MainApp(QMainWindow,ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.title = "Phishing Page Analyser"
        
        self.setupUi(self)
        self.handle_elements()

    def handle_elements(self):
        self.setWindowTitle(self.title)
        self.det_boxer.setReadOnly(True)
        self.btn_scan_one.clicked.connect(self.fetch_one)

    def fetch_one(self):
        url=self.edit_one.text()
        try:
            self.det_boxer.clear()
            start_time=time.time()
            result=project.analyse_url(url)
            end_time=time.time()
            total_time = str((end_time - start_time)/60)
            time_array=total_time.split(".")
            total_time=time_array[0]+"."+time_array[1][0:2]
            self.lab_state.setText("   URL analysed successfully!")
            content = "    Result fetched for "+url+" in "+str(total_time)+" seconds\n\n"
            for key in result.keys():
                if key == "*":
                    
                    content+= key + "     "
                    content+= result[key] 
                    content+= "\n"
                elif type(result[key]) == type([]):
                    content+="\n" + " "*20 +key + "\n"
                    for ele in result[key]:
                        content+="\n   "+ele+"\n"
                elif type(result[key]) == type(()):
                    content+="\n" + " "*20 +key +"\n"
                    for ele in result[key]:
                        content+="\n   "+ele+"\n"
                elif type(result[key]) == type(""):
                    content+="\n" + "  " +key
                    content+=" : "+result[key]

                content+= "\n\n"
            content+= "\n    Thats all for this URL , now decide yourself with the information "+str('\N{thinking face}') + "\n"
            content+= " \n\n"   
            self.det_boxer.setPlainText(content)
            self.det_boxer.setFont(QFont(".sans-serif",10))
            self.det_boxer.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        except Exception as e:
            print (e)
            
            self.det_boxer.clear()
            self.lab_state.setText("URL could not be scanned! "+ str ('\N{pensive face}'))
            errormsg = "     The URL cannot be scanned."+ str ('\N{pensive face}') +"\n"+\
                     "       Please check your internet connection and the URL for typos and try again."
            self.det_boxer.setPlainText(errormsg)

    

def main():
    app=QApplication(sys.argv)
    QFontDatabase.addApplicationFont("com-bold.ttf")
    QFontDatabase.addApplicationFont("com-lite.ttf")
    QFontDatabase.addApplicationFont("com-rlar.ttf")
    QFontDatabase.addApplicationFont("rob-bold.ttf")
    QFontDatabase.addApplicationFont("rob-lite.ttf")
    QFontDatabase.addApplicationFont("rob-rlar.ttf")
    window=MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
