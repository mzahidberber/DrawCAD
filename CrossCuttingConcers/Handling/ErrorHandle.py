class ErrorHandle:
    @staticmethod
    def Error_Handler(func):
        def Inner_Function(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as ex:
                print(f"func:{func.__name__} error:{ex}")
            else:
                print(f"func:{func.__name__} error:error else")
            finally:
                print(f"func:{func.__name__} handle complete...")

        return Inner_Function
