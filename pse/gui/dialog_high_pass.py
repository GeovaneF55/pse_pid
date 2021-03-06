""" Bibliotecas externas. """
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QComboBox,
                             QDialogButtonBox,
                             QDialog,
                             QHBoxLayout,
                             QLabel,
                             QRadioButton,
                             QSizePolicy,
                             QSpacerItem,
                             QVBoxLayout,
                             QWidget)


""" Biliotecas locais. """
from algorithm.filter import (high_pass)
from gui.spinbox import DoubleTextSpinBox

class DialogHighPass(QDialog):
    def __init__(self, parent = None):
        super(DialogHighPass, self).__init__(parent)

        self.selectedKey = high_pass.Filter.GAUSSIAN_LAPLACE
        self.selectedFilter = {'filter': self.selectedKey,
                               'opt': None}
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.initUI()


    def initUI(self):
        """ Cria todos os componentes referentes as transformações. """

        self.setWindowTitle('Filtros Passa-Alta')

        # Filtros (F).
        self.labels = {}
        self.labels[high_pass.Filter.GAUSSIAN_LAPLACE] = \
            QLabel('Laplaciano do Gaussiano')
        self.labels[high_pass.Filter.LAPLACE] = QLabel('Laplaciano')
        self.labels[high_pass.Filter.PREWITT] = QLabel('Prewitt')
        self.labels[high_pass.Filter.SOBEL] = QLabel('Sobel')
        self.labels[high_pass.Filter.ROBERTS] = QLabel('Roberts')
        
        labelsLayout = QVBoxLayout()
        labelsLayout.setContentsMargins(0, 0, 0, 0)
        for key, label in self.labels.items():
            if key != high_pass.Filter.GAUSSIAN_LAPLACE:
                label.setEnabled(False)
                
            labelsLayout.addWidget(label)

        labelsWidget = QWidget()
        labelsWidget.setLayout(labelsLayout)

        # Máscaras(M).
        self.opts = {}
        
        # M: Passa-Alta
        self.opts[high_pass.Filter.GAUSSIAN_LAPLACE] = DoubleTextSpinBox()
        self.opts[high_pass.Filter.GAUSSIAN_LAPLACE].setSingleStep(0.5)
        self.opts[high_pass.Filter.GAUSSIAN_LAPLACE].setRange(0, 11)
                
        optsLayout = QVBoxLayout()
        optsLayout.setContentsMargins(0, 0, 0, 0)
        for key, opt in self.opts.items():
            if key != high_pass.Filter.GAUSSIAN_LAPLACE:
                opt.setEnabled(False)
                
            optsLayout.addWidget(opt)

        for _ in range(4):
            optsLayout.addItem(
                QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)
            )
            
        optsWidget = QWidget()
        optsWidget.setLayout(optsLayout)

        # Seleção do Filtro (S).
        self.radioButtons = {}
        
        # S: Passa-Alta
        self.radioButtons[high_pass.Filter.GAUSSIAN_LAPLACE] = QRadioButton()
        self.radioButtons[high_pass.Filter.GAUSSIAN_LAPLACE].setChecked(True)
        self.radioButtons[high_pass.Filter.GAUSSIAN_LAPLACE]. \
            clicked.connect(lambda: self.selectFilter(high_pass.Filter.
                                                      GAUSSIAN_LAPLACE))

        self.radioButtons[high_pass.Filter.LAPLACE] = QRadioButton()
        self.radioButtons[high_pass.Filter.LAPLACE].setChecked(False)
        self.radioButtons[high_pass.Filter.LAPLACE]. \
            clicked.connect(lambda: self.selectFilter(high_pass.Filter.LAPLACE))
        
        self.radioButtons[high_pass.Filter.PREWITT] = QRadioButton()
        self.radioButtons[high_pass.Filter.PREWITT].setChecked(False)
        self.radioButtons[high_pass.Filter.PREWITT]. \
            clicked.connect(lambda: self.selectFilter(high_pass.Filter.PREWITT))
        
        self.radioButtons[high_pass.Filter.SOBEL] = QRadioButton()
        self.radioButtons[high_pass.Filter.SOBEL].setChecked(False)
        self.radioButtons[high_pass.Filter.SOBEL]. \
            clicked.connect(lambda: self.selectFilter(high_pass.Filter.SOBEL))

        self.radioButtons[high_pass.Filter.ROBERTS] = QRadioButton()
        self.radioButtons[high_pass.Filter.ROBERTS].setChecked(False)
        self.radioButtons[high_pass.Filter.ROBERTS]. \
            clicked.connect(lambda: self.selectFilter(high_pass.Filter.ROBERTS))
        
        radioButtonsLayout = QVBoxLayout()
        radioButtonsLayout.setContentsMargins(0, 0, 0, 0)
        for key, button in self.radioButtons.items():
            radioButtonsLayout.addWidget(button)
            
        radioButtonsWidget = QWidget()
        radioButtonsWidget.setLayout(radioButtonsLayout)
        
        # Layout.
        sublayout = QHBoxLayout()
        sublayout.addWidget(labelsWidget)
        sublayout.addWidget(optsWidget)
        sublayout.addWidget(radioButtonsWidget)

        # Botões de OK e Cancel.
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.getFilter)
        buttons.rejected.connect(self.reject)

        subwidget = QWidget()
        subwidget.setLayout(sublayout)

        # Layout principal.
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(subwidget)
        mainLayout.addWidget(buttons)
        
        self.setLayout(mainLayout)


    def getFilter(self):
        opt = None
        if self.selectedKey in self.opts:
            opt = self.opts[self.selectedKey].currentText()
            
        self.selectedFilter = {'filter': self.selectedKey,
                               'opt': opt}

        return self.accept()
    
    
    def selectFilter(self, selectedKey):
        """ Seta as configurações do filtro selecionado."""
        
        for key, _ in self.radioButtons.items():
            selected = key == selectedKey
            self.labels[key].setEnabled(selected)

            if key in self.opts:
                self.opts[key].setEnabled(selected)

        self.selectedKey = selectedKey

        
    @staticmethod
    def getResults(parent = None):
        """ Método estático que cria o dialog e retorna uma tupla contendo:
        1- dicionário com as configurações do filtro selecionado
        2- dialog aceito/cancelado
        """

        dialog = DialogHighPass(parent)
        result = dialog.exec_()

        return (dialog.selectedFilter, result)
