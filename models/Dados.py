from datetime import datetime
import json
import fpdf
import pandas as pd

class Dados:
    def __init__(self,
        id: int,
        data: datetime,
        titulo: str,
        dados: dict[str, list] = {
            "linhas": [], "colunas": []
            }):
        self.__id = id
        self.__titulo = titulo
        self.__dados = dados
        self.__data = data

    def exportar(self, tipo: str = "json"):
        """
        Exporta o resultado no formato especificado.
        Args:
            tipo (str): [json, excel, csv, pdf]
        """
        match tipo.lower():
            case "csv":
                pd.DataFrame(self.__dados["linhas"], columns=self.__dados["colunas"]).to_csv(f"{'_'.join(self.__titulo.split())}.csv", index=False)
            case "excel":
                pd.DataFrame(self.__dados["linhas"], columns=self.__dados["colunas"]).to_excel(f"{'_'.join(self.__titulo.split())}.xlsx", index=False)
            case "json":
                with open(f"{'_'.join(self.__titulo.split())}.json", 'w') as f:
                    json.dump(self.__dados, f, indent=4)
            case "pdf":
                # Configurações do PDF
                pdf = fpdf.FPDF(orientation='L', unit='mm', format='A4')  # 'L' para landscape (paisagem)
                pdf.add_page()

                # Título centralizado
                titulo = self.__titulo
                pdf.set_font("Arial", size=16)
                pdf.cell(0, 10, txt=titulo, ln=1, align="C")

                if len(self.__dados["linhas"]) > 0:
                    # Configuração da tabela
                    pdf.set_font("Arial", size=10)
                    colunas = self.__dados["colunas"]
                    linhas = self.__dados["linhas"]
                    
                    # 1. Calcular larguras das colunas automaticamente
                    # Primeiro encontramos o texto mais largo em cada coluna
                    larguras = []
                    for i, coluna in enumerate(colunas):
                        # Inicia com a largura do cabeçalho
                        max_width = pdf.get_string_width(coluna) + 6  # +6 para padding
                        
                        # Verifica todas as células da coluna
                        for linha in linhas:
                            if i < len(linha):  # Verifica se existe o índice na linha
                                cell_width = pdf.get_string_width(str(linha[i])) + 6
                                if cell_width > max_width:
                                    max_width = cell_width
                        
                        # Limita a largura máxima para não ultrapassar a página
                        larguras.append(min(max_width, 60))  # 60mm é o máximo por coluna
                    
                    # 2. Desenhar cabeçalho da tabela
                    pdf.set_fill_color(200, 220, 255)  # Cor de fundo do cabeçalho
                    pdf.set_font("Arial", 'B', 12)  # Fonte em negrito para cabeçalho
                    
                    for i, coluna in enumerate(colunas):
                        pdf.cell(larguras[i], 10, coluna, border=1, fill=True)
                    pdf.ln()
                    
                    # 3. Desenhar linhas da tabela
                    pdf.set_font("Arial", size=10)
                    pdf.set_fill_color(255, 255, 255)  # Fundo branco para células
                    
                    for linha in linhas:
                        for i, item in enumerate(linha):
                            if i < len(larguras):  # Verifica se existe largura definida
                                pdf.cell(larguras[i], 10, str(item), border=1)
                        pdf.ln()
                    
                    # 4. Ajustar posição para não cortar a tabela
                    if pdf.get_y() > 180:  # Se estiver perto do final da página
                        pdf.add_page(orientation='L')  # Nova página em paisagem

                # Salvar o PDF
                pdf.output(f"{'_'.join(self.__titulo.split())}.pdf")
            case _:
                raise ValueError("Formato de exportação não suportado.")

    # Getters
    @property
    def id(self) -> int:
        return self.__id
    @property
    def titulo(self) -> str:
        return self.__titulo
    @property
    def dados(self) -> dict[list, list]:
        return self.__dados
    @property
    def data(self) -> datetime:
        return self.__data
    
    # Setters
    @id.setter
    def id(self, id: int):
        self.__id = id
    @titulo.setter
    def titulo(self, titulo: str):
        self.__titulo = titulo
    @dados.setter
    def dados(self, dados: dict[list, list]):
        self.__dados = dados
    @data.setter
    def data(self, data: datetime):
        self.__data = data