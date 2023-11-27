"""Script da interface do tradutor"""

from PyQt5.QtCore import Qt, pyqtSlot
from deep_translator import GoogleTranslator
from PyQt5.QtWidgets import QDialog, QGridLayout, QComboBox, QPlainTextEdit, QPushButton


class TranslatorInterface(QDialog):
    """Interface do tradutor"""

    # Atributo que define o visual da tela
    _VISUAL = """
        /*Estilo padrão de todos os widgets*/
        QWidget {
            font: 20px;
        }
        
        /*Estilo dos campos de texto*/
        QPlainTextEdit {
            margin-top: 5px;
            margin-bottom: 15px;
        }
        
        /*Estilo do botão*/
        QPushButton {
            margin-bottom: 20px;
            padding: 15px;
        }
    """

    def __init__(self):
        """Inicializa e configura a instância de TranslatorInterface"""

        # Chama o construtor da classe pai (QDialog) para inicializar a instância e Define o tamnho fixo da janela
        super().__init__()
        self.setFixedSize(680, 490)

        # Adciona um título a interface e remove da barra de título o help button
        self.setWindowTitle('Translator')
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        # Aplica um estilo na tela
        self.setStyleSheet(self._VISUAL)

        # Atributo que define as linguas dos comboboxes
        self._currentLanguages = ['', '']

        # Chama a função _initComponents() para estanciar os widgets na tela
        self._initComponents()

    def _initComponents(self):
        """Função que istancia todos os widgets na tela"""

        # Cria e aplica na tela um layout grid
        grid = QGridLayout()
        self.setLayout(grid)

        # Define os ComboBoxes
        self._comboboxSource = QComboBox()  # Combobox do idioma fonte
        self._comboboxTarget = QComboBox()  # Combobox do idioma alvo

        # Adciona aos comboboxes os idiomas suportadados pelo Google Translator
        for langueges, id_langueges in GoogleTranslator().get_supported_languages(True).items():
            self._comboboxSource.addItem(langueges.capitalize(), id_langueges)
            self._comboboxTarget.addItem(langueges.capitalize(), id_langueges)

        # Define a configuração padrão dos idiomas selecionados
        self._comboboxSource.setCurrentText('Portuguese')
        self._comboboxTarget.setCurrentText('English')

        # Atribui as línguas selecionadas em _currentLanguages
        self._currentLanguages = [self._comboboxSource.currentText(), self._comboboxTarget.currentText()]

        # Conecta o método _changeLanguage() aos comboboxes
        self._comboboxSource.currentTextChanged.connect(self._changeLanguage)
        self._comboboxTarget.currentTextChanged.connect(self._changeLanguage)

        # Cria um campo de entrada para digitar o texto que será traduzido
        self._inputTextSource = QPlainTextEdit()
        self._inputTextSource.setPlaceholderText('Enter text')

        # Define o campo de entrada que terá a tradução
        self._inputTranslation = QPlainTextEdit()
        self._inputTranslation.setPlaceholderText('Translation')
        self._inputTranslation.setReadOnly(True)
        self._inputTranslation.viewport().setCursor(Qt.ArrowCursor)

        # Cria o botão de traduzir o texto
        button_translator = QPushButton('Translate')
        button_translator.setCursor(Qt.PointingHandCursor)
        button_translator.clicked.connect(self._translate)

        # Aplica os widgets à grid
        grid.addWidget(self._comboboxSource, 0, 0)
        grid.addWidget(self._comboboxTarget, 0, 2)
        grid.addWidget(self._inputTextSource, 1, 0)
        grid.addWidget(self._inputTranslation, 1, 2)
        grid.addWidget(button_translator, 2, 1,  alignment=Qt.AlignCenter)

    @pyqtSlot()
    def _changeLanguage(self):
        """Método responsável por alterar o idioma selecionado nos comboboxes e evitar a duplicação deles"""

        # Variável que define o combobox inverso do que foi selecionado
        combobox_inverse = self._comboboxTarget if self.sender() is self._comboboxSource else self._comboboxSource

        # Se os IDs dos comboboxes forem iguais, muda o texto do combobox_inverse para o original do combobox acionado
        if self._comboboxSource.currentData() == self._comboboxTarget.currentData():
            combobox_inverse.setCurrentText(self._currentLanguages[0 if self.sender() is self._comboboxSource else 1])

        # limpa a entrada de tradução
        self._inputTranslation.setPlainText('')

        # Redefine o atributo _currentLanguages com as aterações feitas
        self._currentLanguages = [self._comboboxSource.currentText(), self._comboboxTarget.currentText()]

    @pyqtSlot()
    def _translate(self):
        """Metódo responsável por fazer a tradução"""

        # Define as línguas selecionadas
        language_source, language_target = self._comboboxSource.currentData(), self._comboboxTarget.currentData()

        # Estabelece a tradução e a posiciona no _inputTranslation
        translation = GoogleTranslator(language_source, language_target).translate(self._inputTextSource.toPlainText())
        self._inputTranslation.setPlainText(translation)
