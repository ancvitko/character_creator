from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(["stats_calculator.pyx", "main.pyx", "utils.pyx", "character.pyx", "ui.pyx"]),
)
