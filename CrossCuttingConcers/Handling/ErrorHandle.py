from CrossCuttingConcers.Logging import Log

class ErrorHandle:
    @staticmethod
    def Error_Handler(func):
        def Inner_Function(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as ex:
                Log.log(Log.FATAL,f"func: {func.__name__} error:{ex}")
            else:
                Log.log(Log.WARN, f"func: {func.__name__} error:error else")
            finally:
                Log.log(Log.INFO, f"func: {func.__name__} handle complete...")

        return Inner_Function
