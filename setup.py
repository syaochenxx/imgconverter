from setuptools import setup, find_packages

setup(
    name='imgconverter',
    version='0.1.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'imgconverter=imgconverter.main:main',
        ],
    },
    install_requires=[
        'Pillow',
    ],
    author='Syao',
    description='Утилита для конвертации изображений',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
