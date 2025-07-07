from PyQt6.QtWidgets import *
from models import *
from datetime import date
from utils.modelos import modelos

class ModalNovaLinha(QDialog):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.setWindowTitle("Adicionar Linha")

        # Input para a URL
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Digite a URL")

        form.addRow("URL:", self.url_input)

        layout.addLayout(form)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        layout.addWidget(self.buttons)

    def get_dados_editados(self):
        return self.url_input.text()