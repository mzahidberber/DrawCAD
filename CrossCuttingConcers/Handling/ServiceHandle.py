from CrossCuttingConcers.Logging import Log
from collections.abc import Iterable
from Core.Internet import CheckInternet


class ServiceHandle:
    @staticmethod
    def serviceHandle_func(func):
        def Inner_Function(*args, **kwargs):
            # Log.log(Log.INFO,
            #         f"INFO Run Class: {func.__qualname__.split('.<locals>.')[0]} Func: {func.__name__} Args: {args} Kwargs: {kwargs} ")
            try:

                result = func(*args, **kwargs)
                returnValue = ""
                if result != None and isinstance(result, Iterable):
                    for i in result:
                        if not isinstance(i, type) and type(i)!=str:
                            returnValue += f"class: {i.__class__.__name__} | "
                            if '_id' in i.__dict__: returnValue += f"id: {i.__dict__['_id']} | "
                elif result != None and not isinstance(result, Iterable) and not isinstance(result, type):
                    returnValue += f"class: {result.__class__.__name__} | "
                    if '_id' in result.__dict__: returnValue += f"id: {result.__dict__['_id']} | "
                else:
                    returnValue = "None"
                Log.log(Log.INFO,
                        f"INFO Class: {func.__qualname__.split('.<locals>.')[0]} Func: {func.__name__} Return {returnValue}")
                return result

            except Exception as ex:
                Log.log(Log.ERROR,
                        f"ERROR Class: {func.__qualname__.split('.<locals>.')[0]} Func: {func.__name__} error: {ex.message}")
            else:pass
                # Log.log(Log.ERROR,
                #         f"ERROR Class: {func.__qualname__.split('.<locals>.')[0]} Func: {func.__name__} error: You do not have an internet connection")
            finally:
                Log.log(Log.INFO,
                        f"INFO Class: {func.__qualname__.split('.<locals>.')[0]} Func: {func.__name__} handle complete...")

        return Inner_Function

    @staticmethod
    def serviceHandle_cls(cls):
        for attr_name, attr_value in vars(cls).items():
            if callable(attr_value):
                setattr(cls, attr_name, ServiceHandle.serviceHandle_func(attr_value))
        return cls
