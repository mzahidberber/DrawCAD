from PyQt5.QtCore import QObject, pyqtSignal, QPointF
from Commands.Command import Command
from Commands.CommandEnums import CommandEnums
from Model import Layer, Element
from Helpers.Settings import Setting
from datetime import datetime


class CommandLine(QObject):
    updateSignal = pyqtSignal()

    __commandList: list[Command]
    __selectedCommand: CommandEnums

    @property
    def commandList(self) -> list[Command]:
        return self.__commandList

    def __init__(self):
        super().__init__()
        self.__commandList = []

    def __addCommand(self, command: Command):
        self.__commandList.append(command)
        self.updateSignal.emit()

    def __removeCommand(self, command: Command):
        self.__commandList.remove(command)
        self.updateSignal.emit()

    def startCommand(self, command: CommandEnums):
        if command.value == 3:
            self.__addCommand(Command(f"Command : {command.name} Radius : {Setting.radius}"))
        else:
            self.__addCommand(Command(f"Command : {command.name}"))
        self.__selectedCommand = command

    def stopCommand(self):
        self.__addCommand(Command(f"Stop Command"))

    def addPoint(self, point: QPointF):
        self.__addCommand(
            Command(f"Command {self.__selectedCommand.name} x : {round(point.x(), 4)} y : {round(point.y(), 4)}"))

    def changeLayer(self, layer: Layer):
        self.__addCommand(Command(f"Selected Layer : {layer.name}"))

    def setRadius(self, radius: float):
        self.__addCommand(Command(f"Radius : {radius}"))

    def addCustomCommand(self, log: str):
        self.__addCommand(Command(log))
