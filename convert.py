from PIL import Image

# Открываем ваш PNG (желательно, чтобы он был квадратным, например 512x512)
img = Image.open("ascii-art (4).png")

# Сохраняем как ICO с набором стандартных размеров для Windows
icon_sizes = [(16, 16), (32, 32), (48, 48), (256, 256)]
img.save("my_icon.ico", sizes=icon_sizes)
print("Конвертация успешна! Файл my_icon.ico создан.")
