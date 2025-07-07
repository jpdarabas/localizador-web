from logging import config
from models import Solicitacao
import requests
import json
from utils import modelos
from utils import prompt

class Api:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Api, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_inicializado") and self._inicializado:
            return
        self._inicializado = True

        self.carregar_chaves() # apis = self.__apis_chaves.keys()
        self.__modelo: str = self.get_modelos()[0] if self.get_modelos() else None

    def realizar_pergunta(self,
    solicitacao: Solicitacao,
    info: str|dict):
        match self.get_api_modelo_selecionado():
            case "Gemini":
                resposta = self.request_gemini(prompt(solicitacao.dict_, info, solicitacao.descricao))
            case "OpenRouter":
                resposta = self.request_openrouter(prompt(solicitacao.dict_, info, solicitacao.descricao))
            case _:
                raise ValueError("Modelo não suportado ou chave da API não definida.")
            
        start_index = resposta.find("{")
        end_index = resposta.rfind("}") + 1

        # Extrai a parte do texto que parece ser um JSON
        texto_dict = resposta[start_index:end_index]

        # Substitui aspas simples por aspas duplas
        texto_dict = texto_dict.replace("'", "\"")

        # Agora tenta carregar a string JSON
        dicionario = json.loads(texto_dict)
        return resposta, dicionario


    def request_gemini(self, prompt:str, chave: str = None):
        # 1. Endpoint da API do Google
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.__modelo}:generateContent?key={chave if chave else self.definir_chave()}"

        # 2. Cabeçalho da requisição
        headers = {
            "Content-Type": "application/json",
        }

        # 3. Corpo (payload) da requisição no formato do Google
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }

        # 4. Fazendo a chamada POST
        response = requests.post(url, headers=headers, data=json.dumps(data))

        # 5. Extraindo a resposta
        if response.status_code == 200:
            response_json = response.json()
            # O caminho para o texto da resposta é um pouco mais longo
            text_response = response_json['candidates'][0]['content']['parts'][0]['text']
        else:
            raise ValueError(f"Erro na requisição: {response.status_code}") from None

        texto_dict =  response_json['candidates'][0]['content']['parts'][0]['text']
        return texto_dict 
    
    def request_openrouter(self, prompt: str, chave: str = None):
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
            "Authorization": f"Bearer {chave}",
            "Content-Type": "application/json",
            },
            data=json.dumps({
            "model": self.__modelo,
            "messages": [
                {
                "role": "user",
                "content": prompt
                }
            ],

            })
            )
        if response.status_code == 200:
            resposta_json = response.json()
            texto_resposta = resposta_json["choices"][0]["message"]["content"]
            print("Resposta:", texto_resposta)
        else:
            print("Erro:", response.text)


        texto_dict = resposta_json["choices"][0]["message"]["content"]

        return texto_dict
    
    def testar_chave(self, chave: str, api:str):
        try:
            match api:
                case "Gemini":
                    self.request_gemini("teste", chave)
                case "OpenRouter":
                    self.request_openrouter("teste", chave)
                case _:
                    raise ValueError("API não suportada no momento.")
                
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Erro de conexão ou chave inválida: {e}")
                
        except Exception as e:
            print(f"Erro ao testar chave: {e}")

    def carregar_chaves(self):
        with open("utils/config.json", "r") as file:
            self.__apis_chaves = json.load(file)

    def definir_chave(self):
        # Itera sobre modelos e salva a variavel api que é a chave onde o valor = self.__modelo
        for chave, valor in modelos.items():
            if self.__modelo in valor:
                print('a')
                api = chave
                break
        # Retorna a chave da API correspondente ao modelo
        return self.__apis_chaves[api] if self.__apis_chaves and api in self.__apis_chaves else None
    
    def adicionar_chave(self, api: str, chave: str):
        self.__apis_chaves[api] = chave
        with open("utils/config.json", "w") as file:
            json.dump(self.__apis_chaves, file, indent=4)

    # Getters 
    def get_modelos(self) -> list[str]:
        apis = list(self.__apis_chaves.keys())
        modelos_disponiveis = [modelo for api in apis if api in modelos.keys() for modelo in modelos[api]]
        return modelos_disponiveis
    
    def get_api_modelo_selecionado(self) -> str:
        if self.__modelo is None:
            return None
        api = [api for api, modelos in modelos.items() if self.__modelo in modelos]
        return api[0] if api else None

    @property
    def modelo(self) -> str:
        return self.__mode+telo

    @property
    def apis_chaves(self) -> dict[str, str]:
        return self.__apis_chaves
    
    # Setters
    @modelo.setter
    def modelo(self, modelo: str):
        self.__modelo = modelo


    @apis_chaves.setter
    def apis_chaves(self, apis_chaves: dict[str, str]):
        self.__apis_chaves = apis_chaves
