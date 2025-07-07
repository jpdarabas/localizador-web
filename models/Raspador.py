from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dateutil import parser
from datetime import datetime
from bs4 import BeautifulSoup as bs
from datetime import datetime
from collections import Counter, defaultdict
from selenium.webdriver.chrome.options import Options


class Raspador:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Raspador, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_inicializado") and self._inicializado:
            return
        self._inicializado = True
        
    
    def extrair_info(self, url:str,
    tipo:str):

        options = Options()
        options.add_argument("--headless=new")         # Executar em modo invisível (versão nova do headless)
        options.add_argument("--window-size=1920,1080")  # Resolução padrão de tela desktop
        options.add_argument("--disable-gpu")            # Boa prática com headless
        options.add_argument("--no-sandbox")             # Necessário em alguns ambientes Linux
        options.add_argument("--disable-dev-shm-usage")  # Necessário em alguns ambientes Linux

        driver = webdriver.Chrome(options=options)
        driver.get(url)

        WebDriverWait(driver, 3)
        html_content = driver.page_source

        print("Fechando o navegador.")

        soup = bs(html_content, 'html.parser')
        match tipo:
            case "tabela":
                try:
                    return self.pegar_tabela(soup)
                except Exception as e:
                    try:
                        return self.pegar_tabela_div(soup)
                    except Exception as e:
                        raise ValueError(f"Erro ao extrair tabela: {e}, tente novamente com outro tipo ou descrição.")
            case "card":
                try:
                        return self.pegar_tabela_div(soup)
                except Exception as e:
                    try: 
                        texto = soup.select_one("body").text.replace("\n", "")
                        return texto.strip()
                    except Exception as e:
                        raise ValueError(f"Erro ao extrair informações do card: {e}, tente novamente com outro tipo ou descrição.")
            case _:
                texto = soup.select_one("body").text.replace("\n", "")
                return texto.strip()
            

    def pegar_tabela(self, soup):
        try:
            tabelas = soup.select("table")
            tabela_resultado = {"linhas": []}
            for tabela in tabelas:
                colunas = tabela.select("th")
                nomes_colunas = [c.get_text() for c in colunas]
                tabela_resultado["colunas"] = nomes_colunas
                linhas = tabela.select("tr")
                for linha in linhas:
                    dados = linha.select("td")
                    conteudo_dados = [c.get_text() for c in dados]
                    tabela_resultado["linhas"].append(conteudo_dados)
        except Exception as e:
            tabela_resultado = self.pegar_tabela_div(soup)
        return tabela_resultado
    
    def pegar_tabela_div(self, soup):
        todos_os_divs = soup.find_all('div')

        lista_de_assinaturas = []

        for div in todos_os_divs:
            # 1. Pega a combinação de classes
            classes = ' '.join(div.get('class', []))

            # 2. Conta todos os elementos descendentes
            qtd_descendentes = len(div.find_all(True))

            # 3. Mede a profundidade (quantos pais até o topo)
            profundidade = len(list(div.parents))

            # Cria a assinatura como uma tupla
            assinatura = (classes, qtd_descendentes, profundidade)
            lista_de_assinaturas.append(assinatura)

        # 4. Usa o Counter para agrupar e contar as assinaturas idênticas
        contagem_estrutural = Counter(lista_de_assinaturas)

        # Converte o resultado do Counter para uma lista de dicionários para facilitar a visualização
        dados_para_df = []
        for (classes, descendentes, profundidade), contagem in contagem_estrutural.most_common(20):
            if contagem > 1 and classes != "": # Mostra apenas padrões que se repetem
                dados_para_df.append({
                    'Contagem': contagem,
                    'Classes': classes,
                    'Qtd. Descendentes': descendentes,
                    'Profundidade': profundidade
                })

        if dados_para_df:
            df = pd.DataFrame(dados_para_df)
            # Ajusta as opções do pandas para ver o nome completo das classes
            pd.set_option('display.max_colwidth', 120)

        classes = df.loc[df["Qtd. Descendentes"] == max(df["Qtd. Descendentes"])]["Classes"].iloc[0]
        contagem = df.loc[df["Qtd. Descendentes"] == max(df["Qtd. Descendentes"])]["Contagem"].iloc[0]

        # Substitui o ':' por '\:' para escapar o caractere especial
        classes_escapadas = classes.replace(':', r'\:').split(' ')
        # Cria o seletor com os pontos
        i = -1
        while True:
            seletor_css = f"div.{'.'.join(classes_escapadas[:i])}"
            if seletor_css == "div.":
                seletor_css += classes_escapadas[i]
            # Agora a busca vai funcionar
            elementos = soup.select(seletor_css)

            if len(elementos) >= contagem:
                break
            i -= 1

        tabela = []
        for div in elementos:
            qtd_descendentes = len(div.find_all(True))
            descendentes = div.find_all(recursive=False)
            if qtd_descendentes > 0:
                textos = [descendente.text.strip() for descendente in descendentes]
                tabela.append(textos)  # Remove duplicados e mantém a ordem
            else:
                tabela.append(div.text)
        print(tabela)
        return tabela
