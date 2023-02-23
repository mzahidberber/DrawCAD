from Model.BaseModel import BaseModel


class MappingModel:
    @staticmethod
    def mapDictToClass(
        listItems: list[dict] or None, type: BaseModel) -> list[BaseModel] or None:
        return list(map(lambda x: type(x), listItems)) if listItems != None else None

    @staticmethod
    def mapClassToDict(listItems: list[BaseModel] or None) -> list[dict] or None:
        return (
            list(map(lambda x: x.to_dict(), listItems)) if listItems != None else None
        )
