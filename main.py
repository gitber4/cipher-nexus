"""
main.py - Главный файл приложения Cipher Nexus V3.1
Содержит GUI интерфейс на PyQt6 с поддержкой конфигурации
"""

import sys
import json
import os
import configparser
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTextEdit, QPushButton, QTreeWidget, QTreeWidgetItem, QHeaderView,
    QMessageBox, QInputDialog, QFileDialog, QFrame, QComboBox, QCheckBox,
    QListWidget, QListWidgetItem, QSplitter, QGroupBox
)
from PyQt6.QtCore import Qt, pyqtSignal

# Импорт наших модулей
from cipher_core import CipherNexus
from texts import AppTexts
from styles import AppStyles


class ConfigManager:
    """Менеджер конфигурации приложения"""
    
    def __init__(self):
        if hasattr(sys, '_MEIPASS'):
            self.exe_dir = os.path.dirname(sys.executable)
        else:
            self.exe_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.config_path = os.path.join(self.exe_dir, "config.ini")
        self.config = configparser.ConfigParser()
        self.load_config()
    
    def load_config(self):
        if not os.path.exists(self.config_path):
            self.create_default_config()
        
        self.config.read(self.config_path, encoding='utf-8')
        
        if 'SETTINGS' not in self.config:
            self.config['SETTINGS'] = {}
        if 'HISTORY' not in self.config:
            self.config['HISTORY'] = {}
        if 'DICTIONARIES' not in self.config:
            self.config['DICTIONARIES'] = {}
        
        self.save_config()
    
    def create_default_config(self):
        self.config['SETTINGS'] = {
            'theme': 'light',
            'save_history': 'true',
            'save_dictionaries': 'true',
            'max_history_items': '50',
            'max_dictionaries': '10'
        }
        self.config['HISTORY'] = {'items': '[]'}
        self.config['DICTIONARIES'] = {'items': '[]'}
        self.save_config()
    
    def save_config(self):
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                self.config.write(f)
        except Exception as e:
            print(f"Ошибка сохранения конфигурации: {e}")
    
    def get_setting(self, key, default=None):
        try:
            return self.config['SETTINGS'].get(key, default)
        except:
            return default
    
    def set_setting(self, key, value):
        if 'SETTINGS' not in self.config:
            self.config['SETTINGS'] = {}
        self.config['SETTINGS'][key] = str(value)
        self.save_config()
    
    def get_history(self):
        try:
            items_str = self.config['HISTORY'].get('items', '[]')
            return json.loads(items_str)
        except:
            return []
    
    def add_history_item(self, original, encoded, direction='encode'):
        if self.get_setting('save_history', 'true') != 'true':
            return
        
        history = self.get_history()
        max_items = int(self.get_setting('max_history_items', '50'))
        
        item = {
            'timestamp': datetime.now().isoformat(),
            'original': original[:200],
            'encoded': encoded[:200],
            'direction': direction
        }
        
        history.insert(0, item)
        
        if len(history) > max_items:
            history = history[:max_items]
        
        self.config['HISTORY']['items'] = json.dumps(history, ensure_ascii=False)
        self.save_config()
    
    def clear_history(self):
        self.config['HISTORY']['items'] = '[]'
        self.save_config()
    
    def get_dictionaries(self):
        try:
            items_str = self.config['DICTIONARIES'].get('items', '[]')
            return json.loads(items_str)
        except:
            return []
    
    def add_dictionary(self, name, dictionary_data):
        if self.get_setting('save_dictionaries', 'true') != 'true':
            return
        
        dicts = self.get_dictionaries()
        max_items = int(self.get_setting('max_dictionaries', '10'))
        
        for i, d in enumerate(dicts):
            if d['name'] == name:
                dicts.pop(i)
                break
        
        item = {
            'name': name,
            'timestamp': datetime.now().isoformat(),
            'data': dictionary_data
        }
        
        dicts.insert(0, item)
        
        if len(dicts) > max_items:
            dicts = dicts[:max_items]
        
        self.config['DICTIONARIES']['items'] = json.dumps(dicts, ensure_ascii=False)
        self.save_config()
    
    def remove_dictionary(self, index):
        dicts = self.get_dictionaries()
        if 0 <= index < len(dicts):
            dicts.pop(index)
            self.config['DICTIONARIES']['items'] = json.dumps(dicts, ensure_ascii=False)
            self.save_config()
            return True
        return False
    
    def clear_dictionaries(self):
        self.config['DICTIONARIES']['items'] = '[]'
        self.save_config()


class MainWindow(QMainWindow):
    """Главное окно приложения"""
    
    history_changed = pyqtSignal()
    dictionaries_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.texts = AppTexts()
        self.cipher = CipherNexus()
        self.config = ConfigManager()
        self.current_theme = self.config.get_setting('theme', 'light')
        
        self.setWindowTitle(f"{self.texts.APP_NAME} v{self.texts.VERSION} — НЕВЗЛАМЫВАЕМОЕ ШИФРОВАНИЕ")
        self.setMinimumSize(1100, 800)
        
        self.apply_theme(self.current_theme)
        
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        self.tab_encode = QWidget()
        self.tab_dict = QWidget()
        self.tab_settings = QWidget()
        self.tab_readme = QWidget()
        self.tab_history = QWidget()
        self.tab_symbols = QWidget()
        
        self.tabs.addTab(self.tab_encode, self.texts.TAB_ENCODE)
        self.tabs.addTab(self.tab_dict, self.texts.TAB_DICT)
        self.tabs.addTab(self.tab_history, "📜 История")
        self.tabs.addTab(self.tab_symbols, self.texts.TAB_SYMBOLS)
        self.tabs.addTab(self.tab_settings, self.texts.TAB_SETTINGS)
        self.tabs.addTab(self.tab_readme, self.texts.TAB_README)
        
        self.init_encode_tab()
        self.init_dict_tab()
        self.init_history_tab()
        self.init_symbols_tab()
        self.init_settings_tab()
        self.init_readme_tab()
        
        self.history_changed.connect(self.refresh_history_list)
        self.dictionaries_changed.connect(self.refresh_dictionaries_list)
        
        self.refresh_history_list()
        self.refresh_dictionaries_list()
    
    def apply_theme(self, theme_name):
        self.current_theme = theme_name
        style = AppStyles.get_theme(theme_name)
        self.setStyleSheet(style)
        self.config.set_setting('theme', theme_name)
    
    def init_encode_tab(self):
        layout = QVBoxLayout(self.tab_encode)
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Блок кодирования
        group_enc = QFrame()
        group_enc.setFrameStyle(QFrame.Shape.StyledPanel)
        enc_layout = QVBoxLayout(group_enc)
        
        enc_layout.addWidget(QLabel(self.texts.ENCODE_TITLE))
        self.entry_text = QTextEdit()
        self.entry_text.setPlaceholderText(self.texts.ENCODE_PLACEHOLDER)
        self.entry_text.setMaximumHeight(120)
        enc_layout.addWidget(self.entry_text)
        
        btn_row_enc = QHBoxLayout()
        self.btn_encode = QPushButton(self.texts.ENCODE_BUTTON)
        self.btn_encode.clicked.connect(self.encode_action)
        btn_row_enc.addWidget(self.btn_encode)
        
        self.btn_copy_enc = QPushButton(self.texts.BUTTON_COPY)
        self.btn_copy_enc.clicked.connect(lambda: self.copy_text(self.encoded_text))
        btn_row_enc.addWidget(self.btn_copy_enc)
        
        self.btn_paste_enc = QPushButton(self.texts.BUTTON_PASTE)
        self.btn_paste_enc.clicked.connect(lambda: self.paste_text(self.entry_text))
        btn_row_enc.addWidget(self.btn_paste_enc)
        
        btn_row_enc.addStretch()
        enc_layout.addLayout(btn_row_enc)
        
        enc_layout.addWidget(QLabel(self.texts.ENCODE_RESULT))
        self.encoded_text = QTextEdit()
        self.encoded_text.setReadOnly(True)
        self.encoded_text.setMaximumHeight(80)
        enc_layout.addWidget(self.encoded_text)
        
        splitter.addWidget(group_enc)
        
        # Блок декодирования
        group_dec = QFrame()
        group_dec.setFrameStyle(QFrame.Shape.StyledPanel)
        dec_layout = QVBoxLayout(group_dec)
        
        dec_layout.addWidget(QLabel(self.texts.DECODE_TITLE))
        self.entry_encoded = QTextEdit()
        self.entry_encoded.setPlaceholderText(self.texts.DECODE_PLACEHOLDER)
        self.entry_encoded.setMaximumHeight(80)
        dec_layout.addWidget(self.entry_encoded)
        
        btn_row_dec = QHBoxLayout()
        self.btn_decode = QPushButton(self.texts.DECODE_BUTTON)
        self.btn_decode.clicked.connect(self.decode_action)
        btn_row_dec.addWidget(self.btn_decode)
        
        self.btn_copy_dec = QPushButton(self.texts.BUTTON_COPY)
        self.btn_copy_dec.clicked.connect(lambda: self.copy_text(self.decoded_text))
        btn_row_dec.addWidget(self.btn_copy_dec)
        
        self.btn_paste_dec = QPushButton(self.texts.BUTTON_PASTE)
        self.btn_paste_dec.clicked.connect(lambda: self.paste_text(self.entry_encoded))
        btn_row_dec.addWidget(self.btn_paste_dec)
        
        btn_row_dec.addStretch()
        dec_layout.addLayout(btn_row_dec)
        
        dec_layout.addWidget(QLabel(self.texts.DECODE_RESULT))
        self.decoded_text = QTextEdit()
        self.decoded_text.setReadOnly(True)
        self.decoded_text.setMaximumHeight(120)
        dec_layout.addWidget(self.decoded_text)
        
        splitter.addWidget(group_dec)
        splitter.setSizes([350, 350])
        layout.addWidget(splitter)
    
    def init_dict_tab(self):
        layout = QVBoxLayout(self.tab_dict)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.addWidget(QLabel("Текущий словарь:"))
        
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Символ", "Код"])
        self.tree.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.tree.header().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.tree.setAlternatingRowColors(True)
        left_layout.addWidget(self.tree)
        
        btn_row = QHBoxLayout()
        self.btn_export = QPushButton(self.texts.BUTTON_EXPORT)
        self.btn_export.clicked.connect(self.export_dict)
        btn_row.addWidget(self.btn_export)
        
        self.btn_import = QPushButton(self.texts.BUTTON_IMPORT)
        self.btn_import.clicked.connect(self.import_dict)
        btn_row.addWidget(self.btn_import)
        
        self.btn_regenerate = QPushButton(self.texts.BUTTON_REGENERATE)
        self.btn_regenerate.clicked.connect(self.regenerate_dict_dialog)
        btn_row.addWidget(self.btn_regenerate)
        
        self.btn_random = QPushButton(self.texts.BUTTON_RANDOM)
        self.btn_random.clicked.connect(self.random_seed)
        btn_row.addWidget(self.btn_random)
        
        btn_row.addStretch()
        left_layout.addLayout(btn_row)
        splitter.addWidget(left_widget)
        
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.addWidget(QLabel("Сохранённые словари:"))
        
        self.dicts_list = QListWidget()
        self.dicts_list.itemDoubleClicked.connect(self.load_dictionary_from_history)
        right_layout.addWidget(self.dicts_list)
        
        dict_btn_row = QHBoxLayout()
        self.btn_save_dict = QPushButton("💾 Сохранить текущий словарь")
        self.btn_save_dict.clicked.connect(self.save_current_dictionary)
        dict_btn_row.addWidget(self.btn_save_dict)
        
        self.btn_load_dict = QPushButton("📂 Загрузить выбранный")
        self.btn_load_dict.clicked.connect(self.load_dictionary_from_history)
        dict_btn_row.addWidget(self.btn_load_dict)
        
        self.btn_delete_dict = QPushButton("🗑️ Удалить выбранный")
        self.btn_delete_dict.clicked.connect(self.delete_dictionary)
        dict_btn_row.addWidget(self.btn_delete_dict)
        
        self.btn_clear_dicts = QPushButton("🧹 Очистить все")
        self.btn_clear_dicts.clicked.connect(self.clear_all_dictionaries)
        dict_btn_row.addWidget(self.btn_clear_dicts)
        
        dict_btn_row.addStretch()
        right_layout.addLayout(dict_btn_row)
        splitter.addWidget(right_widget)
        splitter.setSizes([600, 300])
        layout.addWidget(splitter)
        self.refresh_dict_tree()
    
    def init_history_tab(self):
        layout = QVBoxLayout(self.tab_history)
        info_label = QLabel("📜 История переводов (сохраняются последние 50 записей)")
        layout.addWidget(info_label)
        self.history_list = QListWidget()
        self.history_list.itemDoubleClicked.connect(self.load_from_history)
        layout.addWidget(self.history_list)
        btn_row = QHBoxLayout()
        self.btn_load_history = QPushButton("📂 Загрузить выбранный")
        self.btn_load_history.clicked.connect(self.load_from_history)
        btn_row.addWidget(self.btn_load_history)
        self.btn_clear_history = QPushButton("🧹 Очистить историю")
        self.btn_clear_history.clicked.connect(self.clear_history)
        btn_row.addWidget(self.btn_clear_history)
        btn_row.addStretch()
        layout.addLayout(btn_row)
    
    def init_symbols_tab(self):
        layout = QVBoxLayout(self.tab_symbols)
        
        stats = self.cipher.get_stats()
        info_label = QLabel(
            f"🔢 Всего символов: {stats['total_letters']} | "
            f"📊 Всего кодов: {stats['total_codes']} | "
            f"🎯 Свободно: {stats['free_codes']} комбинаций"
        )
        info_label.setStyleSheet("font-weight: bold; font-size: 13pt; padding: 15px; background: #4CAF50; color: white; border-radius: 8px;")
        layout.addWidget(info_label)
        
        symbols = self.cipher.get_all_symbols()
        
        groups = [
            ("🇷🇺 Русские (строчные)", symbols['letters_ru_lower']),
            ("🇷🇺 Русские (заглавные)", symbols['letters_ru_upper']),
            ("🇬🇧 Английские (строчные)", symbols['letters_en_lower']),
            ("🇬🇧 Английские (заглавные)", symbols['letters_en_upper']),
            ("🔢 Цифры (включая 0!)", symbols['digits']),
            ("🔣 Специальные символы", symbols['specials']),
            ("❓ Знаки препинания", symbols['punctuation'])
        ]
        
        for group_name, chars in groups:
            group = QGroupBox(group_name)
            group_layout = QVBoxLayout(group)
            
            chars_display = ' '.join(chars)
            label = QLabel(chars_display)
            label.setStyleSheet("font-size: 14pt; font-family: 'Consolas', monospace; padding: 8px;")
            label.setWordWrap(True)
            group_layout.addWidget(label)
            
            count_label = QLabel(f"Всего: {len(chars)} символов")
            count_label.setStyleSheet("color: #888888; font-size: 9pt;")
            group_layout.addWidget(count_label)
            layout.addWidget(group)
        
        layout.addStretch()
    
    def init_settings_tab(self):
        layout = QVBoxLayout(self.tab_settings)
        
        info_group = QGroupBox("📊 Информация о шифровании")
        info_layout = QVBoxLayout(info_group)
        stats = self.cipher.get_stats()
        
        self.seed_label = QLabel(self.texts.SETTINGS_SEED.format(self.texts.SETTINGS_SEED_RANDOM))
        info_layout.addWidget(self.seed_label)
        self.letters_count = QLabel(self.texts.SETTINGS_LETTERS.format(stats['total_letters']))
        info_layout.addWidget(self.letters_count)
        self.code_length = QLabel(self.texts.SETTINGS_CODE_LENGTH.format(stats['code_length']))
        info_layout.addWidget(self.code_length)
        self.total_codes = QLabel(self.texts.SETTINGS_TOTAL_CODES.format(stats['total_codes']))
        info_layout.addWidget(self.total_codes)
        self.free_codes = QLabel(self.texts.SETTINGS_FREE_CODES.format(stats['free_codes']))
        info_layout.addWidget(self.free_codes)
        self.separator_label = QLabel(self.texts.SETTINGS_SEPARATOR.format(stats['separator']))
        info_layout.addWidget(self.separator_label)
        layout.addWidget(info_group)
        
        theme_group = QGroupBox("🎨 Оформление")
        theme_layout = QVBoxLayout(theme_group)
        theme_row = QHBoxLayout()
        theme_row.addWidget(QLabel("Тема:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItem("☀️ Светлая", "light")
        self.theme_combo.addItem("🌙 Тёмная", "dark")
        self.theme_combo.currentIndexChanged.connect(self.change_theme)
        theme_index = 0 if self.current_theme == "light" else 1
        self.theme_combo.setCurrentIndex(theme_index)
        theme_row.addWidget(self.theme_combo)
        theme_row.addStretch()
        theme_layout.addLayout(theme_row)
        layout.addWidget(theme_group)
        
        history_group = QGroupBox("📜 История")
        history_layout = QVBoxLayout(history_group)
        self.save_history_check = QCheckBox("Сохранять историю переводов")
        self.save_history_check.setChecked(self.config.get_setting('save_history', 'true') == 'true')
        self.save_history_check.toggled.connect(self.toggle_history)
        history_layout.addWidget(self.save_history_check)
        self.save_dicts_check = QCheckBox("Сохранять историю словарей")
        self.save_dicts_check.setChecked(self.config.get_setting('save_dictionaries', 'true') == 'true')
        self.save_dicts_check.toggled.connect(self.toggle_dictionaries)
        history_layout.addWidget(self.save_dicts_check)
        limit_row = QHBoxLayout()
        limit_row.addWidget(QLabel("Максимум записей в истории:"))
        self.history_limit_spin = QComboBox()
        for i in [10, 20, 50, 100, 200]:
            self.history_limit_spin.addItem(str(i), i)
        current_limit = int(self.config.get_setting('max_history_items', '50'))
        self.history_limit_spin.setCurrentIndex([10, 20, 50, 100, 200].index(current_limit))
        self.history_limit_spin.currentIndexChanged.connect(self.change_history_limit)
        limit_row.addWidget(self.history_limit_spin)
        limit_row.addStretch()
        history_layout.addLayout(limit_row)
        layout.addWidget(history_group)
        
        self.btn_copy_dict = QPushButton(self.texts.BUTTON_COPY_DICT)
        self.btn_copy_dict.clicked.connect(self.copy_dict_json)
        layout.addWidget(self.btn_copy_dict)
        
        config_label = QLabel(f"📁 Файл конфигурации: {self.config.config_path}")
        config_label.setWordWrap(True)
        config_label.setStyleSheet("color: #888888; font-size: 9pt;")
        layout.addWidget(config_label)
        layout.addStretch()
    
    def init_readme_tab(self):
        layout = QVBoxLayout(self.tab_readme)
        readme_text = QTextEdit()
        readme_text.setReadOnly(True)
        readme_text.setHtml(self.texts.get_readme())
        layout.addWidget(readme_text)
    
    def change_theme(self, index):
        theme = self.theme_combo.currentData()
        self.apply_theme(theme)
        theme_name = "Светлая" if theme == "light" else "Тёмная"
        QMessageBox.information(self, self.texts.MSG_SUCCESS, self.texts.MSG_THEME_CHANGED.format(theme_name))
    
    def toggle_history(self, checked):
        self.config.set_setting('save_history', 'true' if checked else 'false')
        if not checked:
            reply = QMessageBox.question(self, "Очистка истории", "Хотите очистить существующую историю?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.config.clear_history()
                self.history_changed.emit()
    
    def toggle_dictionaries(self, checked):
        self.config.set_setting('save_dictionaries', 'true' if checked else 'false')
        if not checked:
            reply = QMessageBox.question(self, "Очистка словарей", "Хотите очистить сохранённые словари?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.config.clear_dictionaries()
                self.dictionaries_changed.emit()
    
    def change_history_limit(self, index):
        limit = self.history_limit_spin.currentData()
        self.config.set_setting('max_history_items', str(limit))
    
    def refresh_history_list(self):
        self.history_list.clear()
        history = self.config.get_history()
        for i, item in enumerate(history):
            timestamp = datetime.fromisoformat(item['timestamp']).strftime('%H:%M:%S')
            direction = "🔒→" if item['direction'] == 'encode' else "🔓→"
            original = item['original'][:30] + "..." if len(item['original']) > 30 else item['original']
            text = f"{timestamp} {direction} {original}"
            self.history_list.addItem(text)
    
    def refresh_dictionaries_list(self):
        self.dicts_list.clear()
        dicts = self.config.get_dictionaries()
        for i, item in enumerate(dicts):
            timestamp = datetime.fromisoformat(item['timestamp']).strftime('%d.%m.%Y %H:%M')
            text = f"{timestamp} - {item['name']}"
            self.dicts_list.addItem(text)
    
    def save_current_dictionary(self):
        name, ok = QInputDialog.getText(self, "Сохранить словарь", "Введите название словаря:")
        if ok and name:
            self.config.add_dictionary(name, self.cipher.letter_to_code)
            self.dictionaries_changed.emit()
            QMessageBox.information(self, self.texts.MSG_SUCCESS, f"Словарь '{name}' сохранён.")
    
    def load_dictionary_from_history(self):
        current_row = self.dicts_list.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, self.texts.MSG_WARNING, "Выберите словарь для загрузки.")
            return
        dicts = self.config.get_dictionaries()
        if current_row < len(dicts):
            dict_data = dicts[current_row]['data']
            if self.cipher.load_dict(dict_data):
                self.refresh_dict_tree()
                self.seed_label.setText(self.texts.SETTINGS_SEED.format(self.texts.SETTINGS_SEED_IMPORTED))
                QMessageBox.information(self, self.texts.MSG_SUCCESS, f"Словарь '{dicts[current_row]['name']}' загружен.")
            else:
                QMessageBox.critical(self, self.texts.MSG_ERROR, self.texts.MSG_DICT_INVALID)
    
    def delete_dictionary(self):
        current_row = self.dicts_list.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, self.texts.MSG_WARNING, "Выберите словарь для удаления.")
            return
        dicts = self.config.get_dictionaries()
        if current_row < len(dicts):
            name = dicts[current_row]['name']
            reply = QMessageBox.question(self, "Удаление словаря", f"Удалить словарь '{name}'?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.config.remove_dictionary(current_row)
                self.dictionaries_changed.emit()
    
    def clear_all_dictionaries(self):
        reply = QMessageBox.question(self, "Очистка словарей", "Удалить все сохранённые словари?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.config.clear_dictionaries()
            self.dictionaries_changed.emit()
    
    def load_from_history(self):
        current_row = self.history_list.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, self.texts.MSG_WARNING, "Выберите запись из истории.")
            return
        history = self.config.get_history()
        if current_row < len(history):
            item = history[current_row]
            if item['direction'] == 'encode':
                self.entry_text.setText(item['original'])
                self.encoded_text.setText(item['encoded'])
            else:
                self.entry_encoded.setText(item['encoded'])
                self.decoded_text.setText(item['original'])
            self.tabs.setCurrentIndex(0)
    
    def clear_history(self):
        reply = QMessageBox.question(self, "Очистка истории", "Удалить всю историю переводов?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.config.clear_history()
            self.history_changed.emit()
    
    def copy_text(self, text_edit):
        content = text_edit.toPlainText().strip()
        if content:
            clipboard = QApplication.clipboard()
            clipboard.setText(content)
            QMessageBox.information(self, self.texts.MSG_SUCCESS, self.texts.MSG_TEXT_COPIED)
        else:
            QMessageBox.warning(self, self.texts.MSG_WARNING, self.texts.MSG_NO_TEXT)
    
    def paste_text(self, text_edit):
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        if text:
            text_edit.setText(text)
        else:
            QMessageBox.warning(self, self.texts.MSG_ERROR, self.texts.MSG_CLIPBOARD_EMPTY)
    
    def refresh_dict_tree(self):
        self.tree.clear()
        for letter, code in sorted(self.cipher.letter_to_code.items()):
            display_letter = letter
            if letter in ['\\', '"', "'"]:
                display_letter = f"\\{letter}"
            item = QTreeWidgetItem([display_letter, code])
            self.tree.addTopLevelItem(item)
    
    def encode_action(self):
        text = self.entry_text.toPlainText().strip()
        if not text:
            QMessageBox.information(self, self.texts.MSG_INFO, self.texts.MSG_ENTER_TEXT)
            return
        result = self.cipher.encode_text(text)
        self.encoded_text.setText(result)
        if self.config.get_setting('save_history', 'true') == 'true':
            self.config.add_history_item(text, result, 'encode')
            self.history_changed.emit()
    
    def decode_action(self):
        encoded = self.entry_encoded.toPlainText().strip()
        if not encoded:
            QMessageBox.information(self, self.texts.MSG_INFO, self.texts.MSG_ENTER_ENCODED)
            return
        result = self.cipher.decode_text(encoded)
        if result is None:
            QMessageBox.critical(self, self.texts.MSG_ERROR, self.texts.MSG_DECODE_ERROR)
        else:
            self.decoded_text.setText(result)
            if self.config.get_setting('save_history', 'true') == 'true':
                self.config.add_history_item(result, encoded, 'decode')
                self.history_changed.emit()
    
    def export_dict(self):
        file_path, _ = QFileDialog.getSaveFileName(self, self.texts.DIALOG_EXPORT_TITLE, "", self.texts.FILE_FILTER_JSON)
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(self.cipher.letter_to_code, f, ensure_ascii=False, indent=2)
                QMessageBox.information(self, self.texts.MSG_SUCCESS, self.texts.MSG_DICT_SAVED.format(file_path))
            except Exception as e:
                QMessageBox.critical(self, self.texts.MSG_ERROR, self.texts.MSG_SAVE_ERROR.format(e))
    
    def import_dict(self):
        file_path, _ = QFileDialog.getOpenFileName(self, self.texts.DIALOG_IMPORT_TITLE, "", self.texts.FILE_FILTER_JSON)
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if self.cipher.load_dict(data):
                    self.refresh_dict_tree()
                    self.seed_label.setText(self.texts.SETTINGS_SEED.format(self.texts.SETTINGS_SEED_IMPORTED))
                    QMessageBox.information(self, self.texts.MSG_SUCCESS, self.texts.MSG_DICT_LOADED)
                else:
                    QMessageBox.critical(self, self.texts.MSG_ERROR, self.texts.MSG_DICT_INVALID)
            except Exception as e:
                QMessageBox.critical(self, self.texts.MSG_ERROR, self.texts.MSG_LOAD_ERROR.format(e))
    
    def regenerate_dict_dialog(self):
        seed, ok = QInputDialog.getText(self, self.texts.DIALOG_REGENERATE_TITLE, self.texts.DIALOG_REGENERATE_TEXT)
        if ok and seed is not None:
            self.cipher.generate_dict(seed)
            self.refresh_dict_tree()
            self.seed_label.setText(self.texts.SETTINGS_SEED.format(f"'{seed}'"))
            QMessageBox.information(self, self.texts.MSG_SUCCESS, self.texts.MSG_REGENERATED.format(seed))
    
    def random_seed(self):
        self.cipher.generate_dict()
        self.refresh_dict_tree()
        self.seed_label.setText(self.texts.SETTINGS_SEED.format(self.texts.SETTINGS_SEED_RANDOM))
        QMessageBox.information(self, self.texts.MSG_SUCCESS, self.texts.MSG_RANDOM_GENERATED)
    
    def copy_dict_json(self):
        json_str = json.dumps(self.cipher.letter_to_code, ensure_ascii=False, indent=2)
        clipboard = QApplication.clipboard()
        clipboard.setText(json_str)
        QMessageBox.information(self, self.texts.MSG_SUCCESS, self.texts.MSG_DICT_COPIED)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())