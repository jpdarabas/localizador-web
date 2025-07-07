from PyQt6.QtWidgets import *
from models import *
from datetime import date
from utils.modelos import modelos

class ModalAdicionarChave(QDialog):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        form = QFormLayout()
        
        self.setWindowTitle("Adicionar Chave")

        # Select da api usando modelos.keys()
        modelos_api = modelos.keys()
        self.api_select = QComboBox()
        self.api_select.addItems(modelos_api)

        # Input para a chave da API
        self.chave_input = QLineEdit()
        self.chave_input.setPlaceholderText("Digite a chave da API")

        form.addRow("API:", self.api_select)
        form.addRow("Chave da API:", self.chave_input)
    
        layout.addLayout(form)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        layout.addWidget(self.buttons)

    def get_dados_editados(self):
        return self.api_select.currentText(), self.chave_input.text()