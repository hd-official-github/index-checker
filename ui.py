from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QCheckBox
from driver import Exec
class WorkerThread(QThread):
    def __init__(self, x,apikeys):
        super(WorkerThread, self).__init__()
        self.x = x
        self.apikeys = apikeys
    update_counter = pyqtSignal(int)

    def run(self):
        print("starting thread....")
        obj = Exec()
        pointer = obj.run_csv(self.x,self.apikeys)
        for val in pointer:
            print('checking index ', val+1)
            self.update_counter.emit(val)


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.headlessCheck = True
        self.endval = None
        self.thread = None
        self.worker = None
        self.fname = ""
        self.setWindowTitle("Index Checker")
        self.setFixedWidth(320)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.mylabel = QtWidgets.QLabel("Indexing Checker")
        self.mylabel.setFont(QtGui.QFont('Helvetica', 12))
        self.addW(self.mylabel)
        self.my_entry = QtWidgets.QLineEdit()
        self.my_entry.setObjectName("name_field")
        self.my_entry.setDisabled(True)
        self.my_entry.setPlaceholderText("Choose File")
        self.my_entry.setText("")
        self.addW(self.my_entry)
        self.mybtn = QtWidgets.QPushButton("Upload")
        self.mybtn.clicked.connect(self.buttonClick)
        self.addW(self.mybtn)

        self.txtarea = QtWidgets.QPlainTextEdit()
        self.txtarea.setPlaceholderText("Enter scraper api keys")
        self.addW(self.txtarea)

        self.mybtn_exec = QtWidgets.QPushButton("EXECUTE")
        self.mybtn_exec.setStyleSheet("background-color:red;color:white;padding:10px")
        self.mybtn_exec.clicked.connect(self.execute)
        self.mybtn_exec.hide()
        self.addW(self.mybtn_exec)

        self.malbel = QtWidgets.QLabel("Waiting for file...")
        self.malbel.setFont(QtGui.QFont('Helvetica', 10))
        self.malbel.setStyleSheet("color:blue;")
        self.addW(self.malbel)
        self.show()

    def addW(self, widget):
        self.layout().addWidget(widget)

    def getfile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            'c:\\', "CSV files (*.csv *.xls)")
        self.fname = f"{fname[0]}"
        return fname[0]

    def reportProgress(self, n):
        self.malbel.setText(f"CHECKING INDEX OF : {str(n+1)} OF  {str(self.endval)}")

    def execute(self):
        self.v = self.txtarea.toPlainText().splitlines() 
        self.mybtn_exec.setText("Executing....")
        self.mybtn_exec.setDisabled(True)
        self.endval = Exec.read_csv_len(self.fname)
        self.worker = WorkerThread(f"{self.fname}",self.v)
        self.worker.start()
        self.worker.update_counter.connect(self.reportProgress)
        self.worker.finished.connect(self.evt_worker_finished)

    def evt_worker_finished(self):
        self.malbel.setFont(QtGui.QFont('Helvetica', 10))
        self.malbel.setStyleSheet("color:green;")
        self.malbel.setText("CHECKING INDEX FINISHED.THANKS !!!")
        self.mybtn_exec.hide()
        self.mylabel.hide()
        print("Worker thread completed")

    def buttonClick(self):
        fstr = self.getfile()
        self.my_entry.setPlaceholderText(f'{fstr}')
        self.mybtn.hide()
        self.mybtn_exec.show()
        self.malbel.setText("READY TO EXECUTE....")

    def incre_status(self, val, endval):
        self.malbel.setText(f"{val}" + " of " + f"{endval}" + " done")