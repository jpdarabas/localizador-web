styles = """
    /* Estilo geral */
    QMainWindow {
        background-color: #f5f5f5;
        font-family: 'Segoe UI', Arial, sans-serif;
    }
    
    /* Cabeçalho */
    QPushButton {
        padding: 10px;
        font-size: 14px;
        min-width: 100px;
        border: none;
        background-color: #e0e0e0;
    }
    
    QPushButton:hover {
        background-color: #d0d0d0;
    }
    
    QPushButton:checked {
        background-color: #a0a0a0;
        font-weight: bold;
    }
    
    /* Tabelas */
    QTableView {
        gridline-color: #ccc;
        font-size: 12px;
    }
    
    QHeaderView::section {
        background-color: #e0e0e0;
        padding: 5px;
    }
    
    /* Inputs */
    QLineEdit, QComboBox {
        padding: 5px;
        border: 1px solid #ccc;
        border-radius: 3px;
    }

    QLabel {
        font-size: 14px;
        max-width: 240px;
        qproperty-wordWrap: true;
    }
    
    QMessageBox QLabel {
        font-size: 14px;
        qproperty-wordWrap: true;
    }

    QVBoxLayout {
        spacing: 10px;
        margin: 10px;
        padding: 2px;
        alignment: left | top; 

    }
"""