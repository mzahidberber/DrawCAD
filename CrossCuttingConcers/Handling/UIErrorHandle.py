from CrossCuttingConcers.Logging import Log
from Core.UI.ErrorMessageBox import ErrorMessageBox
class UIErrorHandle:
    @staticmethod
    def Error_Handler_Func(func):
        def Inner_Function(*args, **kwargs):
            try:
                from Core.Internet.CheckInternet import CheckInternet
                if CheckInternet.isConnect:
                    return func(*args, **kwargs)
                else:CheckInternet.checkConnectInternet()
            except Exception as ex:
                Log.log(Log.FATAL, f"ERROR class: {func.__qualname__.split('.<locals>.')[0]} func: {func.__name__} error:{ex}")
                ErrorMessageBox("An unexpected error has occurred, please try again.")
            else:
                Log.log(Log.WARN, f"WARNING class: {func.__qualname__.split('.<locals>.')[0]} func: {func.__name__} error:error else")
            finally:
                Log.log(Log.INFO, f"INFO class: {func.__qualname__.split('.<locals>.')[0]} func: {func.__name__} handle complete...")

        return Inner_Function

    @staticmethod
    def Error_Handler_Cls(cls):
        for attr_name, attr_value in vars(cls).items():
            if callable(attr_value):
                setattr(cls, attr_name,UIErrorHandle.Error_Handler_Func(attr_value))
        return cls