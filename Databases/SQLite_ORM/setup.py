from setuptools import setup, find_packages

setup(
    name="SQLite-ORM",
    version="v1.0.5",
    author="LoloCG",
    author_email="",
    description="Personal SQLite ORM for light weight applications.",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/LoloCG/Lolos_Packages",
    packages=find_packages(include=['SQLite_ORM', 'SQLite_ORM.*']),
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



