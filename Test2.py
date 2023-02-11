
def validation(func):
    def inner(value):
        if value!=None:
            return func(value)
        else:
            return print("NOne")
    return inner

@validation
def deneme(asd):
    print(asd)
    return 1

a=deneme("deneme")
print(a)