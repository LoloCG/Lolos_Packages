from setuptools import setup, find_packages

setup(
    name="PersonalPythonPackage",
    version="0.1.0",
    author="LoloCG",
    author_email="",
    description="My own collection of reusable functions and classes for several python libraries and other...",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/LoloCG/PersonalPythonPackage",  # Your repository URL
    packages=find_packages(),  # Automatically finds your submodules
    install_requires=[],  # Base dependencies (if any): "numpy", "pandas", ...
    extras_require={
        'sqlite': ['pysqlite3'],  # SQLite-related dependencies
        'pandas': ['pandas'],  # Pandas-only functionality
        'plotting': ['numpy', 'pandas', 'matplotlib', 'xlsxwriter'],  # Plotting functionality
        'pyside': ['pyside6'],  # PySide for UI
        'curses': ['curses'],  # Curses for terminal UIs
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
