from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
import sys

from models import Gerenciador
from views import TelaPrincipal

def main():
    app = QApplication(sys.argv)  # cria o app Qt

    gerenciador = Gerenciador()
    try:
        tela_principal = TelaPrincipal()
        tela_principal.show()  # mostra a janela principal

        sys.exit(app.exec())  # inicia o loop da aplicação
    finally:
        gerenciador.desconectar()

if __name__ == "__main__":
    main()
