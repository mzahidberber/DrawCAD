from CrossCuttingConcers.Handling.ErrorHandle import ErrorHandle

class DrawSignal(object):
    def __init__(self,*types):
        self.listeners = []
        self.types=types
    def emit(self,*args):
        if len(args) != len(self.types):
            raise ValueError(f"Expected {len(self.types)} arguments, but received {len(args)}")

        for arg, type in zip(args, self.types):
            if not isinstance(arg, type):
                raise TypeError(f"Expected {type.__name__}, but received {type(arg).__name__}")

        for listener in self.listeners:
            listener(*args)

    def connect(self, listener):
        self.listeners.append(listener)