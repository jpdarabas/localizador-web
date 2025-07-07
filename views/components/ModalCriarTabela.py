from PyQt6.QtWidgets import *
from datetime import date


class ModalCriarTabela(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Criar Tabela")
        self.colunas = []

        layout = QVBoxLayout(self)
        form = QFormLayout()

        # Input para o título da tabela
        self.titulo_input = QLineEdit()
        self.titulo_input.setPlaceholderText("Digite o título da tabela")
        form.addRow("Título da Tabela:", self.titulo_input)

        layout.addLayout(form)

        # Input para adicionar coluna
        self.input_coluna = QLineEdit()
        self.input_coluna.setPlaceholderText("Digite o nome da coluna")

        self.btn_adicionar_coluna = QPushButton("Adicionar Coluna")
        self.btn_adicionar_coluna.clicked.connect(self.adicionar_coluna)

        item_layout = QHBoxLayout()
        item_layout.addWidget(self.input_coluna)
        item_layout.addWidget(self.btn_adicionar_coluna)
        layout.addLayout(item_layout)

        # Área onde as colunas são exibidas
        self.colunas_layout = QVBoxLayout()
        layout.addWidget(QLabel("Colunas:"))
        layout.addLayout(self.colunas_layout)

        # Botões de salvar/cancelar
        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

    def adicionar_coluna(self):
        nome = self.input_coluna.text().strip()
        if nome and nome not in self.colunas:
            self.colunas.append(nome)
            self.input_coluna.clear()
            self.atualizar_colunas()

    def remover_coluna(self, nome):
        if nome in self.colunas:
            self.colunas.remove(nome)
            self.atualizar_colunas()

    def atualizar_colunas(self):
        # Limpa todos os widgets antigos
        while self.colunas_layout.count():
            item = self.colunas_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Adiciona os widgets atualizados
        for nome in self.colunas:
            linha = QHBoxLayout()
            label = QLabel(nome)
            btn_remover = QPushButton("Remover")
            btn_remover.clicked.connect(lambda _, n=nome: self.remover_coluna(n))
            linha.addWidget(label)
            linha.addWidget(btn_remover)

            container = QWidget()
            container.setLayout(linha)
            self.colunas_layout.addWidget(container)

    def get_dados_editados(self):
        return self.titulo_input.text().strip(), self.colunas
