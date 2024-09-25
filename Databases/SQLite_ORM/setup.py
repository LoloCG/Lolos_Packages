from setuptools import setup, find_packages

setup(
    name="SQLite-ORM",
    version="v1.0.0",
    author="LoloCG",
    author_email="",
    description="Personal SQLite ORM for light weight applications.",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/LoloCG/Lolos-Packages",
    packages=find_packages(include=['SQLite-ORM', 'SQLite-ORM.*']),
    install_requires=[], # SQLite is built-in, so no base dependencies
    extras_require={
        'sqlite': [],
        'pandas_addon': ['pandas'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)



