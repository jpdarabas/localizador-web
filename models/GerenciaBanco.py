import sqlite3
import os
from models.Solicitacao import Solicitacao
from models.Dados import Dados
from models.Resultado import Resultado
import json

class GerenciaBanco():
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GerenciaBanco, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_inicializado") and self._inicializado:
            return
        self._inicializado = True
        self.nome_banco = "localiza_web.db"
        self.__conexao = None

    def conectar(self):
        self.__conexao = sqlite3.connect(self.nome_banco)
        self.__conexao.row_factory = sqlite3.Row
        self.__cursor = self.__conexao.cursor()
        self.__conexao.execute("PRAGMA foreign_keys = ON")

    def desconectar(self):
        if self.__cursor:
            self.__cursor.close()
        if self.__conexao:
            self.__conexao.close()

    def criar_tabelas(self):
        if not self.__conexao:
            self.conectar()

        arquivos_sql = os.listdir("utils/sql")

        arquivos_sql = [os.path.join("utils/sql", arquivo) for arquivo in arquivos_sql if arquivo.endswith('.sql')]

        for arquivo in arquivos_sql:
            with open(arquivo, 'r', encoding='utf-8') as f:
                sql_script = f.read()
            self.__cursor.executescript(sql_script)

        self.__conexao.commit()

    def carregar_dados(self):
        if not self.__conexao:
            self.conectar()

        self.__cursor.execute("SELECT * FROM solicitacoes")
        solicitacoes = self.__cursor.fetchall()
        
        self.__cursor.execute("SELECT * FROM dados")
        dados = self.__cursor.fetchall()

        self.__cursor.execute("SELECT * FROM resultados")
        resultados = self.__cursor.fetchall()

        return solicitacoes, dados, resultados
    
    # Inserts

    def inserir_solicitacao(self, solicitacao: Solicitacao):
        if not self.__conexao:
            self.conectar()

        sql = """
        INSERT INTO solicitacoes (url, tipo, descricao, status, dict_)
        VALUES (?, ?, ?, ?, ?)
        """
        dict_serializado = json.dumps(solicitacao.dict_)
        if solicitacao.descricao is None:
            solicitacao.descricao = ''

        self.__cursor.execute(sql, (solicitacao.url, solicitacao.tipo, solicitacao.descricao if solicitacao.descricao else '', solicitacao.status, dict_serializado))
        self.__conexao.commit()
        solicitacao.id = self.__cursor.lastrowid

        return solicitacao
    
    def inserir_dados(self, dados: Dados):
        if not self.__conexao:
            self.conectar()

        sql = """
        INSERT INTO dados (dados, titulo)
        VALUES (?, ?)
        """
        dados_dict = json.dumps(dados.dados)
        self.__cursor.execute(sql, (dados_dict, dados.titulo))
        self.__conexao.commit()
        dados.id = self.__cursor.lastrowid

        return dados
    
    def inserir_resultado(self, resultado: Resultado):
        """
        id INTEGER PRIMARY KEY AUTOINCREMENT,
    resposta TEXT NOT NULL,
    id_dados INTEGER NOT NULL,
    id_solicitacao INTEGER NOT NULL,
    data TEXT DEFAULT (datetime('now'))"""
        if not self.__conexao:
            self.conectar()

        sql = """
        INSERT INTO resultados (resposta, id_dados, id_solicitacao, data)
        VALUES (?, ?, ?, ?)
        """
        self.__cursor.execute(sql, (str(resultado.resposta), resultado.id_dados, resultado.id_solicitacao, resultado.data))
        self.__conexao.commit()
        resultado.id = self.__cursor.lastrowid

        return resultado
    
    # Updates

    def atualizar_solicitacao(self, solicitacao: Solicitacao):
        if not self.__conexao:
            self.conectar()

        sql = """
        UPDATE solicitacoes
        SET url = ?, tipo = ?, descricao = ?, status = ?
        WHERE id = ?
        """
        self.__cursor.execute(sql, (solicitacao.url, solicitacao.tipo, solicitacao.descricao, solicitacao.status, solicitacao.id))
        self.__conexao.commit()

    def atualizar_dados(self, dados: Dados):
        if not self.__conexao:
            self.conectar()

        sql = """
        UPDATE dados
        SET dados = ?, titulo = ?
        WHERE id = ?
        """
        self.__cursor.execute(sql, (str(dados.dados), dados.titulo, dados.id))
        self.__conexao.commit()

    def atualizar_resultado(self, resultado: Resultado):
        if not self.__conexao:
            self.conectar()

        sql = """
        UPDATE resultados
        SET resultado = ?, tipo = ?, id_dados = ?, id_solicitacao = ?
        WHERE id = ?
        """
        self.__cursor.execute(sql, (str(resultado.resultado), resultado.tipo, resultado.id_dados, resultado.id_solicitacao, resultado.id))
        self.__conexao.commit()

    # Deletes

    def deletar_solicitacao(self, id: int):
        if not self.__conexao:
            self.conectar()

        sql = "DELETE FROM solicitacoes WHERE id = ?"
        self.__cursor.execute(sql, (id,))
        self.__conexao.commit()

    def deletar_dados(self, id: int):
        if not self.__conexao:
            self.conectar()

        sql = "DELETE FROM dados WHERE id = ?"
        self.__cursor.execute(sql, (id,))
        self.__conexao.commit()

    def deletar_resultado(self, id: int):
        if not self.__conexao:
            self.conectar()

        sql = "DELETE FROM resultados WHERE id = ?"
        self.__cursor.execute(sql, (id,))
        self.__conexao.commit()

        