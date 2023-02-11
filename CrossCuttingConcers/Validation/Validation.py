
class Validation:

    @staticmethod
    def validationNone(func):
        "Validation Value and Value Isn't None Return Function or Return None"
        def __inner(cls,value:list or None):
            if(value!=None):
                return func(cls,value)
            else:
                return None
        return __inner