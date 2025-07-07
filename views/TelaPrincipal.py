from PyQt6.QtWidgets import *
from models import Gerenciador
from PyQt6.QtCore import pyqtSignal, Qt
from views.styles import styles
from .components import *
from views import TelaDados

class TelaPrincipal(QWidget):

    def __init__(self):
        super().__init__()
        self.gerenciador = Gerenciador()

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

        # Selectbox Selecionar Modelo
        self.btn_select_modelo = QComboBox()
        self.btn_select_modelo.addItems(self.gerenciador.api.get_modelos())
        self.btn_select_modelo.currentIndexChanged.connect(self.selecionar_modelo)
        header.addWidget(self.btn_select_modelo)
        # Botão Adicionar Chave
        self.btn_adicionar_chave = QPushButton("Adicionar Chave")
        
        self.btn_adicionar_chave.clicked.connect(self.adicionar_chave)
        header.addWidget(self.btn_adicionar_chave)
        # Botão Nova Solicitação
        self.btn_nova_solicitacao = QPushButton("Nova Solicitação")
        
        self.btn_nova_solicitacao.clicked.connect(self.nova_solicitacao)
        header.addWidget(self.btn_nova_solicitacao)

        # Botão Criar tabela
        self.btn_criar_tabela = QPushButton("Criar Tabela")

        self.btn_criar_tabela.clicked.connect(self.criar_tabela)
        header.addWidget(self.btn_criar_tabela)



        # Body: lista com solicitações, ao abrir abre TelaDados
        # Área de scroll
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        
        # Container do conteúdo (dentro do scroll)
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_layout.setSpacing(15)

        for dados in self.gerenciador.dados:
            item_layout = QHBoxLayout()

            # Titulo
            label_titulo = QLabel(dados.titulo)
            item_layout.addWidget(label_titulo)

            # Botão Abrir
            btn_abrir = QPushButton("Abrir")
            btn_abrir.clicked.connect(lambda _, d=dados:  self.abrir_dados(d))
            item_layout.addWidget(btn_abrir)

            # Botão Excluir
            btn_excluir = QPushButton("Excluir")
            btn_excluir.clicked.connect(lambda _, d=dados: self.excluir_dados(d))
            item_layout.addWidget(btn_excluir)

            self.content_layout.addLayout(item_layout)


        
        sublayout.addLayout(header)
        sublayout.addWidget(self.scroll)
        
        self.scroll.setWidget(self.content_widget)

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

    def selecionar_modelo(self):
        modelo_selecionado = self.btn_select_modelo.currentText()

        self.gerenciador.api.modelo = modelo_selecionado

    def adicionar_chave(self):
            try:
                modal = ModalAdicionarChave()
                if modal.exec() == QDialog.DialogCode.Accepted:
                    api, chave = modal.get_dados_editados()
                    self.gerenciador.api.adicionar_chave(api, chave)
            except ValueError as e:
                QMessageBox.critical(self, "Erro", str(e))
                return
            except Exception as e:
                QMessageBox.critical(self, "Erro", str(e))
                return
            self.atualizar_widgets()

    def criar_tabela(self):
        try:
            modal = ModalCriarTabela()
            if modal.exec() == QDialog.DialogCode.Accepted:
                titulo, colunas = modal.get_dados_editados()
                self.gerenciador.criar_tabela(titulo, colunas)
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))
            print(e)
            return
        self.atualizar_widgets()

    def nova_solicitacao(self):
        try:
            modal = ModalSolicitacao()
            self.gerenciador.api.get_api_modelo_selecionado()
            if modal.exec() == QDialog.DialogCode.Accepted:
                titulo, url, tipo, descricao = modal.get_dados_editados()
                if descricao.strip() == "":
                    descricao = None
                self.gerenciador.realizar_solicitacao(titulo, url, tipo, descricao)
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))
            print(e)
            return
        self.atualizar_widgets()

   
    def abrir_dados(self, dado):
        # Abre TelaDados
        tela_dados = TelaDados(dado)
        tela_dados.show()