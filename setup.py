from setuptools import setup, Extension
from Cython.Build import cythonize
import os

# Define the paths to LP Solve
base_path = os.path.join(os.path.dirname(__file__), 'lpsolve')

include_dirs = [base_path]
library_dirs = [base_path]
libraries = ["lpsolve55"]

extensions = [
    Extension(
        "clara.pylpsolve",
        ["clara/pylpsolve.pyx"],
        include_dirs=include_dirs,
        library_dirs=library_dirs,
        libraries=libraries,
    )
]

setup(
    ext_modules=cythonize(extensions, language_level="3"),
)