"""Script de execução do projeto"""

import sys
from PyQt5.QtWidgets import QApplication
from interface import TranslatorInterface

if __name__ == '__main__':
    # Cria uma aplicação Qt
    application = QApplication(sys.argv)

    # Cria uma instância da MainScreen e a exibe
    main_screen = TranslatorInterface()
    main_screen.show()

    # Inicia o loop de execução da aplicação
    sys.exit(application.exec_())
