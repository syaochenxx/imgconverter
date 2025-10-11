#!/usr/bin/env python3

import os
import argparse
from PIL import Image

BG_WHITE = (255, 255, 255)
BG_BLACK = (0, 0, 0)

def get_rgb_mode(i_format):
	if i_format in ['png', 'webp']:
		return 'RGBA'
	return 'RGB'

def get_l_mod(i_format):
	if i_format in ['png', 'webp']:
		return 'LA'
	return 'L'

def resize_image(img, size):
	width, height = map(int, size.split('x'))
	return img.resize((width, height))

def get_image_with_background(img, color_mod, mode):
	if color_mod:
		color = BG_WHITE
	else:
		color = BG_BLACK
	new_image = Image.new(mode, img.size, color)
	new_image.paste(img, mask=img.split()[3])
	return new_image

def convert_image(argc):
	try:
		with Image.open(argc.file) as img:
			if argc.grey:
				mode = get_l_mode(argc.mode)
			else:
				mode = get_rgb_mode(argc.mode)
			if img.mode in ['LA', 'RGBA'] and mode in ['L', 'RGB']:
				img = get_image_with_background(img, argc.white, mode)
			if img.mode != mode: img = img.convert(mode)
			params = {
				'format':	argc.mode.upper(),
				'quality':	argc.quality,
				'optimize': argc.optimize,
			}

			if (argc.size):
				print(argc.size)
				img = resize_image(img, argc.size)
			outputfile = argc.file.rsplit('.', 1)[0] + f".{argc.mode}"
			img.save(outputfile, **params)
			print(f"Конвертированно: {argc.file} -> {outputfile}")
	except Exception as e:
		print(f"@error <> Ошибка конвертации: {e}")


def main():
	parser = argparse.ArgumentParser(
        description='Конвертер изображений с поддержкой форматов и параметров',
        epilog='Пример: imgconverter image.png -m jpeg -q 80 -s 800x600'
    )
	parser.add_argument('file', help='Входной файл изображения')
	parser.add_argument('-m', '--mode', choices=['png', 'webp', 'jpg', 'jpeg'], default='jpg', help='Формат конвертации, default - jpg)')
	parser.add_argument('-q', '--quality', type=int, default=100, help='Качество сжатия 0-100, default - 100')
	parser.add_argument('-o', '--optimize', action='store_true', help='Включить оптимизацию')
	parser.add_argument('-s', '--size', help='Размер изображения (например 800x600)')
	parser.add_argument('-w', '--white', action='store_true', default=False, help="Белый фон для для конвертации из png/webp, default - black background")
	parser.add_argument('-g', '--grey', action='store_true', help='Черно-белый формат')
	argc = parser.parse_args()
	convert_image(argc)

if __name__ == "__main__":
	main()