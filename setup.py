from setuptools import setup, find_packages

setup(
    name="PersonalPythonPackage",
    version="0.2.0",
    author="LoloCG",
    author_email="",
    description="My own collection of reusable functions and classes for several python libraries and other...",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/LoloCG/PersonalPythonPackage",
    packages=find_packages(include=['personalpythonpackage', 'personalpythonpackage.*']),
    install_requires=[],
    extras_require={
        'pandas': ['pandas'], 
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)



