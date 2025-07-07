from PyQt6.QtWidgets import *
from models import *
from datetime import date
from utils.modelos import modelos

class ModalExportar(QDialog):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.setWindowTitle("Exportar Dados")

        # Selectbox opções de exportação
        self.exportar_select = QComboBox()
        self.exportar_select.addItems(["CSV", "Excel", "PDF"])

        form.addRow("Formato:", self.exportar_select)

        layout.addLayout(form)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        layout.addWidget(self.buttons)

    def get_dados_editados(self):
        return self.exportar_select.currentText()