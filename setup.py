from setuptools import setup, find_packages

setup(
    name='pyqt-custom-frameless-mainwindow',
    version='0.0.1',
    author='Jung Gyu Yoon',
    author_email='yjg30737@gmail.com',
    license='MIT',
    packages=find_packages(),
    description='PyQt Custom Frameless Main Window',
    url='https://github.com/yjg30737/pyqt-custom-frameless-mainwindow.git',
    install_requires=[
        'PyQt5>=5.8'
    ]
)