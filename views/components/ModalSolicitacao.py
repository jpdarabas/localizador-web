from PyQt6.QtWidgets import *
from models import *
from datetime import date
from utils.modelos import modelos

class ModalSolicitacao(QDialog):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        form = QFormLayout()
        
        self.setWindowTitle("Nova Solicitação")

        # Input para o título da tabela
        self.titulo_input = QLineEdit()
        self.titulo_input.setPlaceholderText("Digite o título")
        form.addRow("Título:", self.titulo_input)

        # Input para a URL
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Digite a URL")
        form.addRow("URL:", self.url_input)

        # Select tipo (Tabela, Card, Outro)
        self.tipo_select = QComboBox()
        self.tipo_select.addItems(["Tabela", "Card", "Outro"])
        form.addRow("Tipo:", self.tipo_select)

        # Input para a descrição
        self.descricao_input = QLineEdit()
        self.descricao_input.setPlaceholderText("Digite a descrição")
        form.addRow("Descrição:", self.descricao_input)


        layout.addLayout(form)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        layout.addWidget(self.buttons)

    def get_dados_editados(self):
        return self.titulo_input.text(), self.url_input.text(), self.tipo_select.currentText(), self.descricao_input.text()