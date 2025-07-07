from PyQt6.QtWidgets import *
from models import Gerenciador
from PyQt6.QtCore import pyqtSignal, Qt
from views.styles import styles
from .components import *

class TelaDados(QWidget):

    def __init__(self, dado):
        super().__init__()
        self.gerenciador = Gerenciador()
        self.dados = dado
        self.initUI()

        self.setStyleSheet(styles) 
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowCloseButtonHint | Qt.WindowType.WindowMinimizeButtonHint)



    def initUI(self):
        self.setWindowTitle("Localizador Web")
        self.setMinimumSize(1200, 600)

         # Widget central e layout principal
        # Layout principal
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.atualizar_widgets()

        
        
    def atualizar_widgets(self):
        # Limpa o layout existente
        if not hasattr(self, 'main_layout') or self.main_layout is None:
            return
        self.limpar_layout(self.main_layout)

        sublayout = QVBoxLayout()


         # Cabeçalho (barra de navegação)
        header = QHBoxLayout()

        # cabeçalho:

        # Botão Voltar
        self.btn_voltar = QPushButton("Voltar")
        self.btn_voltar.clicked.connect(self.close)
        header.addWidget(self.btn_voltar)

        # Botão atualizar
        self.btn_atualizar = QPushButton("Atualizar")
        self.btn_atualizar.clicked.connect(self.atualizar)
        header.addWidget(self.btn_atualizar)

        # Botão nova linha
        self.btn_nova_linha = QPushButton("Nova Linha")
        self.btn_nova_linha.clicked.connect(self.adicionar_linha)
        header.addWidget(self.btn_nova_linha)

        # Botão Exportar
        self.btn_exportar = QPushButton("Exportar")
        self.btn_exportar.clicked.connect(self.exportar_dados)
        header.addWidget(self.btn_exportar)

        # Body: lista com solicitações, ao abrir abre TelaDados
        # Área de scroll
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        
        # Container do conteúdo (dentro do scroll)
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_layout.setSpacing(15)

        for dados in [self.gerenciador.dados]:
            item_layout = QHBoxLayout()
            print(dados)
            # Titulo
            label_titulo = QLabel(self.dados.titulo)
            item_layout.addWidget(label_titulo)

            # Botão Abrir
            btn_abrir = QPushButton("")
            btn_abrir.clicked.connect(lambda _, d=dados:  None)
            item_layout.addWidget(btn_abrir)

            # Botão Excluir
            btn_excluir = QPushButton("")
            btn_excluir.clicked.connect(lambda _, d=dados: self.excluir_dados(d))
            item_layout.addWidget(btn_excluir)

            self.content_layout.addLayout(item_layout)
            break
        
        # Apenas mantenha a tabela:
        tabela = QTableWidget()
        # Adiciona as colunas
        tabela.setColumnCount(len(self.dados.dados["colunas"])) 
        tabela.setRowCount(len(self.dados.dados["linhas"]))
        tabela.setHorizontalHeaderLabels(self.dados.dados["colunas"])

        # Configuração visual
        tabela.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        tabela.verticalHeader().setVisible(False)
        tabela.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # Adiciona as linhas
        for row, linha in enumerate(self.dados.dados["linhas"]):
            print(linha)
            for idx, item in enumerate(linha):
                item_widget = QTableWidgetItem(item)
                item_widget.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                tabela.setItem(row, idx, item_widget)

        # Ajustes finais
        tabela.resizeColumnsToContents()
        self.content_layout.addWidget(tabela)
        

        # O resto do layout permanece igual:
        sublayout.addLayout(header)
        self.scroll.setWidget(self.content_widget)
        sublayout.addWidget(self.scroll)
        self.main_layout.addLayout(sublayout)



    def limpar_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                sublayout = item.layout()
                if sublayout is not None:
                    self.limpar_layout(sublayout)
                    sublayout.deleteLater()
        
    
    def excluir_dados(self, dado):
        self.gerenciador.remover_dados(dado)
        self.atualizar_widgets()

    

    def atualizar(self):
        try:
            self.gerenciador.atualizar_dados(self.dados)
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))
            print(e)
            return
        self.atualizar_widgets()

    def adicionar_linha(self):
        try:
            modal = ModalNovaLinha()
            if modal.exec() == QDialog.DialogCode.Accepted:
                linha = modal.get_dados_editados()
                self.gerenciador.adicionar_linha_tabela(self.dados, linha)
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))
            print(e)
            return
        self.atualizar_widgets()

    def exportar_dados(self):
        try:
            modal = ModalExportar()
            if modal.exec() == QDialog.DialogCode.Accepted:
                formato = modal.get_dados_editados()
                self.dados.exportar(formato)
                QMessageBox.information(self, "Exportação", f"Dados exportados com sucesso para o formato {formato}.")
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))
            print(e)
            return
        self.atualizar_widgets()

# class TelaDados(QWidget):

#     def __init__(self, dado):
#         super().__init__()
#         self.dados = dado
#         self.gerenciador = Gerenciador()
#         self.initUI()

#         self.setStyleSheet(styles) 
#         self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowCloseButtonHint | Qt.WindowType.WindowMinimizeButtonHint)



#     def initUI(self):
#         self.setWindowTitle("Localizador Web")
#         self.setMinimumSize(800, 600)

#          # Widget central e layout principal
#         # Layout principal
#         self.main_layout = QVBoxLayout(self)
#         self.main_layout.setContentsMargins(0, 0, 0, 0)

#         self.atualizar_widgets()

        
        
#     def atualizar_widgets(self):
#         # Limpa o layout existente
#         if not hasattr(self, 'main_layout') or self.main_layout is None:
#             return
#         self.limpar_layout(self.main_layout)

#         sublayout = QVBoxLayout()

#          # Cabeçalho (barra de navegação)
#         header = QHBoxLayout()

#         # cabeçalho:

#         # Botão Voltar
#         self.btn_voltar = QPushButton("Voltar")
#         self.btn_voltar.clicked.connect(self.close)
#         header.addWidget(self.btn_voltar)

#         # Botão atualizar
#         self.btn_atualizar = QPushButton("Atualizar")
#         self.btn_atualizar.clicked.connect(self.atualizar)
#         header.addWidget(self.btn_atualizar)

#         # Botão nova linha
#         self.btn_nova_linha = QPushButton("Nova Linha")



#         # Body: lista com solicitações, ao abrir abre TelaDados
#         # Área de scroll
#         self.scroll = QScrollArea()
#         self.scroll.setWidgetResizable(True)
        
#         # Container do conteúdo (dentro do scroll)
#         self.content_widget = QWidget()
#         self.content_layout = QVBoxLayout(self.content_widget)
#         self.content_layout.setContentsMargins(10, 10, 10, 10)
#         self.content_layout.setSpacing(15)


        # # Tabela com os dados
        # tabela = QTableWidget()
        # # Adiciona as colunas
        # tabela.setColumnCount(len(self.dados.dados["colunas"])) 
        # tabela.setHorizontalHeaderLabels(self.dados.dados["colunas"])

        # # Configuração visual
        # tabela.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # tabela.verticalHeader().setVisible(False)
        # tabela.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        # # Adiciona as linhas
        # for row, linha in enumerate(self.dados.dados["linhas"]):

        #     for idx, item in enumerate(linha):
        #         item = QTableWidgetItem(item)
        #         item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        #         tabela.setItem(row, idx, QTableWidgetItem(item))

                
        
        # # Ajustes finais
        # tabela.resizeColumnsToContents()
        # self.content_layout.addWidget(tabela)



        
#         sublayout.addLayout(header)
#         sublayout.addWidget(self.scroll)
        
#         self.scroll.setWidget(self.content_widget)

#         self.main_layout.addLayout(sublayout)



#     def limpar_layout(self, layout):
#         while layout.count():
#             item = layout.takeAt(0)
#             widget = item.widget()
#             if widget is not None:
#                 widget.deleteLater()
#             else:
#                 sublayout = item.layout()
#                 if sublayout is not None:
#                     self.limpar_layout(sublayout)
#                     sublayout.deleteLater()
        
    

#     def atualizar(self):
#         try:
#             self.gerenciador.atualizar_dados(self.dados)
#         except Exception as e:
#             QMessageBox.critical(self, "Erro", str(e))
#             print(e)
#             return
#         self.atualizar_widgets()

   
