from setuptools import setup

setup(
    name="convert2QRhead",
    version="1.1",
    author="YechengZhou",
    author_email="ethanchou1126@gmail.com",
    description=(
        """Convert your head portrait to QR code like head portrait. Written in Python"""
    ),
    license="BSD",
    url="https://github.com/YechengZhou/convert2QRhead",
    install_requires = ['docopt', 'Pillow'],
    scripts=['convert2QRhead.py']
)
