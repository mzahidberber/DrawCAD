from CrossCuttingConcers.Logging import  Log
from collections.abc import Iterable
class LogAspect:
    @staticmethod
    def logAspect(func):
        def Inner_Function(*args, **kwargs):
            Log.log(Log.INFO,f"Run Func: {func.__name__} Args: {args} Kwargs: {kwargs} ")
            try:
                result=func(*args, **kwargs)
                returnValue=""

                if result != None and isinstance(result,Iterable):
                    for i in result:
                        if not isinstance(i,type):
                            returnValue+=f"class: {i.__class__.__name__} | "
                            if '_id' in i.__dict__:returnValue+=f"id: {i.__dict__['_id']} | "

                elif result !=None and not isinstance(result,Iterable) and not isinstance(result, type):
                    returnValue += f"class: {result.__class__.__name__} | "
                    if '_id' in result.__dict__: returnValue += f"id: {result.__dict__['_id']} | "

                else:
                    returnValue="None"

                Log.log(Log.INFO, f"Success Func: {func.__name__} Return {returnValue}")
                return  result
            except Exception as ex:
                Log.log(Log.ERROR,f"Except Func: {func.__name__} error: {ex}")
            else:pass
                # Log.log(Log.WARN, f"func: {func.__name__} error:error else")
            finally:pass
                # Log.log(Log.INFO, f"func: {func.__name__} handle complete...")

        return Inner_Function