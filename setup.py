from setuptools import setup, find_packages

VERSION = '0.0.4'
DESCRIPTION = 'Fortunae quer ser tornar uma biblioteca de análise financeira. Importa indicadores fundamentalistas de ações e fundos'
LONG_DESCRIPTION = ' Fortunae quer ser tornar uma biblioteca de análise financeira. Voltada pra importação de indicadores fundamentalistas atuais de ações ou fundos imobiliarios usando multithreading.'

# Setting up
setup(
    name="fortunae",
    version=VERSION,
    author="Arthur Chabole",
    author_email="<chabole.arthur@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pandas', 'requests'],
    keywords=['python', 'finance', 'money', 'invest'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)