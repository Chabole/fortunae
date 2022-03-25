from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent

VERSION = '0.0.9'
DESCRIPTION = 'Fortunae quer ser tornar uma biblioteca de análise financeira. Indicada para importar indicadores fundamentalistas de ações e fundos'
LONG_DESCRIPTION = (this_directory / "README.md").read_text()

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