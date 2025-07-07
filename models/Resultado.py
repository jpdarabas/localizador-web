from datetime import datetime
import json
class Resultado:
    def __init__(self, 
        id: int,
        resposta: str,
        id_dados: int,
        id_solicitacao: int,
        data: datetime):
        self.__id = id
        self.__resposta = resposta
        self.__id_dados = id_dados
        self.__id_solicitacao = id_solicitacao
        self.__data = data



    # Getters
    @property
    def id(self) -> int:
        return self.__id
    @property
    def resposta(self) -> str:
        return self.__resposta
    @property
    def id_dados(self) -> int:
        return self.__id_dados
    @property
    def id_solicitacao(self) -> int:
        return self.__id_solicitacao
    @property
    def data(self) -> datetime:
        return self.__data
    
    # Setters
    @id.setter
    def id(self, id: int):
        self.__id = id
