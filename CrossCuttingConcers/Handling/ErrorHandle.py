from CrossCuttingConcers.Logging import Log
from Core.UI.ErrorMessageBox import ErrorMessageBox
class ErrorHandle:
    @staticmethod
    def Error_Handler(func):
        def Inner_Function(*args, **kwargs):
            try:
                from Core.Internet.CheckInternet import CheckInternet
                if CheckInternet.isConnect:return func(*args, **kwargs)
                else:CheckInternet.checkConnectInternet()
            except Exception as ex:
                if type(func) != staticmethod:
                    Log.log(Log.FATAL,f"ERROR class: {func.__qualname__.split('.<locals>.')[0]} func: {func.__name__} error:{ex}")
                else:
                    Log.log(Log.FATAL,
                            f"ERROR class: staticmethod func: {func.__func__.__name__} error:{ex}")
            else:
                if type(func) != staticmethod:
                    Log.log(Log.WARN, f"WARNING class: {func.__qualname__.split('.<locals>.')[0]} func: {func.__name__} error:error else")
                else:
                    Log.log(Log.WARN,
                            f"WARNING class: staticmethod func: {func.__func__.__name__} error:error else")
            finally:
                if type(func) != staticmethod:
                    Log.log(Log.INFO, f"INFO class: {func.__qualname__.split('.<locals>.')[0]} func: {func.__name__} handle complete...")
                else:
                    Log.log(Log.INFO,
                            f"INFO class: staticmethod func: {func.__func__.__name__} handle complete...")

        return Inner_Function



    @staticmethod
    def Error_Handler_Cls(cls):
        for attr_name, attr_value in vars(cls).items():
            if callable(attr_value):
                setattr(cls, attr_name, ErrorHandle.Error_Handler(attr_value))
        return cls
