from PyQt5.QtCore import QObject,Qt, QPointF
from PyQt5.QtWidgets import QListWidget,QLineEdit,QCompleter
from PyQt5.QtGui import QRegExpValidator
from PyQt5.Qt import QRegExp
from Commands.CommandLine import CommandLine
from Commands.CommandEnums import CommandEnums
from Core.Signal import DrawSignal
class CommandLineUI(QObject):
    commandSignal= DrawSignal(CommandEnums)
    coordinateSignal = DrawSignal(object)
    distanceSignal= DrawSignal(object)
    escapeSignal= DrawSignal()
    deleteSignal= DrawSignal()
    deleteSpaceEnterSignal= DrawSignal()

    __commandLine:CommandLine=None
    __lastCommand:CommandEnums

    @property
    def commandLine(self)->CommandLine:return self.__commandLine
    @commandLine.setter
    def commandLine(self,commandLine:CommandLine):
        self.__commandLine=commandLine
        if commandLine is not None:
            self.__commandLine.updateSignal.connect(self.refreshList)
            self.refreshList()
        else:
            self.__listWidget.clear()



    def __init__(self,listWidget:QListWidget,lineEdit:QLineEdit):
        super().__init__()
        self.__listWidget=listWidget
        self.__lineEdit=lineEdit



        self.__lineEdit.setValidator(QRegExpValidator(QRegExp("^[A-Za-z0-9.,-]+$")))
        commands=list(map(lambda x:x.name,CommandEnums))
        commands.insert(0,"")
        self.completer = QCompleter(commands)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setCompletionMode(QCompleter.InlineCompletion)
        self.__lineEdit.setCompleter(self.completer)

        self.__lineEdit.keyPressEvent=self.lineEditKeyPress

        self.__lastCommand=CommandEnums.Line

    def lineEditKeyPress(self,ev):
        QLineEdit.keyPressEvent(self.__lineEdit, ev)
        if ev.key() == Qt.Key_Space or ev.key() == Qt.Key_Return or ev.key() == Qt.Key_Enter:
            self.deleteSpaceEnterSignal.emit()
            self.__lineEdit.selectAll()
            try:
                distance = float(self.__lineEdit.selectedText())
            except Exception as ex:
                try:
                    coordinate = self.__lineEdit.selectedText().split(",")
                    coordinateX,coordinateY=float(coordinate[0]),float(coordinate[1])
                except Exception as ex:
                    if self.__lineEdit.selectedText()=="":
                        self.commandSignal.emit(self.__lastCommand)
                        return
                    for i in CommandEnums:
                        if i.name.lower()==self.__lineEdit.selectedText().lower():
                            self.commandSignal.emit(i)
                            self.__lastCommand=i
                            break
                else:
                    self.coordinateSignal.emit(QPointF(coordinateX, coordinateY))
            else:
                self.distanceSignal.emit(distance)

            finally:
                self.__lineEdit.clear()

        elif ev.key()==Qt.Key_Escape:self.escapeSignal.emit()
        elif ev.key()==Qt.Key_Delete:self.deleteSignal.emit()


    def refreshList(self):
        self.__listWidget.clear()
        if self.__commandLine is not None:[self.__listWidget.addItem(i.message) for i in self.__commandLine.commandList]
        self.__listWidget.scrollToBottom()

