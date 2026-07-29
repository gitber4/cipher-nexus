"""
cipher_core.py - Ядро шифрования Cipher Nexus V3.1
Содержит логику генерации словаря, кодирования и декодирования
Поддерживает буквы, цифры (включая 0) и специальные символы
"""

import random
import itertools
import hashlib


class CipherNexus:
    """Основной класс шифрования с поддержкой seed"""
    VERSION = "3.1"
    APP_NAME = "Cipher Nexus"

    def __init__(self, seed=None):
        # Все поддерживаемые буквы (русские + английские, оба регистра)
        self.letters = []
        self.letters.extend("абвгдежзийклмнопрстуфхцчшщъыьэюя")
        self.letters.extend("АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ")
        self.letters.extend("abcdefghijklmnopqrstuvwxyz")
        self.letters.extend("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        
        # Цифры (включая 0!)
        self.letters.extend("0123456789")
        
        # Специальные символы
        self.letters.extend("-_+=")
        self.letters.extend("!\"№;%:?*()@#$^&|/\\'><{}[]")
        
        # Знаки препинания (теперь кодируются через seed)
        self.letters.extend(".,!?;")
        
        # Всего символов: 163

        # Все возможные трёхзначные коды из цифр 1-9 (0 - разделитель)
        self.all_codes = [''.join(p) for p in itertools.product('123456789', repeat=3)]
        
        # Словари для шифрования
        self.letter_to_code = {}
        self.code_to_letter = {}
        
        # Разделитель (0 используется как разделитель между словами)
        self.separator = '0'
        self.current_seed = None

        if seed is not None:
            self.generate_dict(seed)
        else:
            self.generate_dict()

    def generate_dict(self, seed=None):
        """
        Генерирует словарь на основе seed.
        Если seed None - используется случайный seed.
        """
        if seed is not None:
            self.current_seed = seed
            # Преобразуем строку в число через MD5
            seed_int = int(hashlib.md5(seed.encode()).hexdigest(), 16) % (2**32)
            rng = random.Random(seed_int)
        else:
            self.current_seed = None
            rng = random.Random()

        # Перемешиваем коды
        codes = self.all_codes.copy()
        rng.shuffle(codes)
        codes = codes[:len(self.letters)]

        self.letter_to_code = {letter: code for letter, code in zip(self.letters, codes)}
        self.code_to_letter = {code: letter for letter, code in zip(self.letters, codes)}

    def load_dict(self, letter_to_code):
        """
        Загружает словарь из внешнего словаря.
        Проверяет валидность: все буквы должны быть, коды должны быть уникальными и из 1-9.
        """
        # Проверяем, что все буквы присутствуют
        if set(letter_to_code.keys()) != set(self.letters):
            missing = set(self.letters) - set(letter_to_code.keys())
            extra = set(letter_to_code.keys()) - set(self.letters)
            print(f"Missing: {missing}")
            print(f"Extra: {extra}")
            return False

        # Проверяем формат кодов
        if any(len(code) != 3 or any(c not in '123456789' for c in code)
               for code in letter_to_code.values()):
            return False

        # Проверяем уникальность кодов
        if len(set(letter_to_code.values())) != len(self.letters):
            return False

        self.letter_to_code = letter_to_code.copy()
        self.code_to_letter = {v: k for k, v in self.letter_to_code.items()}
        self.current_seed = None
        return True

    def encode_text(self, text):
        """Кодирует текст в цифровую строку"""
        if not text:
            return ""

        result = []
        for ch in text:
            if ch in self.letter_to_code:
                result.append(self.letter_to_code[ch])
            elif ch == ' ':
                result.append(self.separator)
            # Остальные символы игнорируем
        return ''.join(result)

    def decode_text(self, encoded):
        """Декодирует цифровую строку обратно в текст"""
        if not encoded:
            return ""

        parts = encoded.split(self.separator)
        decoded_parts = []

        for part in parts:
            if part == "":
                decoded_parts.append("")
                continue

            word = []
            i = 0
            while i < len(part):
                # Берем 3 символа как код
                if i + 3 > len(part):
                    return None  # Ошибка формата
                
                code = part[i:i+3]
                if code not in self.code_to_letter:
                    return None  # Неизвестный код
                
                word.append(self.code_to_letter[code])
                i += 3

            decoded_parts.append(''.join(word))

        return ' '.join(decoded_parts)

    def get_stats(self):
        """Возвращает статистику о словаре"""
        return {
            'total_letters': len(self.letters),
            'total_codes': len(self.all_codes),
            'used_codes': len(self.letter_to_code),
            'free_codes': len(self.all_codes) - len(self.letter_to_code),
            'code_length': 3,
            'separator': self.separator,
            'supported_chars': sorted(self.letters)
        }

    def get_all_symbols(self):
        """Возвращает список всех поддерживаемых символов для отображения"""
        return {
            'letters_ru_lower': 'абвгдежзийклмнопрстуфхцчшщъыьэюя',
            'letters_ru_upper': 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ',
            'letters_en_lower': 'abcdefghijklmnopqrstuvwxyz',
            'letters_en_upper': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
            'digits': '0123456789',
            'specials': '-_+=!"№;%:?*()@#$^&|/\\\'><{}[]',
            'punctuation': '.,!?;'
        }