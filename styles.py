"""
styles.py - Стили и темы оформления приложения
Содержит CSS-подобные стили для PyQt6 с поддержкой светлой и тёмной темы
"""


class AppStyles:
    """Класс со всеми стилями приложения"""

    # Светлая тема
    LIGHT_THEME = """
        QMainWindow {
            background-color: #f5f5f5;
        }

        QTabWidget::pane {
            border: 1px solid #cccccc;
            background: white;
            border-radius: 4px;
        }

        QTabBar::tab {
            background: #e0e0e0;
            color: #333333;
            padding: 8px 16px;
            margin-right: 2px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }

        QTabBar::tab:selected {
            background: white;
            border-bottom: 2px solid #4CAF50;
        }

        QTabBar::tab:hover {
            background: #d0d0d0;
        }

        QTextEdit {
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 11pt;
            border: 1px solid #cccccc;
            border-radius: 4px;
            padding: 4px;
            background: white;
            color: #333333;
        }

        QTextEdit:focus {
            border: 1px solid #4CAF50;
        }

        QTextEdit:disabled, QTextEdit[readOnly="true"] {
            background: #f5f5f5;
            color: #555555;
        }

        QPushButton {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 10pt;
        }

        QPushButton:hover {
            background: #45a049;
        }

        QPushButton:pressed {
            background: #3d8b40;
        }

        QPushButton:disabled {
            background: #cccccc;
            color: #666666;
        }

        QTreeWidget {
            border: 1px solid #cccccc;
            border-radius: 4px;
            alternate-background-color: #f9f9f9;
            color: #333333;
        }

        QTreeWidget::item {
            padding: 4px;
        }

        QTreeWidget::item:selected {
            background: #4CAF50;
            color: white;
        }

        QHeaderView::section {
            background: #e0e0e0;
            padding: 6px;
            border: 1px solid #cccccc;
            font-weight: bold;
            color: #333333;
        }

        QFrame {
            border-radius: 4px;
        }

        QLabel {
            font-size: 10pt;
            padding: 4px;
            color: #333333;
        }

        QGroupBox {
            font-weight: bold;
            border: 1px solid #cccccc;
            border-radius: 4px;
            margin-top: 10px;
            padding-top: 10px;
            color: #333333;
        }

        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }

        QScrollBar:vertical {
            border: none;
            background: #f0f0f0;
            width: 10px;
            margin: 0px;
        }

        QScrollBar::handle:vertical {
            background: #cccccc;
            min-height: 20px;
            border-radius: 5px;
        }

        QScrollBar::handle:vertical:hover {
            background: #aaaaaa;
        }

        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }

        QMessageBox {
            background-color: white;
        }

        QMessageBox QPushButton {
            min-width: 80px;
        }

        QInputDialog {
            background-color: white;
        }

        QFileDialog {
            background-color: white;
        }

        QMenuBar {
            background: #f0f0f0;
            color: #333333;
        }

        QMenuBar::item:selected {
            background: #4CAF50;
            color: white;
        }

        QMenu {
            background: white;
            color: #333333;
        }

        QMenu::item:selected {
            background: #4CAF50;
            color: white;
        }
    """

    # Тёмная тема
    DARK_THEME = """
        QMainWindow {
            background-color: #1e1e1e;
        }

        QTabWidget::pane {
            border: 1px solid #3c3c3c;
            background: #2d2d2d;
            border-radius: 4px;
        }

        QTabBar::tab {
            background: #3c3c3c;
            color: #cccccc;
            padding: 8px 16px;
            margin-right: 2px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }

        QTabBar::tab:selected {
            background: #2d2d2d;
            border-bottom: 2px solid #4CAF50;
            color: white;
        }

        QTabBar::tab:hover {
            background: #4a4a4a;
        }

        QTextEdit {
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 11pt;
            border: 1px solid #3c3c3c;
            border-radius: 4px;
            padding: 4px;
            background: #252525;
            color: #e0e0e0;
        }

        QTextEdit:focus {
            border: 1px solid #4CAF50;
        }

        QTextEdit:disabled, QTextEdit[readOnly="true"] {
            background: #1e1e1e;
            color: #aaaaaa;
        }

        QPushButton {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 10pt;
        }

        QPushButton:hover {
            background: #45a049;
        }

        QPushButton:pressed {
            background: #3d8b40;
        }

        QPushButton:disabled {
            background: #3c3c3c;
            color: #666666;
        }

        QTreeWidget {
            border: 1px solid #3c3c3c;
            border-radius: 4px;
            alternate-background-color: #2a2a2a;
            color: #e0e0e0;
            background: #252525;
        }

        QTreeWidget::item {
            padding: 4px;
        }

        QTreeWidget::item:selected {
            background: #4CAF50;
            color: white;
        }

        QHeaderView::section {
            background: #3c3c3c;
            padding: 6px;
            border: 1px solid #4a4a4a;
            font-weight: bold;
            color: #e0e0e0;
        }

        QFrame {
            border-radius: 4px;
        }

        QLabel {
            font-size: 10pt;
            padding: 4px;
            color: #e0e0e0;
        }

        QGroupBox {
            font-weight: bold;
            border: 1px solid #3c3c3c;
            border-radius: 4px;
            margin-top: 10px;
            padding-top: 10px;
            color: #e0e0e0;
        }

        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }

        QScrollBar:vertical {
            border: none;
            background: #2d2d2d;
            width: 10px;
            margin: 0px;
        }

        QScrollBar::handle:vertical {
            background: #4a4a4a;
            min-height: 20px;
            border-radius: 5px;
        }

        QScrollBar::handle:vertical:hover {
            background: #5a5a5a;
        }

        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }

        QMessageBox {
            background-color: #2d2d2d;
            color: #e0e0e0;
        }

        QMessageBox QPushButton {
            min-width: 80px;
        }

        QInputDialog {
            background-color: #2d2d2d;
            color: #e0e0e0;
        }

        QFileDialog {
            background-color: #2d2d2d;
            color: #e0e0e0;
        }

        QMenuBar {
            background: #2d2d2d;
            color: #e0e0e0;
        }

        QMenuBar::item:selected {
            background: #4CAF50;
            color: white;
        }

        QMenu {
            background: #2d2d2d;
            color: #e0e0e0;
        }

        QMenu::item:selected {
            background: #4CAF50;
            color: white;
        }

        QComboBox {
            background: #252525;
            color: #e0e0e0;
            border: 1px solid #3c3c3c;
            padding: 4px;
            border-radius: 4px;
        }

        QComboBox::drop-down {
            border: none;
        }

        QComboBox QAbstractItemView {
            background: #252525;
            color: #e0e0e0;
        }

        QScrollArea {
            background: #1e1e1e;
        }
    """

    # Стиль для кнопок с иконками (светлая тема)
    ICON_BUTTON_STYLE_LIGHT = """
        QPushButton {
            background: #2196F3;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 10pt;
        }

        QPushButton:hover {
            background: #1976D2;
        }

        QPushButton:pressed {
            background: #0D47A1;
        }
    """

    # Стиль для кнопок с иконками (тёмная тема)
    ICON_BUTTON_STYLE_DARK = """
        QPushButton {
            background: #2196F3;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 10pt;
        }

        QPushButton:hover {
            background: #1976D2;
        }

        QPushButton:pressed {
            background: #0D47A1;
        }
    """

    # Стиль для предупреждающих кнопок (светлая тема)
    WARNING_BUTTON_STYLE_LIGHT = """
        QPushButton {
            background: #FF9800;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 10pt;
        }

        QPushButton:hover {
            background: #F57C00;
        }

        QPushButton:pressed {
            background: #E65100;
        }
    """

    # Стиль для предупреждающих кнопок (тёмная тема)
    WARNING_BUTTON_STYLE_DARK = """
        QPushButton {
            background: #FF9800;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 10pt;
        }

        QPushButton:hover {
            background: #F57C00;
        }

        QPushButton:pressed {
            background: #E65100;
        }
    """

    @staticmethod
    def get_theme(theme_name="light"):
        """Возвращает стиль для выбранной темы"""
        if theme_name == "dark":
            return AppStyles.DARK_THEME
        return AppStyles.LIGHT_THEME

    @staticmethod
    def get_icon_button_style(theme_name="light"):
        """Возвращает стиль для иконок в зависимости от темы"""
        if theme_name == "dark":
            return AppStyles.ICON_BUTTON_STYLE_DARK
        return AppStyles.ICON_BUTTON_STYLE_LIGHT

    @staticmethod
    def get_warning_button_style(theme_name="light"):
        """Возвращает стиль для предупреждающих кнопок в зависимости от темы"""
        if theme_name == "dark":
            return AppStyles.WARNING_BUTTON_STYLE_DARK
        return AppStyles.WARNING_BUTTON_STYLE_LIGHT