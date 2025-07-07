class Solicitacao:
    def __init__(self, 
        id: int,
        url: str,
        tipo: str,
        descricao: str,
        status: str,
        dict_: dict[str, list] = {
            "linhas": [], "colunas": []
        }):
        self.__id = id
        self.__url = url
        self.__tipo = tipo
        self.__descricao = descricao
        self.__status = status
        self.__dict_ = dict_

    # Getters

    @property
    def id(self) -> int:
        return self.__id

    @property
    def url(self) -> str:
        return self.__url

    @property
    def tipo(self) -> str:
        return self.__tipo

    @property
    def descricao(self) -> str:
        return self.__descricao

    @property
    def status(self) -> str:
        return self.__status
    
    @property
    def dict_(self) -> dict[str, list]:
        return self.__dict_
    
    # Setters

    @id.setter
    def id(self, id: int):
        self.__id = id

    @url.setter
    def url(self, url: str):
        self.__url = url

    @tipo.setter
    def tipo(self, tipo: str):
        self.__tipo = tipo

    @descricao.setter
    def descricao(self, descricao: str):
        self.__descricao = descricao

    @status.setter
    def status(self, status: str):
        if status not in ["pendente", "concluída", 
        "erro"]:
            raise ValueError("Status inválido. Deve ser 'pendente', 'concluída' ou 'erro'.")
        self.__status = status

    @dict_.setter
    def dict_(self, dict_: dict[str, list]):
        if not isinstance(dict_, dict) or not all(isinstance(v, list) for v in dict_.values()):
            raise ValueError("O dicionário deve conter listas como valores.")
        self.__dict_ = dict_