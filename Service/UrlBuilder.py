from multipledispatch import dispatch

class UrlBuilder:
    def __init__(self) -> None:
        self.url:str=""
        self.params:str=""

    def urlBuild(self,url:str):
        if (self.url==""):self.url+=url
        else: self.url+=f"/{url}"
        return self

    @dispatch(str,str)
    def paramsBuild(self,username:str,password:str):
        if (self.params==""):
            self.params+=f"?username={username}&password={password}"
        return self

    @dispatch(str)
    def paramsBuild(self,param:str):
        if(self.params==""):self.params+=f"?{param}"
        else: self.params+=f"&{param}"
        return self


    def build(self):
        if (self.url!=None and self.params!=None):
            return self.url+self.params

