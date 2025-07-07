from models.Raspador import Raspador
from models.Api import Api
from models.Solicitacao import Solicitacao
from models.Resultado import Resultado
from models.Dados import Dados
from models.GerenciaBanco import GerenciaBanco
from datetime import datetime
import json
import pandas as pd
import fpdf

class Gerenciador:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Gerenciador, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_inicializado") and self._inicializado:
            return
        self._inicializado = True
        self.__raspador = Raspador()
        self.api = Api()
        self.__db = GerenciaBanco()
        self.__db.conectar()
        self.__db.criar_tabelas()
        solicitacoes, dados, resultados = self.__db.carregar_dados()
        
        self.__solicitacoes = [Solicitacao(**sol) for sol in solicitacoes]

        for solicitacao in self.__solicitacoes:
            solicitacao.dict_ = json.loads(solicitacao.dict_)

        self.__dados = [Dados(**dado) for dado in dados]

        for dado in self.__dados:
            if isinstance(dado.dados, str):
                try:
                    dado.dados = json.loads(dado.dados)
                except json.JSONDecodeError:
                    # Se falhar, tenta corrigir aspas simples para duplas
                    try:
                        corrected = dado.dados.replace("'", '"')
                        dado.dados = json.loads(corrected)
                    except:
                        dado.dados = {
                                        "linhas": [], "colunas": []
                                        } 
                        
            elif isinstance(dado.dados, (dict, list)):
                # Já está decodificado, não faz nada
                pass
            else:
                dado.dados = {
                                "linhas": [], "colunas": []
                                }  # Valor padrão para casos inválidos


        self.__resultados = [Resultado(**resultado) for resultado in resultados]

    def realizar_solicitacao(self,
    titulo: str,
    url: str,
    tipo: str, # Tabela, Card, Outro
    descricao: str = None):
        solicitacao = Solicitacao(
            id=None,
            url=url,
            tipo=tipo,
            descricao=descricao,
            status="pendente"
        )
        # Adicionar ao banco de dados e adicionar id
        solicitacao = self.__db.inserir_solicitacao(solicitacao)

        self.__solicitacoes.append(solicitacao)

        try:
            # Extrai informações do site
            info = self.__raspador.extrair_info(url, tipo)
            # Realiza a pergunta na API
            try:
                resposta, dict_ = self.api.realizar_pergunta(solicitacao, info)
            except Exception as e:
                raise ValueError(f"Erro ao realizar a pergunta: {e}, tente novamente com outro tipo ou descrição.")
            # Extrai os dados da resposta
            dados = Dados(
                id=None,
                data=datetime.now(),
                titulo=titulo,
                dados=dict_
            )

            # Adiciona ao banco de dados e adiciona id
            dados = self.__db.inserir_dados(dados)

            # Cria o resultado
            resultado = Resultado(
                id=None,
                resposta=resposta,
                id_dados=dados.id,
                id_solicitacao=solicitacao.id,
                data=datetime.now()
            )

            # Adiciona ao banco e adiciona id
            resultado = self.__db.inserir_resultado(resultado)

            # Salva o resultado
            self.__resultados.append(resultado)
            self.__dados.append(dados)

            # Atualiza a solicitação para concluída
            solicitacao.status = "concluída"
            self.__db.atualizar_solicitacao(solicitacao)
            self.__solicitacoes[-1] = solicitacao
        except Exception as e:
            solicitacao.status = "erro"
            self.__db.atualizar_solicitacao(solicitacao)
            self.__solicitacoes[-1] = solicitacao
            raise Exception(f"Erro ao realizar a solicitação: {e}, tente novamente com outro tipo ou descrição.")

    # Cria uma tabela vazia no banco de dados
    def criar_tabela(self, 
                     titulo:str,
                     colunas:list[str]):
        dado = Dados(
            id=None,
            data=datetime.now(),
            titulo=titulo,
            dados={
                "linhas": [],
                "colunas": colunas
            }
        )
        # Cria um dado vazio e adiciona ao banco de dados
        dado = self.__db.inserir_dados(dado)
        self.__dados.append(dado)

    def adicionar_linha_tabela(self,
                               dados: Dados,
                               url: str):
        tipo =  "outro"
        descricao = "ADICIONE APENAS UMA LINHA NA TABELA E MANTENHA AS LINHAS EXISTENTES"
        solicitacao = Solicitacao(
            id=None,
            url=url,
            tipo=tipo,
            descricao=descricao,
            status="pendente",
            dict_=dados.dados
        )
        # Adicionar ao banco de dados e adicionar id
        solicitacao = self.__db.inserir_solicitacao(solicitacao)

        self.__solicitacoes.append(solicitacao)
        # Extrai informações do site
        info = self.__raspador.extrair_info(url, tipo)
        # Realiza a pergunta na API
        try:
            resposta, dict_ = self.api.realizar_pergunta(solicitacao, info)
        except Exception as e:
            raise ValueError(f"Erro ao realizar a pergunta: {e}, tente novamente com outro tipo ou descrição.")
        
        resultado = Resultado(
            id=None,
            resposta=resposta,
            id_dados=dados.id,
            id_solicitacao=solicitacao.id,
            data=datetime.now()
        )

        # Atualiza o dicionário de dados
        dados.dados = dict_

        # Atualiza o dado no banco de dados
        self.__db.atualizar_dados(dados)

        # Salva o resultado
        self.__resultados.append(resultado)
        
        # Atualiza o dado no gerenciador
        self.atualizar_dados(dados)


        # Atualiza a solicitação para concluída
        solicitacao.status = "concluída"
        self.__db.atualizar_solicitacao(solicitacao)
        self.__solicitacoes[-1] = solicitacao

    def solicitar_dados_atualizados(self, dados: Dados):
        resultados_dados = [resultado for resultado in self.__resultados if resultado.id_dados == dados.id]
        solicitacoes = [solicitacao for solicitacao in self.__solicitacoes if solicitacao.id in [resultado.id_solicitacao for resultado in resultados_dados]]
        dict_ = None
        for solicitacao in solicitacoes:
            nova_solicitacao = Solicitacao(
            id=None,
            url=solicitacao.url,
            tipo=solicitacao.tipo,
            descricao=solicitacao.descricao,
            status="pendente",
            dict_= dict_ if dict_ else solicitacao.dict_
            )
            # Adicionar ao banco de dados e adicionar id
            nova_solicitacao = self.__db.inserir_solicitacao(nova_solicitacao)

            self.__solicitacoes.append(nova_solicitacao)
            # Extrai informações do site
            info = self.__raspador.extrair_info(nova_solicitacao.url, nova_solicitacao.tipo)
            # Realiza a pergunta na API
            try:
                resposta, dict_ = self.api.realizar_pergunta(nova_solicitacao, info)
            except Exception as e:
                raise ValueError(f"Erro ao realizar a pergunta: {e}, tente novamente com outro tipo ou descrição.")
            
            resultado = Resultado(
                id=None,
                resposta=resposta,
                id_dados=dados.id,
                id_solicitacao=nova_solicitacao.id,
                data=datetime.now()
            )

            # Atualiza o dicionário de dados
            dados.dados = dict_
            dados.data = datetime.now()

            # Atualiza o dado no banco de dados
            self.__db.atualizar_dados(dados)

            # Salva o resultado
            self.__resultados.append(resultado)
            
            # Atualiza o dado no gerenciador
            self.atualizar_dados(dados)

            # Atualiza a solicitação para concluída
            nova_solicitacao.status = "concluída"
            self.__db.atualizar_solicitacao(nova_solicitacao)
            self.__solicitacoes[-1] = nova_solicitacao

    def atualizar_dados(self,
                             dado: Dados):
        # Atualiza o dado no gerenciador
        for i, d in enumerate(self.__dados):
            if d.id == dado.id:
                self.__dados[i] = dado
                break

    def remover_dados(self, dado: Dados):
        # Remove o dado do gerenciador
        self.__dados = [d for d in self.__dados if d.id != dado.id]
        self.__db.deletar_dados(dado.id)


    # Getters
    @property
    def solicitacoes(self) -> list[Solicitacao]:
        return self.__solicitacoes

    @property
    def resultados(self) -> list[Resultado]:
        return self.__resultados
    
    @property
    def dados(self) -> list[Dados]:
        return self.__dados
    

    # Desconectar do banco de dados
    def desconectar(self):
        self.__db.desconectar()